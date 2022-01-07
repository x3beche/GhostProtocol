from PyQt6 import QtCore, QtGui, QtWidgets
from json import dump,dumps,load,loads
from base64 import b64decode,b64encode
from serial.tools.list_ports import comports
from time import sleep,time
from serial import Serial
from os import scandir
import datetime
import sys

class Ui_GP(object):

    #ax45-s
    def f_encrypt(self, oW,nW,rtry):
        own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
        if own>nwn: chc=94-own+nwn
        else: chc=nwn-own
        return rtry[1][chc-1]
    def f_decrypt(self, oW,nW,rtry):
        own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
        if own+nwn>94: chc=own+nwn-94
        else: chc=nwn+own
        return rtry[1][chc-1]
    def axen_algorithm(self,text,keyNumber):
        a,rtry,final=self.keyComplier(keyNumber)[1],self.keyComplier(keyNumber)[0],''
        oW=rtry[1][ord(a[1])-32]
        for y in range(0,len(text)):
            oW=self.f_encrypt(oW,text[y],rtry)
            final=final+oW
        return final
    def axde_algorithm(self,text,keyNumber):
        a,rtry,final=self.keyComplier(keyNumber)[1],self.keyComplier(keyNumber)[0],''
        oW=rtry[1][ord(a[1])-32]
        for y in range(0,len(text)):
            nW=text[y]
            final=final+self.f_decrypt(oW,nW,rtry)
            oW=text[y]
        return final
    def axen(self, text,keyNumber):
        self.total = len(dumps({"data":text})[10:len(dumps({"data":text}))-2])*2
        data = self.axen_algorithm(self.axen_algorithm(dumps({"data":text})[10:len(dumps({"data":text}))-2],keyNumber),keyNumber)

        return data
    def axde(self, text,keyNumber):
        self.total = len(dumps({"data":text})[10:len(dumps({"data":text}))-2])*2

        data = loads('{"data": "'+self.axde_algorithm(self.axde_algorithm(text,keyNumber),keyNumber)+'"}')["data"]
        return data
    def keyComplier(self, fileNumber):
        fileName,keyList='key'+str(fileNumber)+'.ax',[[],[]]
        try:
            with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
            if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
                for x in range(1,len(json_data["key"].keys())+1): keyList[0].append(str(x)),keyList[1].append(json_data["key"][str(x)])
                return keyList, [keyList[0][0],keyList[1][0]]
            else:print("This key file is not compatible with this encryption")
        except:print("Wrong key format!")
    def keyAnalyzer(self, fileNumber):
        fileName ='key'+str(fileNumber)+'.ax'
        try:
            keyAnalyzerData = ""
            with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
            if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
                keyLabel = "Algorithm = {}\nLayer = {}".format(json_data["algorithm"], json_data["layer"])
                keyAnalyzerData = ""
                for x in range(1,95):
                    if x == 94:
                        return [keyAnalyzerData + "{} - {}".format(x, json_data["key"][str(x)]), keyLabel]
                    keyAnalyzerData = keyAnalyzerData + "{} - {}\n".format(x, json_data["key"][str(x)])
        except:print("Wrong key format!")
    def fileLister(self, direction):
        programFiles,extensions,files = ["desktop.ini","AX45-S.exe","keyConverterOldToNew.py","algorithms.py","AX45-S.py","ax45sEngine","keygenerator.py"],["ax","axen"],[]
        with scandir() as entries:
            if direction == "EN":
                for entry in entries:
                    if entry.name.rsplit(".")[-1] not in extensions and entry.name not in programFiles and len(entry.name.split(".")) >= 2 : files.append(entry.name)
                return files
            elif direction == "DE":
                for entry in entries:
                    if entry.name.rsplit(".")[-1] == "axen" and len(entry.name.split("."))>=3: files.append(entry.name)
                return files
            elif direction == "KEY":
                for entry in entries: 
                    if entry.name.rsplit(".")[-1] == "ax" and len(entry.name.split("."))==2 :files.append(int(entry.name.replace("key","").split(".")[0]))
                return files
            else: return "Wrong direction!"
    def fileEN(self, fileInput,keynum):
        try:
            with open(fileInput,"rb") as file: data = self.axen(b64encode(file.read()).decode(),keynum)
        except: return False
        try:
            with open(fileInput+".axen","w") as file: file.write(data)
        except: return False
        return True
    def fileDE(self, fileInput,keynum):
        try:
            with open(fileInput,"r") as file: data = file.read() 
        except: return False
        try:
            with open(fileInput.rsplit(".",1)[0],"wb") as file: file.write(b64decode(self.axde(data,keynum)))
        except: return False
        return True

    #nrf24l01
    def moduleConfig(self,port,node_id,key,encryptionModule):
        
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
    def moduleInit(self):
        try:
            self.ser = Serial(self.port,self.baud) # Serial connection to module
            sleep(1) # Connection timeout
            start_time = time()
            while True:
                end_time = time()
                if self.ser.inWaiting()>0: self.radioDetails.append(self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r"))
                if len(self.radioDetails)==17:
                    for x in range(0,len(self.radioDetails)): self.radioDetails[x]=self.radioDetails[x].split("=")[1].strip()
                    if self.radioDetails[13]=="nRF24L01+" or self.radioDetails[13]=="nRF24L01": 
                        self.terminalUpdate("Module initialization completed.","SUCCESS")
                        self.selectMode("IDLE")
                        return True 
                if end_time-start_time>self.portTimeout: 
                    self.terminalUpdate("Error detected in module initialization.","WARNING")
                    self.alert("Error Handler","Module doesn't confirmed by main core! Make sure that the cable connections to the communication card are correct. ")
                    return False
        except:
            self.terminalUpdate("Error detected in module initialization.","WARNING")
            self.alert("Error Handler","There was an error connecting to the card, make sure you entered the data \ncorrectly or the card is not run with another program!")
            return False
    def msgTX(self,data):
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
    def masterCrypter(self,data,direction):
        # Direction :
        # True  -> Encrption  
        # False -> Decryption
        if self.encryptionModule == "AX45-S":
            if    direction==True  : return self.axen(data,self.key) # Encryption
            elif  direction==False : return self.axde(data,self.key) # Decryption
        else: raise ValueError('The encryption algorithm you entered is not available in the system.')
    def tx(self, data):
        while True:
            if self.mode=="IDLE":

                self.mode = "TX" # Posting module status to the object
                # Initial preparation for sending data
                startTime=time()
                incorrectTransmissions = 0
                correctTransmissions = 0
                data = self.masterCrypter(data,True) # Data encryption
                datasets = [data[i:i+self.packetSize] for i in range(0, len(data), self.packetSize)] # Split data into sets of 28 bytes

                # Flags the channel for the start of the broadcast, if not confirmed the broadcast will not start
                error_value=False 
                tx_start= self.masterCrypter("STREAM-ORIGIN+"+str(len(data))+"+"+self.nodeId,True)+"\r\n"   # preparing origin flag
                self.ser.write(tx_start.encode())                                          # sending origin flag

                readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r") 
                # # If the message transmission is not confirmed, 
                # it must be repeated until the timeout is reached.
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        incorrectTransmissions+=1
                        self.ser.write(tx_start.encode())
                        readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")

                        if readline=="code[200]" : 
                            error_value=False
                correctTransmissions+=1

                # Sending the main data
                for x in range(0,len(datasets)):
                    data=datasets[x]+"\r\n"
                    self.ser.write(data.encode())
                    readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")
                    if readline=="code[417]":
                        error_value=True
                        while error_value==True:

                            incorrectTransmissions+=1
                            self.ser.write(data.encode())
                            readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")

                            if readline=="code[200]":
                                error_value=False
                    correctTransmissions+=1

                # It marks the end of the broadcast, if it is not confirmed, the broadcast will not end until the timeout has passed.
                error_value=False 
                tx_stop=self.streamEndFlag+"\r\n"                                                   # preparing origin flag
                self.ser.write(tx_stop.encode())                                           # sending origin flag
                readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")     # checking return from module
                    
                # # If the message transmission is not confirmed, 
                # it must be repeated until the timeout is reached.
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        incorrectTransmissions+=1
                        self.ser.write(tx_stop.encode())
                        readline=self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")
                        if readline=="code[200]":
                            error_value=False
                correctTransmissions+=1
                
                endTime = time()
                self.totalIncorrectTransmissions += incorrectTransmissions
                self.totalCorrectTransmissions += correctTransmissions
                self.mode = "IDLE" # Posting module status to the object
                return {"success":correctTransmissions,"failed":incorrectTransmissions,"time":endTime-startTime}
    def rx(self):
        if (self.ser.inWaiting()>0) and self.mode!="TX":
            self.selectMode("RX")
            
            a = self.ser.readline()[:-2].decode('utf-8', errors='ignore').rstrip("\x00").rstrip("\r")
            if a[:13]==self.streamOriginFlag:
                cont, self.mode, datasets, datasetForDecrypt= True, "RX",[],""
                _, dataSize, nodeRxUser = self.masterCrypter(a, False).split("+")
                datasets.append(a)
                self.totalReceived+=1
                while cont==True:
                    a = self.ser.readline()[:-2].decode(errors='replace').rstrip("\x00").rstrip("\r")
                    if a==datasets[-1]: pass
                    else:
                        self.totalReceived+=1
                        datasets.append(a)
                    if a[:10]==self.streamEndFlag:
                        self.totalReceived+=1
                        cont=False
                for x in range(1,len(datasets)-1): datasetForDecrypt+=datasets[x]
                datasetDecrypted=self.masterCrypter(datasetForDecrypt.rstrip("\r"),False)

                if (len(datasetForDecrypt)==int(dataSize)) and (dataSize != 0):
                    self.selectMode("IDLE")
                    
                    self.mode,json_data = "IDLE",loads(datasetDecrypted) # Posting module status to the object
                    if json_data["dataType"] == "msg": return self.msgRX(nodeRxUser,json_data["data"])
                    elif json_data["dataType"] == "file": return self.fileRX(nodeRxUser,json_data)
                    else: return "Wrong data format!"
                else: 
                    self.selectMode("IDLE")
                    
                    self.mode = "IDLE" # Posting module status to the object
                    return "Fail"

        else: pass
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

    # GUI Side
    def setupUi(self, GP):
        GP.setObjectName("GP")
        GP.setWindowIcon(QtGui.QIcon("files/gp.ico"))
        GP.setFixedSize(660, 560)
        with open("files/chat.qss",'r') as f: GP.setStyleSheet(f.read())
        self.deviceFrame = QtWidgets.QGroupBox(GP)
        self.deviceFrame.setGeometry(QtCore.QRect(10, -10, 641, 161))
        self.deviceFrame.setTitle("")
        self.deviceFrame.setObjectName("deviceFrame")
        self.keyTitle = QtWidgets.QLabel(self.deviceFrame)
        self.keyTitle.setGeometry(QtCore.QRect(10, 30, 91, 21))
        self.keyTitle.setObjectName("keyTitle")
        self.usernameTitle = QtWidgets.QLabel(self.deviceFrame)
        self.usernameTitle.setGeometry(QtCore.QRect(10, 90, 91, 21))
        self.usernameTitle.setObjectName("usernameTitle")
        self.portTitle = QtWidgets.QLabel(self.deviceFrame)
        self.portTitle.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.portTitle.setObjectName("portTitle")
        self.keySelectionBox = QtWidgets.QComboBox(self.deviceFrame)
        self.keySelectionBox.setGeometry(QtCore.QRect(100, 30, 151, 22))
        self.keySelectionBox.setCurrentText("")
        self.keySelectionBox.setObjectName("keySelectionBox")
        self.portSelectionBox = QtWidgets.QComboBox(self.deviceFrame)
        self.portSelectionBox.setGeometry(QtCore.QRect(100, 60, 151, 22))
        self.portSelectionBox.setCurrentText("")
        self.portSelectionBox.setObjectName("portSelectionBox")
        self.usernameInput = QtWidgets.QLineEdit(self.deviceFrame)
        self.usernameInput.setGeometry(QtCore.QRect(100, 89, 150, 26))
        self.usernameInput.setObjectName("usernameInput")
        self.terminalBox = QtWidgets.QTextEdit(self.deviceFrame)
        self.terminalBox.setGeometry(QtCore.QRect(260, 32, 241, 117))
        self.terminalBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.terminalBox.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.terminalBox.setObjectName("terminalBox")
        self.deviceModes = QtWidgets.QGroupBox(self.deviceFrame)
        self.deviceModes.setGeometry(QtCore.QRect(510, 12, 121, 137))
        self.deviceModes.setTitle("")
        self.deviceModes.setObjectName("deviceModes")
        self.RXCheckBox = QtWidgets.QCheckBox(self.deviceModes)
        self.RXCheckBox.setGeometry(QtCore.QRect(10, 90, 101, 20))
        self.RXCheckBox.setObjectName("RXCheckBox")
        self.IDLECheckBox = QtWidgets.QCheckBox(self.deviceModes)
        self.IDLECheckBox.setGeometry(QtCore.QRect(10, 70, 82, 20))
        self.IDLECheckBox.setObjectName("IDLECheckBox")
        self.INITCheckBox = QtWidgets.QCheckBox(self.deviceModes)
        self.INITCheckBox.setGeometry(QtCore.QRect(10, 50, 121, 20))
        self.INITCheckBox.setObjectName("INITCheckBox")
        self.deviceModeTitle = QtWidgets.QLabel(self.deviceModes)
        self.deviceModeTitle.setGeometry(QtCore.QRect(10, 25, 81, 16))
        self.deviceModeTitle.setObjectName("deviceModeTitle")
        self.TXCheckBox = QtWidgets.QCheckBox(self.deviceModes)
        self.TXCheckBox.setGeometry(QtCore.QRect(10, 110, 121, 20))
        self.TXCheckBox.setObjectName("TXCheckBox")
        self.initializeModule = QtWidgets.QPushButton(self.deviceFrame)
        self.initializeModule.setGeometry(QtCore.QRect(10, 120, 241, 31))
        self.initializeModule.setObjectName("initializeModule")
        self.messages = QtWidgets.QTextEdit(GP)
        self.messages.setGeometry(QtCore.QRect(10, 160, 641, 351))
        self.messages.setObjectName("messages")
        self.sendMsgButton = QtWidgets.QPushButton(GP)
        self.sendMsgButton.setGeometry(QtCore.QRect(430, 520, 111, 31))
        self.sendMsgButton.setObjectName("sendMsgButton")
        self.sendFileButton = QtWidgets.QPushButton(GP)
        self.sendFileButton.setGeometry(QtCore.QRect(550, 520, 101, 31))
        self.sendFileButton.setObjectName("sendFileButton")
        self.msgInput = QtWidgets.QLineEdit(GP)
        self.msgInput.setGeometry(QtCore.QRect(10, 520, 411, 31))
        self.msgInput.setObjectName("msgInput")
        self.retranslateUi(GP)
        QtCore.QMetaObject.connectSlotsByName(GP)
    def retranslateUi(self, GP):
        _translate = QtCore.QCoreApplication.translate
        GP.setWindowTitle(_translate("GP", "GhostProtocol - nRF24L01"))
        self.keyTitle.setText(_translate("GP", "Key Selection :"))
        self.usernameTitle.setText(_translate("GP", "Username :"))
        self.portTitle.setText(_translate("GP", "COM Port :"))
        self.keySelectionBox.setPlaceholderText(_translate("GP", "--- Key Files ---"))
        self.portSelectionBox.setPlaceholderText(_translate("GP", "--- Ports ---"))
        self.RXCheckBox.setText(_translate("GP", "RECEIVING"))
        self.IDLECheckBox.setText(_translate("GP", "IDLE"))
        self.INITCheckBox.setText(_translate("GP", "INIT"))
        self.deviceModeTitle.setText(_translate("GP", "Device Mode :"))
        self.TXCheckBox.setText(_translate("GP", "TRANSMITTING"))
        self.initializeModule.setText(_translate("GP", "Initialize The Module"))
        self.sendMsgButton.setText(_translate("GP", "Send Message"))
        self.sendFileButton.setText(_translate("GP", "Send File"))
        self.usernameInput.setPlaceholderText(_translate("GP", "Enter Username Here"))
        self.terminalBox.setReadOnly(True)
        self.messages.setReadOnly(True)
        self.msgInput.setEnabled(False)
        self.sendFileButton.setEnabled(False)
        self.sendMsgButton.setEnabled(False)
        self.initializeModule.setEnabled(False)
        self.usernameInput.setMaxLength(5)
        self.info_color = "#FFD801"
        self.warning_color = "#ED2939"
        self.success_color = "#FF4CAF50"
        self.chat_time_color = "#D3D3D3"
        self.chat_user_color = "#F6F6F6"
        self.chat_root_color = "#5B9EFE"
        self.IDLECheckBox.setProperty("color", "idle")
        self.TXCheckBox.setProperty("color", "txrx")
        self.RXCheckBox.setProperty("color", "txrx")
        self.INITCheckBox.setProperty("color", "init")
        self.afterburn()   
    def afterburn(self):
        self.terminalUpdate("Terminal started!", "SUCCESS")
        self.selectMode("INIT")
        QtCore.QCoreApplication.processEvents()
        self.keyLister()
        self.portLister()
        self.connections()
    def connections(self):
        self.keySelectionBox.currentTextChanged.connect(self.keyInfoMeta)
        self.portSelectionBox.currentTextChanged.connect(self.portInfoMeta)
        self.usernameInput.textChanged.connect(self.usernameMeta)
        self.usernameInput.returnPressed.connect(self.usernameInputEnter)
        self.initializeModule.clicked.connect(self.initModule)
        self.msgInput.returnPressed.connect(self.sendMessage)
        self.sendMsgButton.clicked.connect(self.sendMessage)
    def initModule(self):
        self.initializeModule.setEnabled(False)
        self.usernameInput.setEnabled(False)
        self.moduleConfig(self.comPort, self.username, self.keyNumber, "AX45-S") 
        
        if self.moduleInit() == True:
            self.msgInput.setEnabled(True)
            self.sendMsgButton.setEnabled(True)
            self.initializeModule.setEnabled(False)
            self.keySelectionBox.setEnabled(False)
            self.portSelectionBox.setEnabled(False)
            self.usernameInput.setEnabled(False)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.recvMessage)
            self.timer.start(10)
            #self.recvMessage()       
        else: 
            self.initializeModule.setEnabled(True)
            self.keySelectionBox.setEnabled(True)
            self.portSelectionBox.setEnabled(True)
            self.usernameInput.setEnabled(True)           
    def usernameInputEnter(self):
        if self.portSelectionBox.currentText != "" and self.keySelectionBox.currentText != "" and self.usernameInput.text() != "": self.initModule()
    def usernameMeta(self):
        self.username = self.usernameInput.text()
        self.usernameInput.setText(self.username.upper())
        self.initButtonCheck()
    def keyInfoMeta(self):
        if self.keySelectionBox.currentText() != "":
            self.keyNumber = int(self.keySelectionBox.currentText().replace("key","").replace(".ax",""))
            self.initButtonCheck()
    def portInfoMeta(self):
        if self.portSelectionBox.currentText() != "":
            self.comPort = self.portSelectionBox.currentText()
            self.initButtonCheck()
    def selectMode(self, deviceMode):
        
        self.TXCheckBox.setEnabled(True)
        self.RXCheckBox.setEnabled(True)
        self.IDLECheckBox.setEnabled(True)
        self.INITCheckBox.setEnabled(True)
        
        self.TXCheckBox.setCheckable(False)
        self.RXCheckBox.setCheckable(False)
        self.IDLECheckBox.setCheckable(False)
        self.INITCheckBox.setCheckable(False)

        if deviceMode=="IDLE": 

            self.IDLECheckBox.setEnabled(False)
        elif deviceMode=="TX": 
            
            self.TXCheckBox.setEnabled(False)
        elif deviceMode=="RX": 
            
            self.RXCheckBox.setEnabled(False)
        elif deviceMode=="INIT": 
            
            self.INITCheckBox.setEnabled(False)
            
        else: pass

        QtCore.QCoreApplication.processEvents()
    def terminalUpdate(self,msg,status):
        if status ==      "INFO": self.terminalBox.insertHtml(f'<font color={self.chat_user_color}><strong>INFO :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "WARNING": self.terminalBox.insertHtml(f'<font color={self.info_color     }><strong>WARNING :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "SUCCESS": self.terminalBox.insertHtml(f'<font color={self.success_color  }><strong>SUCCESS :: </strong></font><font color="white">{msg}</font><br>')
        self.terminalBox.verticalScrollBar().setValue(self.terminalBox.verticalScrollBar().maximum())
    def keyLister(self):
        self.keySelectionBox.clear()   
        for i,key in enumerate(self.fileLister("KEY")):
            self.keySelectionBox.addItem("")
            self.keySelectionBox.setItemText(i, "key"+str(key)+".ax")
    def portLister(self):
        self.portSelectionBox.clear()   
        for i,port in enumerate(self.portChecker()):
            self.portSelectionBox.addItem("")
            self.portSelectionBox.setItemText(i, port)
    def portChecker(self):
        PORTS=[]
        for i in comports(): PORTS.append(str(i).split(" ")[0])
        return PORTS
    def alert(self,title,alert_msg):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(f"<p align='left'>{alert_msg}<br>")
        msg.setWindowIcon(QtGui.QIcon('files/alert.png'))
        with open("files/theme.qss",'r') as f: msg.setStyleSheet(f.read())
        msg.exec()
    def initButtonCheck(self):
        if self.keySelectionBox.currentText() != "" and self.portSelectionBox.currentText() != "" and self.usernameInput.text() != "": self.initializeModule.setEnabled(True)
        else: self.initializeModule.setEnabled(False)
    def timeChecker(self):
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)
        if len(minute) == 1: minute = "0"+minute
        elif len(minute) == 0 : minute = "00"
        if len(hour) == 1: hour = "0"+hour
        elif len(hour) == 0 : hour = "00"
        return hour+":"+minute
    def messageBoxUpdate(self, who, root_check, text):
            if root_check == False:
                self.messages.insertHtml(f'<font color={self.chat_time_color}>{self.timeChecker()}</font> <font color={self.chat_user_color}><strong><b>{who}</b></strong></font><font color="white"> > {text}</font><br>')
            elif root_check == True:
                self.messages.insertHtml(f'<font color={self.chat_time_color}>{self.timeChecker()}</font> <font color={self.chat_root_color}><strong><b>{who}</b></strong></font><font color="white"> > {text}</font><br>')
            self.messages.verticalScrollBar().setValue(self.messages.verticalScrollBar().maximum())
    def sendMessage(self):  
        self.selectMode("TX")
        
        if self.msgInput.text() != "" and len(self.msgInput.text()) != self.msgInput.text().count(" "):
            self.messageBoxUpdate(self.username, True, self.msgInput.text())
            s,f,t = self.msgTX(self.msgInput.text()).values()
            self.terminalUpdate("Message Has Been Transmitted", "INFO")
            self.terminalUpdate(f"S {s} | F {f} | Time Elapsed : {t:.2f}", "SUCCESS")
        
        self.msgInput.setText("")
        self.selectMode("IDLE")
    def recvMessage(self):
        msg = self.rx()
        if msg != None:
            try: self.messageBoxUpdate(msg["node"], False, msg["data"])
            except: pass  
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GP = QtWidgets.QWidget()
    ui = Ui_GP()
    ui.setupUi(GP)
    GP.show()
    sys.exit(app.exec())
