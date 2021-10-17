from ghostprotocol import nrf24l01,portChecker
from random import randint
from time import sleep

# Port Selection
ports = portChecker()
for i,port in enumerate(ports) : print(f"{i+1}-) {port}")
port = ports[int(input("Select Port : "))-1]


m = nrf24l01(port,"MEDIPOL","237415","AX45-S") # Creating object nrf24l01
print(m.cardSpec) # See the properties of the object


while True:
    
    # Transmitting Mode
    data = input("Enter the message to be sent >> ")
    s,f,t = m.tx(data).values()
    print(f"Total Success : {m.totalCorrectTransmissions} | Total Failed {m.totalIncorrectTransmissions} | Success : {s} | Failed {f} | Time Elapsed : {t}")

    # Receiving Mode
    """
    cache = m.rx()
    if cache != None:
        print(f">> {cache}")
    """