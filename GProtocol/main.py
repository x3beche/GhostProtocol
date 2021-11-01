import threading
from ghostprotocol import nrf24l01,portChecker

# Port Selection
ports = portChecker()
for i,port in enumerate(ports) : print(f"{i+1}-) {port}")
port = ports[int(input("Select Port : "))-1]
nodeID = input("nodeID >> ")

# Creating the nrf24l01 object
nrf = nrf24l01(port,nodeID,"237415","AX45-S") # Creating object nrf24l01
nrf.moduleInit()
print(nrf.cardSpec) # See the properties of the object

# Setting transmitter side
def transmitter():
    while True:
        dataToTX = input()
        if dataToTX[:10] == "/send_file":
            fileName = dataToTX.split(" ",1)[1]
            s,f,t = nrf.fileTX(fileName).values()
            print(f"Total Success : {nrf.totalCorrectTransmissions} | Total Failed {nrf.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")
        else :
            s,f,t = nrf.msgTX(dataToTX).values()
            print(f"Total Success : {nrf.totalCorrectTransmissions} | Total Failed {nrf.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")

# Setting receiver side1
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

#tx_data = nrf.fileToData("nordic.png")
#print(nrf.masterCrypter(tx_data,False))