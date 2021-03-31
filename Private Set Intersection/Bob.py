#!/usr/bin/python3

import logging
from time import sleep
import numpy as np
from numpysocket import NumpySocket
import main

logger = logging.getLogger('Bob')
logger.setLevel(logging.INFO)

host_ip = 'localhost'  # change me

npSocket = NumpySocket()
while(True):
    try:
        npSocket.startClient(host_ip, 9999)
        break
    except:
        logger.warning("connection failed, make sure `server` is running.")
        sleep(1)
        continue

logger.info("connected to server")

""" q=np.array([main.generateBigPrime(8)])
logger.info("sending q to Alice ...")
npSocket.send(q) """

q=17
# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

beta = main.generNumberZq(q)

SetB = main.generSet(996)
SetPrimeB=main.ComputeRandomOracleAndPowerofSet(SetB,beta)
npSocket.send(SetPrimeB)
print("sending SetPrimeB to Alice ...")

SetPrimeA = npSocket.recieve()
#logger.info(SetPrimeA)
print("SetPrimeA received from Alice ...")
print(SetPrimeA)

SetSecondB = npSocket.recieve()
#logger.info(SetSecondB)
print("SetSecondB received from Alice ...")
print(SetSecondB)


SetSecondA=main.ComputePowerofSet(SetPrimeA,beta)
print("sending SetSecondA to Bob ...")
npSocket.send(SetSecondA)

_, _, y_ind = np.intersect1d(SetSecondA, SetSecondB, return_indices=True)
if y_ind.size==0:
  print("Bob has no element in common with Alice")
else:
  print("Bob has the folowing elements in common with Alice",SetB[y_ind]) 
# restore np.load for future normal usage
np.load = np_load_old

logger.info("closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("client already disconnected")
