import paho.mqtt.client as mqtt
import sqlite3
import time
db = sqlite3.connect('TEST.db')
cursor=db.cursor()
onmessagestatus=False
msgtopic=""
msgpayload=""
# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    client.subscribe("/rc522/A0")
    client.subscribe("/IEYI/hrjh/search/send")
    client.subscribe("/IEYI/hrjh/check/getlist")
    client.subscribe("/IEYI/hrjh/check/getUID")
    client.subscribe("/IEYI/hrjh/aram/lib/danger")

# 接收訊息（接收到 PUBLISH）的回呼函數
def on_message(client, userdata, msg):
    print(type(msg))
    print(type(msg.topic))
    print(type(msg.payload))
    global msgtopic
    global msgpayload
    msgtopic=str(msg.topic)
    msgpayload=str(msg.payload.decode('utf-8'))
    global onmessagestatus
    onmessagestatus=True
    """if(msg.topic=="/rc522/A0"):
        #print("[{}]: {}".format(msg.topic, str(msg.payload)))
        getUID=str(msg.payload)[2:8]
        getaddr=str(msg.payload)[-3:-1]
        
        #get data of No
        a="SELECT NO FROM DATA WHERE UID='%s';"%(getUID)
        cursor.fetchall()
        cursor.execute(a)
        getNo=int(list(cursor.fetchone())[0])

        #get data of last in No and change secondlast to last
        # a="SELECT LAST FROM DATA WHERE NO=%d;"%(getNo)
        # cursor.fetchall()
        # cursor.execute(a)
        # lasttemp=list(cursor.fetchone())[0]
        # a="UPDATE DATA SET SECONDLAST='%s' WHERE NO=%d;"%(lasttemp,getNo)
        # cursor.execute(a)

        #change location to getaddr
        a="UPDATE DATA SET LOCATION='%s' WHERE NO=%d;"%(getaddr,getNo)
        cursor.fetchall()
        cursor.execute(a)
        db.commit()


        a="SELECT TYPE FROM DATA WHERE NO=%d;"%(getNo)
        cursor.fetchall()
        cursor.execute(a)
        gettype=list(cursor.fetchone())[0]
        if(gettype==1 and getaddr=="OH"):
            #發送失智警報
            a="SELECT * FROM DATA WHERE NO='%s'"%(getNo)
            cursor.fetchall()
            cursor.execute(a)
            xs=list(cursor.fetchone())
            s = ' '.join(str(x) for x in xs)
            
            client.publish("/IEYI/hrjh/aram/search/dementia", str(s))
        if(getaddr=="NS" or getaddr=="EL"):
            #禁區警報
            a="SELECT * FROM DATA WHERE NO='%s'"%(getNo)
            cursor.fetchall()
            cursor.execute(a)
            xs=list(cursor.fetchone())
            s = ' '.join(str(x) for x in xs)
            
            client.publish("/IEYI/hrjh/aram/search/danger", str(s))

        #change lastTime to gettime
        a="UPDATE DATA SET LASTTIME='%s' WHERE NO=%d;"%(int(time.time()),getNo)
        cursor.fetchall()
        cursor.execute(a)
        db.commit()

        #save lib
    elif(msg.topic=="/IEYI/hrjh/search/send"):
        print("即將回傳查詢結果")
        searchget=str(msg.payload)[2:-1]
        a="SELECT * FROM DATA WHERE BEDNO='%s'"%(searchget)
        cursor.fetchall()
        cursor.execute(a)
        xs=list(cursor.fetchone())
        s = ' '.join(str(x) for x in xs)
        client.publish("/IEYI/hrjh/search/return", str(s))
    # elif(msg.topic=="/IEYI/hrjh/aram/lib/danger"):
    #     searchget=str(msg.payload)[2:-1]
    #     a="SELECT * FROM DATA WHERE UID='%s'"%(searchget)
    #     cursor.fetchall()
    #     cursor.execute(a)
    #     xs=list(cursor.fetchone())
    #     s = ' '.join(str(x) for x in xs)
        
    #     client.publish("/IEYI/hrjh/aram/search/danger", str(s))
    elif(msg.topic=="/IEYI/hrjh/check/getlist"):
        a="SELECT NAME FROM DATA"
        cursor.fetchall()
        cursor.execute(a)
        client.publish("IEYI/hrjh/check/returnlist",list(cursor.fetchall()))
    elif(msg.topic=="/IEYI/hrjh/check/getUID"):
        a="SELECT UID FROM DATA WHERE NAME='%s'"%(str(msg.payload)[2:-1])
        cursor.fetchall()
        cursor.execute(a)
        client.publish("IEYI/hrjh/check/returnUID",str(list(cursor.fetchone())[0]))
"""
# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定建立連線回呼函數
client.on_connect = on_connect

# 設定接收訊息回呼函數
client.on_message = on_message

# 設定登入帳號密碼（若無則可省略）
client.username_pw_set("","")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("192.168.1.87", 1883)

# 進入無窮處理迴圈
client.loop_start()

