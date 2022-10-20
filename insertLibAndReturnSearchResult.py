import paho.mqtt.client as mqtt
import sqlite3
db = sqlite3.connect('TEST.db')
cursor=db.cursor()
# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    client.subscribe("rc522/A0")
    client.subscribe("/IEYI/hrjh/search/send")


# 接收訊息（接收到 PUBLISH）的回呼函數
def on_message(client, userdata, msg):
    if(msg.topic=="/rc522/A0"):
        #print("[{}]: {}".format(msg.topic, str(msg.payload)))
        getaddr=str(msg.payload)[2:4]
        gettime=str(msg.payload)[4:-15]
        getUID=str(msg.payload)[-15:-1]
        #get data of No
        a="SELECT NO FROM DATA WHERE UID='%s';"%(getUID)
        cursor.execute(a)
        getNo=int(list(cursor.fetchone())[0])

        #get data of last in No and change secondlast to last
        a="SELECT LAST FROM DATA WHERE NO=%d;"%(getNo)
        cursor.execute(a)
        lasttemp=list(cursor.fetchone())[0]
        a="UPDATE DATA SET SECONDLAST='%s' WHERE NO=%d;"%(lasttemp,getNo)
        cursor.execute(a)

        #change last to getaddr
        a="UPDATE DATA SET LAST='%s' WHERE NO=%d;"%(getaddr,getNo)
        cursor.execute(a)

        #get data of lastTime in No and change secondlastTime to lastTime
        a="SELECT LASTTIME FROM DATA WHERE NO=%d;"%(getNo)
        cursor.execute(a)
        lasttimetemp=list(cursor.fetchone())[0]
        a="UPDATE DATA SET SECONDLASTTIME='%s' WHERE NO=%d;"%(lasttimetemp,getNo)
        cursor.execute(a)

        #change lastTime to gettime
        a="UPDATE DATA SET LASTTIME='%s' WHERE NO=%d;"%(gettime,getNo)
        cursor.execute(a)

        #save lib
        db.commit()
    elif(msg.topic=="/IEYI/hrjh/search/send"):
        searchget=str(msg.payload)[2:-1]
        a="SELECT * FROM DATA WHERE BEDNO='%s'"%(searchget)
        cursor.execute(a)
        xs=list(cursor.fetchone())
        s = ' '.join(str(x) for x in xs)
        print(s)
        client.publish("/IEYI/hrjh/search/return", str(s))

# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定建立連線回呼函數
client.on_connect = on_connect

# 設定接收訊息回呼函數
client.on_message = on_message

# 設定登入帳號密碼（若無則可省略）
client.username_pw_set("","")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect("test.mosquitto.org", 1883)

# 進入無窮處理迴圈
client.loop_forever()