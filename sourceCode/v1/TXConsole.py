import sqlite3,random,time,serial.tools.list_ports,base64
db = sqlite3.connect('ghostprotocol.db')
cursor = db.cursor()
tx_id_count=1
rx_id_count=1


def photoToText(fileName):
    filePhoto=fileName+'.png'
    with open(filePhoto, 'rb') as imageFile:
        str = base64.b64encode(imageFile.read()).decode('utf-8')
    return str

def textToPhoto(photoTextRaw):
    with open(filePhoto, 'wb') as fh:
        fh.write(base64.decodebytes(photoTextRaw.encode('utf-8')))

def afterburner():
    cursor.execute("CREATE TABLE IF NOT EXISTS tx(tx_id,msg,confirm)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rx(rx_id,msg)")
    cursor.execute("CREATE TABLE IF NOT EXISTS conf(settings)")
    db.commit()
    cursor.execute("DROP table tx")
    cursor.execute("DROP table rx")
    cursor.execute("DROP table conf")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS tx(tx_id,msg,confirm)")
    cursor.execute("CREATE TABLE IF NOT EXISTS rx(rx_id,msg)")
    cursor.execute("CREATE TABLE IF NOT EXISTS conf(settings)")
    db.commit()
def dataView():
    cursor.execute("SELECT msg FROM tx;")
    datacache=cursor.fetchall()
    for data in datacache:
        print(data)
    datacache=[]
def confRegister(node,com,key):
    cursor.execute("""INSERT INTO conf VALUES ('{}')""".format(node))
    cursor.execute("""INSERT INTO conf VALUES ('{}')""".format(com))
    cursor.execute("""INSERT INTO conf VALUES ('{}')""".format(key))
    db.commit()
def txRegister(tx_id,msg,confirm):
    cursor.execute("""INSERT INTO tx VALUES ({},'{}','{}')""".format(tx_id,msg,confirm))
    db.commit()
def dataComplier(raw):
    raw=raw.replace("ı","i")
    raw=raw.replace("ö","o")
    raw=raw.replace("ğ","g")
    raw=raw.replace("ü","u")
    raw=raw.replace("ç","c")
    raw=raw.replace("ş","s")
    raw=raw.replace("İ","I")
    raw=raw.replace("Ö","O")
    raw=raw.replace("Ü","U")
    raw=raw.replace("Ğ","G")
    raw=raw.replace("Ç","C")
    raw=raw.replace("Ş","S")
    return raw

PORTS=[]
for i in serial.tools.list_ports.comports():
    PORTS.append(str(i).split(" ")[0])
for i in range(0,len(PORTS)):
    print(str(i+1)+"-) "+PORTS[i])
i = input("Select COM Port : ")
COM=PORTS[int(i)-1]
NODE = input("Select NODE Name : ")
if NODE=="NULL":
    NODE = input("NULL cannot be selected please enter another NODE Name : ")
KEY=237415

afterburner()
confRegister(NODE,COM,KEY)

while True:
    dataTX=dataComplier(input("Data to TX : "))

    if dataTX=="exit":
        break

    elif dataTX[:8]=="img_send":

        dataTXimg=dataTX.split("=")
        txRegister(tx_id_count,photoToText(dataTXimg[1]),"negative")
        tx_id_count+=1

    else:
        txRegister(tx_id_count,dataTX,"negative")
        tx_id_count+=1

dataView()
db.close()
