import curses,time,random,serial,sqlite3
from ax45sEngine.algorithms import axen,axde

banner1 = [
"       ________               __     ____             __                   __         "
,"      / ____/ /_  ____  _____/ /_   / __ \_________  / /_____  _________  / /         "
,"     / / __/ __ \/ __ \/ ___/ __/  / /_/ / ___/ __ \/ __/ __ \/ ___/ __ \/ /          "
,"    / /_/ / / / / /_/ (__  ) /_   / ____/ /  / /_/ / /_/ /_/ / /__/ /_/ / /           "
,"    \____/_/ /_/\____/____/\__/  /_/   /_/   \____/\__/\____/\___/\____/_/            "
,"                                                                                      "
,"             GProtocol Main Framework & Powered by AX45-S Algorithm                   "]
banner2 = [
"       _  ___ _               __     _  _             __                   __         "
,"         / ____/ /_  ____  _____/ /_   / __ \_________  / /_____  ____  ___  / /         "
,"   / / __/ __ \/ __ \  ___/ __/  / /_/ / ___/ __ \/ __/ __ \/ ___/ __ \/ /          "
,"      / /_/ / / / / /_/ (__  ) /_   / ____/ /  / /_/ / /_  /_/ / /__/ /_/ / /           "
,"  \____/_/ /_/\_ __/____/\__/  /_/   /_/   \__ _/\__/\____/\___/\____/_/             "
,"                                                                                      "
,"             GProtocol Main Framework & Powered by AX45-S Algorithm                   "]


def module_config():
    global db
    global cursor
    global COM
    global NODE
    global KEY
    global so
    global se
    global BAUD
    global datasize
    global PORTS
    global NODE_CACHE
    global MODE
    global datasets_de
    global dataset_de
    global PACKAGE_QUE
    PACKAGE_QUE=0
    BAUD=115200
    datasize=0
    NODE_CACHE="NULL"
    MODE="IDLE"
    datasets_de=[]
    dataset_de=""
    so="STREAM-ORIGIN"
    se="STREAM-END"

    db = sqlite3.connect('ghostprotocol.db')
    cursor = db.cursor()

    def convertTuple(tup):
        str = ''
        for item in tup:
            str = str + item
        return str

    cursor.execute("SELECT settings FROM conf;")
    datacache=cursor.fetchall()
    NODE=convertTuple(datacache[0])
    COM=convertTuple(datacache[1])
    KEY=int(convertTuple(datacache[2]))
    datacache=[]
