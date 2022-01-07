from ax45sEngine.algorithms import axen,axde
from serial.tools.list_ports import comports
from serial import Serial
from time import sleep,time
from base64 import b64decode,b64encode
from json import loads,dumps

# Returns a list of devices on which ports
def portChecker():
    PORTS=[]
    for i in comports(): PORTS.append(str(i).split(" ")[0])
    for i,port in enumerate(PORTS) : print(f"{i+1}-) {port}")
    return PORTS[int(input("Select Port : "))-1]

# Main nrf24l01 object 
class nrf24l01:

    # Required definitions and initialization of the module
    def __init__(self,port,node_id,key,encryptionModule):
        
        # Module configurations :
        self.radioDetails     = [] # Information from the radio, variables will come in the initialization part
        self.portTimeout      = 5  # Where to use : module initialization
        self.timeOutShort     = 5  # Where to use : when sending data
        self.timeOutLong      = 15 # Where to use : to send start and end flags
        self.encryptionModule = encryptionModule # Setting crypto module
        self.port             = port    # Setting COM port
        self.nodeId           = node_id # Setting node id
        self.key              = str(key)     # Setting key file
        self.baud             = 115200  # Setting baud rate
        self.mode             = "IDLE"  # Setting Mode
        self.streamOriginFlag = self.masterCrypter("STREAM-ORIGIN",True) # Calculating the origin flag
        self.streamEndFlag    = self.masterCrypter("END-STREAM",True)    # Calculating the end flag
        
        # Packet size : nrf24l01 transmits 32 bits, but \r\n added to the end 
        # of the message gives a total of 4 bits, 28 bits set plus 4 bits gives a total of 32 bits )
        self.packetSize       = 28 # Do not change!
        
        # Statistical information
        self.totalIncorrectTransmissions = 0
        self.totalCorrectTransmissions = 0
        self.totalReceived = 0

    # Module Initialization function for making sure the correct module is connected and initialized successfully
    def moduleInit(self):
        try:
            self.ser = Serial(self.port,self.baud) # Serial connection to module
            sleep(1) # Connection timeout
            start_time = time()
            while True:
                end_time = time()
                if self.ser.inWaiting()>0: self.radioDetails.append(self.ser.readline()[:-2].decode('utf-8', errors='replace').rstrip("\x00").rstrip("\r"))
                if len(self.radioDetails)==17:
                    for x in range(0,len(self.radioDetails)): self.radioDetails[x]=self.radioDetails[x].split("=")[1].strip()
                    if self.radioDetails[13]=="nRF24L01+" or self.radioDetails[13]=="nRF24L01": 
                        print("RESPOND :: Module initialized successfully")
                        break
                if end_time-start_time>self.portTimeout: print("ERROR :: Module doesn't confirmed by main core! Make sure that the cable connections to the communication card are correct. "),exit()
        except: print("ERROR :: There was an error connecting to the card, make sure you entered the data \ncorrectly or the card is not run with another program!"),exit()
    
    # See the specifications of the object
    @property
    def cardSpec(self):
        return f"""
        portTimeout      = {self.portTimeout} sec
        timeOutShort     = {self.timeOutShort} sec
        timeOutLong      = {self.timeOutLong} sec
        encryptionModule = {self.encryptionModule}
        dataRate         = {self.radioDetails[12]}
        moduleModel      = {self.radioDetails[13]}
        CRC Length       = {self.radioDetails[14]}
        PA Power         = {self.radioDetails[15]}
        Pipe Addres      = {self.radioDetails[2].split(" ")[1]}
        port             = {self.port}
        nodeId           = {self.nodeId}
        keyFileID        = {self.key}
        baudRate         = {self.baud}
        GPPacketSize     = {(self.packetSize+4)*8} bits
        mode             = {self.mode}
        streamOriginFlag = {self.streamOriginFlag}
        streamEndFlag    = {self.streamEndFlag}
        """
    
    # Functions for data operations
    def msgTX(self,data):
        #print("JSON Format -> ",dumps({"dataType":"msg","data":data}))
        return self.tx(dumps({"dataType":"msg","data":data}))
    def msgRX(self,node,data):
        return {"node":node,"data":data}
    def fileTX(self,fileInput):
        with open(fileInput,"rb") as file: 
            try : fileName,fileType,data = fileInput.rsplit('.', 1)[0],fileInput.rsplit('.', 1)[1],b64encode(file.read()).decode()
            except : print("Wrong file format! The file must have an extension."),exit()
        return self.tx(dumps({"dataType":"file","fileName":fileName,"fileType":fileType,"data":data}))
    def fileRX(self,node,data):
        fileName = data["fileName"]+"."+data["fileType"]
        with open(fileName,"wb") as file: file.write(b64decode(data["data"].encode()))
        return {"node":node,"data":fileName+" saved in main directiory."}

    # Main crypto handler
    def masterCrypter(self,data,direction):
        # Direction :
        # True  -> Encrption  
        # False -> Decryption
        if self.encryptionModule == "AX45-S":
            if    direction==True  : return axen(data,self.key) # Encryption
            elif  direction==False : return axde(data,self.key) # Decryption
        else: raise ValueError('The encryption algorithm you entered is not available in the system.')
    
    # Transmitting module
    def tx(self, data):
        while True:
            if self.mode=="IDLE":

                self.mode = "TX" # Posting module status to the object
                #sleep(0.1)            
                # Initial preparation for sending data
                
                startTime=time()
                incorrectTransmissions = 0
                correctTransmissions = 0
                data = self.masterCrypter(data,True) # Data encryption
                #print("Encrpypted -> ",data)
                datasets = [data[i:i+self.packetSize] for i in range(0, len(data), self.packetSize)] # Split data into sets of 28 bytes

                
                # Flags the channel for the start of the broadcast, if not confirmed the broadcast will not start
                error_value=False 
                tx_start= self.masterCrypter("STREAM-ORIGIN+"+str(len(data))+"+"+self.nodeId,True)+"\r\n"   # preparing origin flag
                self.ser.write(tx_start.encode())                                          # sending origin flag
                
                readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r") 
                #print(readline)

                #.rstrip("\x00").rstrip("\r")     # checking return from module

                
                
                
                
                
                # # If the message transmission is not confirmed, 
                # it must be repeated until the timeout is reached.
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        incorrectTransmissions+=1
                        self.ser.write(tx_start.encode())
                        readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")

                        if readline=="code[200]" : 
                            error_value=False
                correctTransmissions+=1

                # Sending the main data
                for x in range(0,len(datasets)):
                    data=datasets[x]+"\r\n"
                    self.ser.write(data.encode())
                    readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                    if readline=="code[417]":
                        error_value=True
                        while error_value==True:

                            incorrectTransmissions+=1
                            self.ser.write(data.encode())
                            readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")

                            if readline=="code[200]":
                                error_value=False
                    correctTransmissions+=1

                # It marks the end of the broadcast, if it is not confirmed, the broadcast will not end until the timeout has passed.
                error_value=False 
                tx_stop=self.streamEndFlag+"\r\n"                                                   # preparing origin flag
                self.ser.write(tx_stop.encode())                                           # sending origin flag
                readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")     # checking return from module
                    
                # # If the message transmission is not confirmed, 
                # it must be repeated until the timeout is reached.
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        incorrectTransmissions+=1
                        self.ser.write(tx_stop.encode())
                        readline=self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                        if readline=="code[200]":
                            error_value=False
                correctTransmissions+=1
                
                endTime = time()
                self.totalIncorrectTransmissions += incorrectTransmissions
                self.totalCorrectTransmissions += correctTransmissions
                self.mode = "IDLE" # Posting module status to the object
                return {"success":correctTransmissions,"failed":incorrectTransmissions,"time":endTime-startTime}
  
    # Receiving mode
    def rx(self):
        if (self.ser.inWaiting()>0) and self.mode!="TX":
            a = self.ser.readline()[:-2].decode('utf-8', errors='replace').rstrip("\x00").rstrip("\r")
            if a[:13]==self.streamOriginFlag:
                cont, self.mode, datasets, datasetForDecrypt= True, "RX",[],""
                _, dataSize, nodeRxUser = self.masterCrypter(a, False).split("+")
                datasets.append(a)
                self.totalReceived+=1
                while cont==True:
                    a = self.ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                    if a==datasets[-1]: pass
                    else:
                        self.totalReceived+=1
                        datasets.append(a)
                    if a[:10]==self.streamEndFlag:
                        self.totalReceived+=1
                        cont=False

                for x in range(1,len(datasets)-1): datasetForDecrypt+=datasets[x]
                datasetDecrypted=self.masterCrypter(datasetForDecrypt,False)

                if (len(datasetDecrypted)==int(dataSize)) and (dataSize != 0): 
                    
                    self.mode,json_data = "IDLE",loads(datasetDecrypted) # Posting module status to the object
                    if json_data["dataType"] == "msg": return self.msgRX(nodeRxUser,json_data["data"])
                    elif json_data["dataType"] == "file": return self.fileRX(nodeRxUser,json_data)
                    else: return "Wrong data format!"
            
                else: 
                    self.mode = "IDLE" # Posting module status to the object
                    return "Fail"
        else: pass