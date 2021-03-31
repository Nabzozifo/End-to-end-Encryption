#!/usr/bin/python3
import logging
from time import sleep
import numpy as np
from numpysocket import NumpySocket
import mains
import time

logger = logging.getLogger('Alice')
logger.setLevel(logging.INFO)

host_ip = 'localhost' 

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

print('Alice : Extracting Keyword ....')
MM=mains.extract_Keyword()
print('Alice : Build DX ....')
DX=mains.buildDX(MM)
time.sleep(3)

npSocket.send(np.array([DX]))
print('Alice : Send DX to Bob ....')
time.sleep(3)

w=input("Enter the keyword : ")
Kw=mains.create_sha256_signature(mains.K1,w)
npSocket.send(np.array([Kw]))
print('Alice : Send Kw to Bob ....')
time.sleep(3)
np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

L = npSocket.recieve()
logger.info("L recieved.")
time.sleep(3)
# restore np.load for future normal usage
np.load = np_load_old

print('Result for search of : ',w)
mains.display_result(L,w)
logger.info("closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("client already disconnected")
