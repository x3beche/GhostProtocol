import threading
from ghostprotocol import nrf24l01,portChecker
from time import sleep

# Port Selection
port = portChecker()
nodeId = input("nodeId >> ")

# Creating the nrf24l01 object
nrf = nrf24l01(port,nodeId,237415,"AX45-S") # Creating object nrf24l01
nrf.moduleInit()
print(nrf.cardSpec) # See the properties of the object

# Setting transmitter side
def transmitter():
    while True:
        dataToTX = input()
        if dataToTX[:10] == "/send_file":
            fileName = dataToTX.split(" ",1)[1]
            s,f,t = nrf.fileTX(fileName).values()
            #print(f"Total Success : {nrf.totalCorrectTransmissions} | Total Failed {nrf.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")
        else :
            s,f,t = nrf.msgTX(dataToTX).values()
            #print(f"Total Success : {nrf.totalCorrectTransmissions} | Total Failed {nrf.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")

# Setting receiver side1
def receiver():
    while True:
        msg = nrf.rx()
        if msg != None:
            try:
                node, data = msg["node"], msg["data"]
                print(f"{node} >> {data}")
            except: pass
        sleep(0.01)

t1 = threading.Thread(target=transmitter)
t2 = threading.Thread(target=receiver)

t1.start()
t2.start()