from io import StringIO
import multiprocessing
import time
import mains
import subprocess
def worker():
	print('Alice : Extracting Keyword ....')
	MM=mains.extract_Keyword()
	print('Alice : Build DX ....')
	DX=mains.buildDX(MM)
	print('Alice : Send DX to Bob ....')
	w=input("Enter the keyword : ")
	Kw=mains.create_sha256_signature(mains.K1,w)
	print('Alice : Send Kw to Bob ....')

	return DX,Kw,MM,w

def my_service(DX,Kw):
	print('Bob : Compute L ....')
	L=mains.query(Kw,DX)
	print('Bob : Send L to Alice ....')
	return L

def result(L,w):
	print('Alice : Decryptind and displaying result ....')
	mains.display_result(L,w)

def verify(MM,w):
	print('MM[w] is : ')
	print(MM[w])

if __name__ == '__main__':
	DX,kw,MM,w=worker()
	L=my_service(DX,kw)
	result(L,w)
	verify(MM,w)