import paho.mqtt.client as mqtt
import sqlite3
import time
db = sqlite3.connect('TEST.db')
cursor=db.cursor()
# 建立連線（接收到 CONNACK）的回呼函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/rc5")
def on_message(client, userdata, msg):
    print(msg.payload)
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
client.loop_start()
while True:
    print("1")
    time.sleep(1)