import hashlib
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import hmac
import binascii
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from collections import defaultdict
import random
import main

df = pd.read_csv("document.csv")

'''  create a vocabulary of words  '''

nltk.download("stopwords")

def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

#load a set of stop words
stopword_set = set(stopwords.words("english"))
#get the text column 
docs=df["Body"].tolist()

#ignore words that appear in 85% of documents, 
#eliminate stop words
cv=CountVectorizer(max_df=0.85,stop_words=stopword_set)
word_count_vector=cv.fit_transform(docs)

"""Extracting keyword """
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)
feature_names=cv.get_feature_names()

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results



def extract_Keyword():
    A = defaultdict(list)
    for i in range (len(docs)):
        #generate tf-idf for the given document
        tf_idf_vector=tfidf_transformer.transform(cv.transform([docs[i]]))

        #sort the tf-idf vectors by descending order of scores
        sorted_items=sort_coo(tf_idf_vector.tocoo())

        #extract only the top n; n here is 10
        keywords=extract_topn_from_vector(feature_names,sorted_items,10)
        for k in keywords:
            A[k].append(df['Message-ID'][i])
    return A




K1=''.join([str(elem) for elem in [random.randint(0, 1) for i in range(32)]])
K2=''.join([str(elem) for elem in [random.randint(0, 1) for i in range(32)]])



def buildDX(MM):
    D={}
    L=[]
    for w in MM.keys():
        Kw=main.create_sha256_signature(K1, w)
        cnt=0
        for id in MM[w]:
            L.append((main.create_sha256_signature(Kw, str(cnt)),main.encrypt(K2,id)))
            cnt+=1
    for lt in L:
        D[lt[0]]=lt[1]
    return D


BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(password,plain_text):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**4, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(password,enc_dict):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**4, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

def query(w,DX):
  L=[]
  i=0
  l=main.create_sha256_signature(w, str(i))
  if l not in DX.keys():
    return L
  while DX[l]!= None :
    L.append(DX[l])
    i=i+1
    l=main.create_sha256_signature(w, str(i))
    if l not in DX.keys():
      break
  return L

def display_result(L,w):
    if L==[]:
        print("Not result for the keyword : ",w)
    else:
        for ct in L:
            print(main.decrypt(K2,ct).decode("UTF-8"))