def main(scr):


    def startup():
        global ser
        global h
        global w

        ser = serial.Serial(COM,BAUD)
        curses.curs_set(0)
        h,w = scr.getmaxyx()



        for x in range(0,len(banner1)):
            scr.addstr(h//8-len(banner2)//2+x,        w//2-len(banner2[6])//2,        banner1[x])
        curses.wrapper(data)
        scr.refresh()
        time.sleep(0.8)
        scr.clear()
        for x in range(0,len(banner2)):
            scr.addstr(h//8-len(banner2)//2+x,        w//2-len(banner2[6])//2,        banner2[x])
        curses.wrapper(data)
        scr.refresh()
        time.sleep(0.2)
        scr.clear()
        for x in range(0,len(banner1)):
            scr.addstr(h//8-len(banner2)//2+x,        w//2-len(banner2[6])//2,        banner1[x])
        curses.wrapper(data)
        scr.refresh()
        time.sleep(0.8)
    def data(fall):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        begin_x = w-w//2 ; begin_y = h//4
        height = 37 ; width = w//2-4
        fall = curses.newwin(height, width, begin_y, begin_x)
        fall.box()
        fall.attron(curses.color_pair(1))
        fall.addstr(0,2," Data Fall ")
        fall.attroff(curses.color_pair(1))
        fall.attron(curses.color_pair(2))
        fall.addstr(0,width-5," X ")
        fall.attroff(curses.color_pair(2))
        fall.refresh()
        begin_xf = w//32 ; begin_yf = h//4
        heightf = 28 ; widthf = w//2-4
        win = curses.newwin(heightf, widthf, begin_yf, begin_xf)
        win.box()
        win.attron(curses.color_pair(1))
        win.addstr(0,2," Terminal ")
        win.attroff(curses.color_pair(1))
        win.attron(curses.color_pair(2))
        win.addstr(0,widthf-5," X ")
        win.attroff(curses.color_pair(2))
        win.addstr(2,2,"gate@root:~ Connecting to Serial "+COM+"...")
        win.refresh()
        begin_xz = w//32 ; begin_yz = h//4+28
        heightz = 9 ; widthz = w//2-4

        sendbox = curses.newwin(heightz, widthz, begin_yz, begin_xz)
        sendbox.box()
        sendbox.refresh()
        sendbox.attron(curses.color_pair(1))
        sendbox.addstr(0,2," SendBox ")
        sendbox.attroff(curses.color_pair(1))
        sendbox.attron(curses.color_pair(2))
        sendbox.addstr(0,widthf-5," X ")
        sendbox.attroff(curses.color_pair(2))
        sendbox.attron(curses.color_pair(2))
        sendbox.addstr(0,widthf-5," X ")
        sendbox.attroff(curses.color_pair(2))
        sendbox.addstr(0,12," TX [")
        sendbox.attron(curses.color_pair(2))
        sendbox.addstr(0,17,"■")
        sendbox.attroff(curses.color_pair(2))
        sendbox.addstr(0,18,"] RX [")
        sendbox.attron(curses.color_pair(2))
        sendbox.addstr(0,24,"■")
        sendbox.attroff(curses.color_pair(2))
        sendbox.addstr(0,25,"] ")
        sendbox.refresh()
    def main(data):

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        begin_x = w-w//2+2 ; begin_y = h//4+2
        height = 33 ; width = w//2-8
        data = curses.newwin(height, width, begin_y, begin_x)

        begin_xf = w//32 ; begin_yf = h//4
        heightf = 28 ; widthf = w//2-4
        win = curses.newwin(heightf, widthf, begin_yf, begin_xf)

        begin_xz = w//32 ; begin_yz = h//4+28
        heightz = 9 ; widthz = w//2-4
        sendbox = curses.newwin(heightz, widthz, begin_yz, begin_xz)

        win.box()
        win.attron(curses.color_pair(1))
        win.addstr(0,2," Terminal ")
        win.attroff(curses.color_pair(1))
        win.attron(curses.color_pair(2))
        win.addstr(0,widthf-5," X ")
        win.attroff(curses.color_pair(2))
        win.refresh()

        data_fallscreen=[]
        command_fall_screen=[]
        command_fall_screen.append("gate@root:~ Connecting to Serial "+COM+"...")
        command_fall_screen.append("gate@root:~ Serial Connection Success")
        command_fall_screen.append("gate@root:~ Transferring to data fall screen...")

        def photoToText(fileName):
            filePhoto=fileName+'.png'
            with open(filePhoto, 'rb') as imageFile:
                str = base64.b64encode(imageFile.read()).decode('utf-8')
            return str
        def textToPhoto(photoTextRaw):
            with open(filePhoto, 'wb') as fh:
                fh.write(base64.decodebytes(photoTextRaw.encode('utf-8')))
        def convertTuple(tup):
            str = ''
            for item in tup:
                str = str + item
            return str
        def newMessageCheck():
            cursor.execute("SELECT confirm FROM tx;")
            SQL_STAT_CHECK_TUP=cursor.fetchall()
            SQL_STAT_CHECK_STR=[]
            for TUP_STAT in SQL_STAT_CHECK_TUP:
                SQL_STAT_CHECK_STR.append(convertTuple(TUP_STAT))
            NEGATIVE_COUNT=SQL_STAT_CHECK_STR.count("negative")
            return NEGATIVE_COUNT
        def TX(DATA,NODE):
            def gtx(data):
                global KEY
                global NODE
                global COM
                global BAUD
                error_value=False
                n = 28 #packet size
                datasets=axen(data,KEY)
                datasets = [datasets[i:i+n] for i in range(0, len(datasets), n)]
                command_fall_screen.append("gate@root:~ "+str(len(datasets))+" Package Stacked")
                command_fall_screen.append("gate@root:~ Switching to TX Mode")

                tx_start="STREAM-ORIGIN+"+str(len(data))+"+"+NODE+"\r\n"
                ser.write(tx_start.encode())
                readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+tx_start[:-2])
                win_call()
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        ser.write(tx_start.encode())
                        readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                        command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+tx_start[:-2])
                        win_call()
                        if readline=="code[200]":
                            error_value=False


                for x in range(0,len(datasets)):
                    sendbox_call("TX",len(datasets)-x)
                    data=datasets[x]+"\r\n"
                    ser.write(data.encode())
                    readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                    command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+data[:-2])
                    win_call()
                    if readline=="code[417]":
                        error_value=True
                        while error_value==True:
                            ser.write(data.encode())
                            readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                            command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+data[:-2])
                            win_call()
                            if readline=="code[200]":
                                error_value=False


                tx_stop="STREAM-END\r\n"
                ser.write(tx_stop.encode())
                readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+tx_stop[:-2])
                win_call()
                if readline=="code[417]":
                    error_value=True
                    while error_value==True:
                        ser.write(data.encode())
                        readline=ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                        command_fall_screen.append("nrf24l01@root:~ "+readline+" DataTX ----> "+tx_stop[:-2])
                        win_call()
                        if readline=="code[200]":
                            error_value=False


                command_fall_screen.append("gate@root:~ Switching to RX Mode")
            data_call(NODE,DATA)
            win_call()
            sendbox_call("TX",PACKAGE_QUE)
            gtx(DATA)
            win_call()
            sendbox_call("RX",PACKAGE_QUE)
        def RX():
            win_call()
            sendbox_call("RX",PACKAGE_QUE)
            if (ser.inWaiting()>0):
                datasets_de=[]
                dataset_de=""
                global NODE_CACHE
                global MODE
                datasize=0
                a = ser.readline()[:-2].decode('utf-8', errors='replace').rstrip("\x00").rstrip("\r")
                if a[:13]==so:
                    datasize=a.split("+")[1]
                    NODE_CACHE=a.split("+")[2]
                    cont=True
                    datasets_de.append(a)
                    command_fall_screen.append("gate@root:~ Stream Origin Has Been Found")
                    command_fall_screen.append("gate@root:~ Data Queue Tracking...")
                    command_fall_screen.append("nrf24l01@root:~ code[200] DataRX ----> "+a)
                    win_call()

                    while cont==True:
                        a = ser.readline()[:-2].decode().rstrip("\x00").rstrip("\r")
                        if a==datasets_de[-1]:
                            pass
                        else:
                            datasets_de.append(a)
                            command_fall_screen.append("nrf24l01@root:~ code[200] DataRX ----> "+a)
                            win_call()
                        if a[:10]==se:
                            cont=False

                for x in range(1,len(datasets_de)-1):
                    dataset_de=dataset_de+datasets_de[x]
                dataset_de=axde(dataset_de,KEY)

                if (len(dataset_de)==int(datasize)) and (datasize != 0) and (NODE_CACHE!="NULL"):
                    command_fall_screen.append("gate@root:~ Transmit Succes No Packet Loss")

                    data_call(NODE_CACHE,dataset_de)
                    win_call()

                else:
                    command_fall_screen.append("gate@root:~ Packet loss")
                    win_call()
            else:
                pass

            win_call()
            sendbox_call("RX",PACKAGE_QUE)
        def win_call():
            win.clear()
            win.box()
            win.attron(curses.color_pair(1))
            win.addstr(0,2," Terminal ")
            win.attroff(curses.color_pair(1))
            win.attron(curses.color_pair(2))
            win.addstr(0,widthf-5," X ")
            win.attroff(curses.color_pair(2))

            def printlines():

                for y in range(0,len(command_fall_screen)):

                    if str(command_fall_screen[y])[-15:]=="Package Stacked":
                        win.addstr(y+2,2,str(command_fall_screen[y])[:11], curses.A_BOLD)
                        win.attron(curses.color_pair(3))
                        win.addstr(y+2,14,str(command_fall_screen[y])[12:])
                        win.attroff(curses.color_pair(3))

                    elif str(command_fall_screen[y])[-20:]=="Switching to TX Mode":
                        win.addstr(y+2,2,str(command_fall_screen[y])[:11], curses.A_BOLD)
                        win.attron(curses.color_pair(4))
                        win.addstr(y+2,14,str(command_fall_screen[y])[-20:])
                        win.attroff(curses.color_pair(4))

                    elif str(command_fall_screen[y])[-20:]=="Switching to RX Mode":
                        win.addstr(y+2,2,str(command_fall_screen[y])[:11], curses.A_BOLD)
                        win.attron(curses.color_pair(4))
                        win.addstr(y+2,14,str(command_fall_screen[y])[-20:])
                        win.attroff(curses.color_pair(4))

                    elif str(command_fall_screen[y])[-22:]=="Switching to IDLE Mode":
                        win.addstr(y+2,2,str(command_fall_screen[y])[:11], curses.A_BOLD)
                        win.attron(curses.color_pair(4))
                        win.addstr(y+2,14,str(command_fall_screen[y])[-22:])
                        win.attroff(curses.color_pair(4))

                    elif str(command_fall_screen[y])[:25]=="nrf24l01@root:~ code[417]":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(5))
                        win.addstr(y+2,18,str("code[417]"))
                        win.attroff(curses.color_pair(5))

                    elif str(command_fall_screen[y])[:25]=="nrf24l01@root:~ code[200]":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(6))
                        win.addstr(y+2,18,str("code[200]"))
                        win.attroff(curses.color_pair(6))

                    elif str(command_fall_screen[y])[-30:]=="Transmit Succes No Packet Loss":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(4))
                        win.addstr(y+2,14,str("Transmit Succes No Packet Loss"))
                        win.attroff(curses.color_pair(4))

                    elif str(command_fall_screen[y])[-28:]=="Stream Origin Has Been Found":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(7))
                        win.addstr(y+2,14,str("Stream Origin Has Been Found"))
                        win.attroff(curses.color_pair(7))

                    elif str(command_fall_screen[y])[-22:]=="Data Queue Tracking...":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(7))
                        win.addstr(y+2,14,str("Data Queue Tracking..."))
                        win.attroff(curses.color_pair(7))

                    elif str(command_fall_screen[y])[-11:]=="Packet loss":
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)
                        win.attron(curses.color_pair(2))
                        win.addstr(y+2,14,str("Packet loss"))
                        win.attroff(curses.color_pair(2))

                    else:
                        win.addstr(y+2,2,str(command_fall_screen[y]), curses.A_BOLD)

            if len(command_fall_screen)<=24:
                printlines()
            if len(command_fall_screen)>24:
                while len(command_fall_screen)>24:
                    del command_fall_screen[0]
                printlines()

            win.refresh()
        def data_call(NODE,DATA):
            data.clear()
            if len(data_fallscreen)>=1:
                data_fallscreen.append(" ")
            t=68
            DATA=NODE+" -> "+DATA
            line = [DATA[i:i+t] for i in range(0, len(DATA), t)]
            for loop in range(0,len(line)):
                data_fallscreen.append(line[loop])
            if len(data_fallscreen)<=33:
                for x in range(0,len(data_fallscreen)):
                    data.addstr(x,0,str(data_fallscreen[x]))
                data.refresh()
            if len(data_fallscreen)>33:
                while len(data_fallscreen)>33:
                    del data_fallscreen[0]
                for x in range(0,len(data_fallscreen)):
                    data.addstr(x,0,str(data_fallscreen[x]))
                data.refresh()
        def sendbox_call(MODULE_STATUS,PACKAGE_QUE):
            sendbox.clear()
            sendbox.box()
            sendbox.attron(curses.color_pair(1))
            sendbox.addstr(0,2," SendBox ")
            sendbox.attroff(curses.color_pair(1))
            sendbox.attron(curses.color_pair(2))
            sendbox.addstr(0,widthf-5," X ")
            sendbox.attroff(curses.color_pair(2))

            if MODULE_STATUS=="TX":
                    sendbox.addstr(0,12," TX [")
                    sendbox.attron(curses.color_pair(1))
                    sendbox.addstr(0,17,"■")
                    sendbox.attroff(curses.color_pair(1))
                    sendbox.addstr(0,18,"] RX [")
                    sendbox.attron(curses.color_pair(2))
                    sendbox.addstr(0,24,"■")
                    sendbox.attroff(curses.color_pair(2))
                    sendbox.addstr(0,25,"] ")
                    sendbox.addstr(2,2,str(" [+] Module Transmiting Datasets to Channel..."))
            if MODULE_STATUS=="RX":
                    sendbox.addstr(0,12," TX [")
                    sendbox.attron(curses.color_pair(2))
                    sendbox.addstr(0,17,"■")
                    sendbox.attroff(curses.color_pair(2))
                    sendbox.addstr(0,18,"] RX [")
                    sendbox.attron(curses.color_pair(1))
                    sendbox.addstr(0,24,"■")
                    sendbox.attroff(curses.color_pair(1))
                    sendbox.addstr(0,25,"] ")
                    sendbox.addstr(2,2,str(" [+] Module Searching Channel For Any Signal..."))
            if MODULE_STATUS=="IDLE":
                    sendbox.addstr(0,12," TX [")
                    sendbox.attron(curses.color_pair(2))
                    sendbox.addstr(0,17,"■")
                    sendbox.attroff(curses.color_pair(2))
                    sendbox.addstr(0,18,"] RX [")
                    sendbox.attron(curses.color_pair(2))
                    sendbox.addstr(0,24,"■")
                    sendbox.attroff(curses.color_pair(2))
                    sendbox.addstr(0,25,"] ")

            sendbox.addstr(3,2,str(" [+] "+str(PACKAGE_QUE)+" Packet(s) Waiting for Data Transfer"))

            sendbox.addstr(6,2,str(" [Node: "+NODE+" / Port: "+COM+" / Baud Rate: "+str(BAUD)+" / KEY: key"+str(KEY)+".ax]"))
            sendbox.refresh()

        win_call()
        MODE="RX"
        tx_id_count=0

        while True:
            if newMessageCheck()>=1:
                cursor.execute("SELECT msg,confirm FROM tx;")
                SQL_TX_DATA=cursor.fetchall()
                for x in range(0,len(SQL_TX_DATA)):
                    if SQL_TX_DATA[x][1]=="negative":
                        cursor.execute('Update tx set confirm ="{}" where tx_id = {}'.format("positive",x+1))
                        DATA=convertTuple(SQL_TX_DATA[x][0])
                        MODE="TX"
                        db.commit()
                        break
            if MODE=="IDLE":
                pass
            elif MODE=="TX":
                TX(DATA,NODE)
                MODE="RX"
            elif MODE=="RX":
                RX()

    startup()
    curses.wrapper(data)
    curses.wrapper(main)
    curses.wrapper(sendbox)

module_config()
curses.wrapper(main)
