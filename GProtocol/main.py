import threading
from ax45sEngine.algorithms import trans
from ghostprotocol import nrf24l01,portChecker
from random import randint
from time import sleep

# Port Selection
ports = portChecker()
for i,port in enumerate(ports) : print(f"{i+1}-) {port}")
port = ports[int(input("Select Port : "))-1]
nodeID = input("nodeID >> ")

# Creating the nrf24l01 object
nrf = nrf24l01(port,nodeID,"237415","AX45-S") # Creating object nrf24l01
print(nrf.cardSpec) # See the properties of the object

# Setting transmitter side
def transmitter():
    while True:
        nrf.tx(input())
        #s,f,t = m.tx(input()).values()
        #print(f"Total Success : {m.totalCorrectTransmissions} | Total Failed {m.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")

# Setting receiver side
def receiver():
    while True:
        cache = nrf.rx()
        if cache != None:
            try:
                node, data = cache["node"], cache["data"]
                print(f"{node} >> {data}")
            except: pass


t1 = threading.Thread(target=transmitter)
t2 = threading.Thread(target=receiver)

t1.start()
t2.start()