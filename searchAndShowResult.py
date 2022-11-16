import tkinter
import tkinter.font
from numpy import delete
import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time

# 設置日期時間的格式
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 連線設定

#######################################################

searchWin=tkinter.Tk()

def setObject():
    global bedno
    bedno=tkinter.StringVar()
    global bednobox
    bednobox=tkinter.Entry(searchWin, textvariable=bedno,width=20,font=tkinter.font.Font(size=36))
    global searchbutton
    searchbutton=tkinter.Button(searchWin, text='查詢', command=mqttsearch,width=5,font=tkinter.font.Font(size=36))

    bednobox.grid(row=0,column=0)
    searchbutton.grid(row=0,column=1)
    global listbox
    listbox=tkinter.Listbox(searchWin,width=30,font=tkinter.font.Font(size=36))
    listbox.grid(row=1,column=0,columnspan=2)

def mqttsearch():
    client.publish("/IEYI/hrjh/search/send", bednobox.get())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    client.subscribe("/IEYI/hrjh/search/return")

def on_message(client, userdata, msg):
    getmsg=msg.payload.decode('utf-8').split()
    print(getmsg)
    listbox.delete(0,'end')
    getname=getmsg[1][0]+"◯"+getmsg[1][2]
    listbox.insert('end',"姓名：%s"%(getname))
    listbox.insert('end',"電子標籤唯一碼：%s"%(getmsg[3]))
    listbox.insert('end',"床號：%s"%(getmsg[4]))
    listbox.insert('end',"倒數第二個通過的門：%s"%(getmsg[5]))
    listbox.insert('end',"倒數第二個通過門的時間：%s"%(getmsg[6]))
    listbox.insert('end',"最後一次通過的門：%s"%(getmsg[7]))
    listbox.insert('end',"最後一次通過門的時間：%s"%(getmsg[8]))
    listbox.insert('end',"猜測所在位置：%s"%(getmsg[9]))

# 初始化地端程式
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 設定登入帳號密碼
client.username_pw_set("","")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("test.mosquitto.org", 1883, 60)


setObject()
client.loop_start()
searchWin.mainloop()
