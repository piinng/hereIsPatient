import tkinter
import tkinter.font
from numpy import delete
import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time
import os
from tkinter import messagebox

# 設置日期時間的格式
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 連線設定

#######################################################

searchWin=tkinter.Tk()



def notify(title, text):
    os.system("""
    osascript -e 'display notification "{}" with title "{}" sound name "{}"'
    """.format(text, title,"/System/Library/Sounds/Tink.aiff"))

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
    listbox=tkinter.Listbox(searchWin,width=30,height=5,font=tkinter.font.Font(size=36))
    listbox.grid(row=1,column=0,columnspan=2)

def mqttsearch():
    print("查詢鍵被按下")
    client.publish("/IEYI/hrjh/search/send", bednobox.get())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 每次連線之後，重新設定訂閱主題
    client.subscribe("/IEYI/hrjh/search/return")
    client.subscribe("/IEYI/hrjh/aram/search/danger")
    client.subscribe("/IEYI/hrjh/aram/search/dementia")
    client.subscribe("/IEYI/hrjh/aram/search/time")


def on_message(client, userdata, msg):
    if(msg.topic=="/IEYI/hrjh/search/return"):
        getmsg=msg.payload.decode('utf-8').split()
        print(getmsg)
        listbox.delete(0,'end')
        getname=getmsg[1][0]+"◯"+getmsg[1][2]
        listbox.insert('end',"姓名：%s"%(getname))
        listbox.insert('end',"電子標籤唯一碼：%s"%(getmsg[3]))
        listbox.insert('end',"床號：%s"%(getmsg[4]))
        listbox.insert('end',"所在區域：%s"%(getmsg[6]))
    # elif(msg.topic=="/IEYI/hrjh/aram/search/danger"):
    #     getmsg=msg.payload.decode('utf-8').split()
    #     if(getmsg[6]=="EL"):
    #         notify("禁區警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n跑到逃生梯了，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    #     if(getmsg[6]=="NS"):
    #         notify("禁區警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n跑進護理站了，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    # elif(msg.topic=="/IEYI/hrjh/aram/search/dementia"):
    #     getmsg=msg.payload.decode('utf-8').split()
    #     notify("失智警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n離開醫院了，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    elif(msg.topic=="/IEYI/hrjh/aram/search/time"):
        getmsg=msg.payload.decode('utf-8').split()
        print(getmsg)
        result=messagebox.showinfo("","姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n待在廁所超過10秒鐘，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
        print(result)
        # notify("時間警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n待在廁所超過5秒鐘，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    elif(msg.topic=="/IEYI/hrjh/aram/search/danger"):
        getmsg=msg.payload.decode('utf-8').split()
        print(getmsg)
        result=messagebox.showinfo("","姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n跑到%s了，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4],getmsg[6]))
        print(result)
        # notify("禁區警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n待在廁所超過5秒鐘，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    elif(msg.topic=="/IEYI/hrjh/aram/search/dementia"):
        getmsg=msg.payload.decode('utf-8').split()
        print(getmsg)
        result=messagebox.showinfo("","姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n跑出醫院了，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
        print(result)
        # notify("失智警報", "姓名：%s\n電子標籤唯一碼：%s\n床號：%s\n待在廁所超過5秒鐘，請過去查看！！"%((getmsg[1][0]+"◯"+getmsg[1][2]),getmsg[3],getmsg[4]))
    


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