while True:
    atime="SELECT LASTTIME, LOCATION, ID FROM DATA"
    cursor.fetchall()
    cursor.execute(atime)
    timelist=cursor.fetchall()
    count=0
    for i in timelist:
        #print(timelist[count])
        if(timelist[count][1]=="廁所"):
            if((int(time.time())-timelist[count][0])>5):
                atime="SELECT * FROM DATA WHERE ID='%s'"%(timelist[count][2])
                cursor.fetchall()
                cursor.execute(atime)
                xs=list(cursor.fetchone())
                s = ' '.join(str(x) for x in xs)
                print(s)
                client.publish("/IEYI/hrjh/aram/search/time", str(s))
                atime="UPDATE DATA SET LASTTIME=%d WHERE ID='%s'"%(int(time.time()),timelist[count][2])
                cursor.fetchall()
                cursor.execute(atime)
                db.commit()
                print(timelist[count])
                atime="UPDATE DATA SET LOCATION='廁所!' WHERE ID='%s'"%(timelist[count][2])
                cursor.fetchall()
                cursor.execute(atime)
                db.commit()
        count+=1
    if(onmessagestatus==True):
        onmessagestatus=False
        if(msgtopic=="/rc522/A0"):
            #print("[{}]: {}".format(msg.topic, str(msg.payload)))
            print("有人通過")
            getUID=msgpayload.split()[0][0:5]
            print(msgpayload)
            getaddr=msgpayload.split()[2]
            print(getUID)
            
            #get data of No
            a="SELECT NO FROM DATA WHERE UID='%s';"%(getUID)
            cursor.fetchall()
            cursor.execute(a)
            getNo=int(list(cursor.fetchone())[0])

            #get data of last in No and change secondlast to last
            # a="SELECT LAST FROM DATA WHERE NO=%d;"%(getNo)
            # cursor.fetchall()
            # cursor.execute(a)
            # lasttemp=list(cursor.fetchone())[0]
            # a="UPDATE DATA SET SECONDLAST='%s' WHERE NO=%d;"%(lasttemp,getNo)
            # cursor.execute(a)

            #change location to getaddr
            a="UPDATE DATA SET LOCATION='%s' WHERE NO=%d;"%(getaddr,getNo)
            cursor.fetchall()
            cursor.execute(a)
            db.commit()


            a="SELECT TYPE FROM DATA WHERE NO=%d;"%(getNo)
            cursor.fetchall()
            cursor.execute(a)
            gettype=list(cursor.fetchone())[0]
            if(gettype==1 and getaddr=="醫院外"):
                #發送失智警報
                a="SELECT * FROM DATA WHERE NO='%s'"%(getNo)
                cursor.fetchall()
                cursor.execute(a)
                xs=list(cursor.fetchone())
                s = ' '.join(str(x) for x in xs)
                
                client.publish("/IEYI/hrjh/aram/search/dementia", str(s))
                a="SELECT LOCATION FROM DATA WHERE UID='%s'"%(getUID)
                cursor.fetchall()
                cursor.execute(a)
                a="UPDATE DATA SET LOCATION='%s' WHERE UID='%s'"%(str(list(cursor.fetchone())[0])+"!",getUID)
                cursor.execute(a)
                db.commit()
            
            if(getaddr=="護理站" or getaddr=="逃生梯"):
                #禁區警報
                a="SELECT * FROM DATA WHERE NO='%s'"%(getNo)
                cursor.fetchall()
                cursor.execute(a)
                xs=list(cursor.fetchone())
                s = ' '.join(str(x) for x in xs)
                
                client.publish("/IEYI/hrjh/aram/search/danger", str(s))
                a="SELECT LOCATION FROM DATA WHERE UID='%s'"%(getUID)
                cursor.fetchall()
                cursor.execute(a)
                a="UPDATE DATA SET LOCATION='%s' WHERE UID='%s'"%(str(list(cursor.fetchone())[0])+"!",getUID)
                cursor.execute(a)
                db.commit()

            #change lastTime to gettime
            a="UPDATE DATA SET LASTTIME='%s' WHERE NO=%d;"%(int(time.time()),getNo)
            cursor.fetchall()
            cursor.execute(a)
            db.commit()

            #save lib
        elif(msgtopic=="/IEYI/hrjh/search/send"):
            print("即將回傳查詢結果")
            searchget=str(msgpayload)
            print(msgpayload)
            print(searchget)
            a="SELECT * FROM DATA WHERE BEDNO='%s'"%(searchget)
            cursor.fetchall()
            cursor.execute(a)
            try:
                xs=list(cursor.fetchone())
                s = ' '.join(str(x) for x in xs)
                client.publish("/IEYI/hrjh/search/return", str(s))
            except:
                pass
        # elif(msgtopic=="/IEYI/hrjh/aram/lib/danger"):
        #     searchget=str(msgpayload)[2:-1]
        #     a="SELECT * FROM DATA WHERE UID='%s'"%(searchget)
        #     cursor.fetchall()
        #     cursor.execute(a)
        #     xs=list(cursor.fetchone())
        #     s = ' '.join(str(x) for x in xs)
        #     client.publish("/IEYI/hrjh/aram/search/danger", str(s))

        #     a="SELECT LOCATION FROM DATA WHERE UID='%s'"%(searchget)
        #     cursor.fetchall()
        #     cursor.execute(a)
        #     a="UPDATE DATA SET LOCATION='%s' WHERE UID='%s'"%(str(list(cursor.fetchone)[0])+"!",searchget)
        #     cursor.execute(a)
        #     db.commit()
        # elif(msgtopic=="/IEYI/hrjh/check/getlist"):
        #     a="SELECT NAME FROM DATA"
        #     cursor.fetchall()
        #     cursor.execute(a)
        #     client.publish("IEYI/hrjh/check/returnlist",list(cursor.fetchall()))
        # elif(msgtopic=="/IEYI/hrjh/check/getUID"):
        #     a="SELECT UID FROM DATA WHERE NAME='%s'"%(str(msgpayload)[2:-1])
        #     cursor.fetchall()
        #     cursor.execute(a)
        #     client.publish("IEYI/hrjh/check/returnUID",str(list(cursor.fetchone())[0]))
    