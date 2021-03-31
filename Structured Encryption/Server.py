#!/usr/bin/python3

import logging
import numpy as np
from numpysocket import NumpySocket
import time
import main

logger = logging.getLogger('server')
logger.setLevel(logging.INFO)

npSocket = NumpySocket()

logger.info("starting server, waiting for client")
npSocket.startServer(9999)

np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

DX = npSocket.recieve()
logger.info("DX recieved")
time.sleep(3)

Kw = npSocket.recieve()
logger.info("kw receied")
time.sleep(3)

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


L=query(Kw[0],DX[0])
npSocket.send(np.array(L))
logger.info("sending L")
time.sleep(3)
# restore np.load for future normal usage
np.load = np_load_old

logger.info("closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("server already disconnected")
