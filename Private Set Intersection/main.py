# from Crypto.Util import number 
from random import choice
from string import ascii_lowercase, digits
import random
import numpy as np
import hashlib 
from random import randint

def isPrime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

def generateBigPrime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n-1), 2**n)
        if isPrime(p, 1000):
            return p

def generSet(n):
  chars = ascii_lowercase + digits
  lst = [''.join(choice(chars) for _ in range(random.randint(5, 15))) for _ in range(n)]+['Naby','Nabzozifo',6,'Loubia']
  return np.array(lst)

def randomOracle(elem):
  return int(hashlib.sha256(elem.encode()).hexdigest(), 16)

def ComputeRandomOracleAndPowerofSet(parseset,power):
  result=map(randomOracle, parseset)
  return np.array(list(result))**power

def ComputePowerofSet(parseset,power):
  return parseset**power


def generNumberZq(q):
	return random.randint(1,q)

