#!/usr/bin/python3

import logging
import numpy as np
from numpysocket import NumpySocket
import main

logger = logging.getLogger('Alice')
logger.setLevel(logging.INFO)

npSocket = NumpySocket()

logger.info("starting server, waiting for client")
npSocket.startServer(9999)

""" # save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

q = npSocket.recieve()
logger.info(q)
logger.info("q received from Bob")

# restore np.load for future normal usage
np.load = np_load_old """
q=17
# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

SetPrimeB = npSocket.recieve()
# logger.info(SetPrimeB)
print("SetPrimeB received from Bob ...")
print(SetPrimeB)


alpha = main.generNumberZq(q)

SetA = main.generSet(996)
SetPrimeA=main.ComputeRandomOracleAndPowerofSet(SetA,alpha)
npSocket.send(SetPrimeA)
print("sending SetPrimeA to Bob ...")


SetSecondB=main.ComputePowerofSet(SetPrimeB,alpha)
npSocket.send(SetSecondB)
print("sending SetSecondB to Bob ...")

SetSecondA = npSocket.recieve()
print("receiving SetSecondA to Bob ...")
print(SetSecondA)

_, x_ind, _ = np.intersect1d(SetSecondA, SetSecondB, return_indices=True)
if x_ind.size==0:
  print("Alice has no element in common with Bob")
else:
  print("Alice has the folowing elements in common with Bob",SetA[x_ind]) 

# restore np.load for future normal usage
np.load = np_load_old


logger.info("closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("server already disconnected")
