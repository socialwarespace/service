#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import json
import getter
import requests
import sys
import os
import time
import keyboards
import database as data

def auth():
    token = getter.get_token()
    token = token[0:len(token)-1] #need to fix token.txt
    print(token)
    vk = vk_api.VkApi(token=token, api_version=5.68)
    vk._auth_token()
    return vk
#vk.method("messages.send", {"user_id": id, "message": "hj", "keyboard": get_main_keyboard(id =id, connection = connection)})
def get_main_keyboard(id, connection):
    sql = "SELECT subscribe FROM USERS WHERE id = "+str(id)
    res = data.executeSQL(sql = sql, connection = connection)
    if res[0][0] == True:
        return key['main_menu_on']
    else:
        return key['main_menu_off']
def add_user(id):
    sql = "SELECT id FROM USERS WHERE id = " + str(id)
    res = data.executeSQL(sql = sql, connection = connection)
    if res == 0:
        sql = "INSERT INTO USERS (id) VALUES("+str(id)+")"
        print(sql)
        data.executeSQL(sql = sql, connection = connection)
        print("iixaaa")
def subscribe(id):
    sql = "SELECT subscribe FROM USERS WHERE id = " + str(id)
    res = data.executeSQL(sql, connection)
    if res[0][0]==False:
        sql = "UPDATE USERS SET subscribe = True WHERE id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Теперь я буду отправлять тебе новости о наших акциях и не только😉", "keyboard": get_main_keyboard(id, connection)})

    else:
        sql = "UPDATE USERS SET subscribe = False WHERE id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Если передумаешь, я буду рад🙃", "keyboard": get_main_keyboard(id, connection)})

def get_photos(directories, type):
    files = []
    for directory in directories:
        print(directory)
        allow_files = os.listdir(directory)
        print(allow_files)
        if type == 'main':
            files.append(directory+"/"+allow_files[allow_files.index('main.jpeg')])
        else:
            for f in allow_files:
                files.append(directory+"/"+f)
    print("files: ",files)
    return upload.photo_messages(files)

def get_attachment(photos):
    attachment = ""
    for photo in photos:
        attachment = attachment + "photo"+str(photo['owner_id'])+"_"+str(photo['id'])+","
    return attachment[0:len(attachment)-1]


def data_processing(id, pay, msg):
    add_user(id = id)
    if pay=='"command":"start"' or pay == "admin":
        photos = get_photos(["img/logo"], "main")
        print(photos)
        vk.method("messages.send", {"user_id": id, "message": "Привет, я бот Макс!\nЯ представляю лучшую компанию по аренде авто 'Прокат Сервис Чита'\n\nЯ могу рассказать тебе о компании, подобрать авто или показать список всех доступных авто!\n\nСо мной следует общаться посредством графической клаватуры, это очень важно.\nИтак, начнем😎", "keyboard": get_main_keyboard(id = id, connection = connection), "attachment": get_attachment(photos)})
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": "Опять по новой? Ну, ладно...", "keyboard":key['start']})
    elif pay == "about_us":
        about = open("info/about.txt")
        msg = about.read()
        vk.method("messages.send", {"user_id": id, "message": msg, "keyboard":get_main_keyboard(id = id, connection = connection)})
    
    elif pay == "subscribe":
        subscribe(id)
    
    elif pay == "selection":
        sql = "delete from USERS_CARS where id = "+str(id)
        data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какой авто Вас интересует?", "keyboard": key['type']})
    
    elif pay == "drive_unit":
        if msg == "Минивэн":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'minivan')"
            data.executeSQL(sql, connection)
        elif msg == "Легковой авто":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'passenger')"
            data.executeSQL(sql, connection)
        elif msg == "Внедорожник":
            sql = "insert into USERS_CARS (id, type) values("+str(id)+", 'suv')"
            data.executeSQL(sql, connection)
        elif msg =="Неважно":
            sql = "insert into USERS_CARS (id) values("+str(id)+")"
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какой привод нужен?", "keyboard": key['drive_unit']})
    elif pay == "volume":
        if msg == "Передний":
            sql = "update USERS_CARS set drive_unit = 'front' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "Задний":
            sql = "update USERS_CARS set drive_unit = 'back' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "4wd":
            sql = "update USERS_CARS set drive_unit = '4wd' where id = "+str(id)
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какой объем двигателя хотите?", "keyboard": key['volume']})
    elif pay == "steering":
        if msg == "До двух литров":
            sql = "update USERS_CARS set volume = '<2' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От двух до трех литров":
            sql = "update USERS_CARS set volume = '2-3' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От трех литров":
            sql = "update USERS_CARS set volume = '>3' where id = "+str(id)
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какой руль?", "keyboard": key['steering']})
    elif pay == "price":
        if msg == "Левый":
            sql = "update USERS_CARS set steering = 'left' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "Правый":
            sql = "update USERS_CARS set steering = 'right' where id = "+str(id)
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "Какая цена Вас устроит?", "keyboard": key['price']})
    elif pay == "how_long":
        if msg == "До 2000 рублей/сутки":
            sql = "update USERS_CARS set price = '<2000' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От 2000 до 3000 рублей/сутки":
            sql = "update USERS_CARS set price = '2000-3000' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От 3000 рублей/сутки":
            sql = "update USERS_CARS set price = '>3000' where id = "+str(id)
            data.executeSQL(sql, connection)
        vk.method("messages.send", {"user_id": id, "message": "На какой срок планируете брать авто? От этого зависит цена.", "keyboard": key['how_long']})
    elif pay == "finish_selection":
        if msg == "До десяти дней":
            sql = "update USERS_CARS set how_long = '<10' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От десяти до двадцати дней":
            sql = "update USERS_CARS set how_long = '10-20' where id = "+str(id)
            data.executeSQL(sql, connection)
        elif msg == "От двадцати одного дня":
            sql = "update USERS_CARS set how_long = '>20' where id = "+str(id)
            data.executeSQL(sql, connection)
        sql = "select * from USERS_CARS where id = " + str(id)
        res = data.executeSQL(sql, connection)
        for r in res:
            print(r)
        vk.method("messages.send", {"user_id": id, "message": "Вот так!", "keyboard": get_main_keyboard(id, connection)})     

    else: 
        vk.method("messages.send", {"user_id":id, "message": "Я тебя не понимаю...","keyboard": get_main_keyboard(id = id, connection = connection)})
def get_msg():
    while True:
        try:
            messages = vk.method("messages.getConversations", {"offset": 0, "count": 100, "filter": "unanswered"})
            if messages["count"] >= 1:
                id = messages["items"][0]["last_message"]["from_id"]
                msg = messages["items"][0]["last_message"]["text"]
                if "payload" in messages["items"][0]["last_message"]:
                    pay = messages["items"][0]["last_message"]["payload"][1:-1]
                    try:
                        pay = bytes(pay, 'cp1251').decode('utf-8')
                    except ValueError:
                        pass
                    try:
                        msg = bytes(msg, 'cp1251').decode('utf-8')
                    except ValueError:
                        pass    
                else:
                    pay = "0"
                print("pay: ", pay)
                print("msg: ", msg)
                data_processing(id=id, pay=pay, msg=msg)
        except Exception:
            time.sleep(0.1)
key = keyboards.get_keyboards() 
vk = auth()
upload = vk_api.upload.VkUpload(vk)
#error = vk_api.VkApi.http_handler(1)
print("1 ",vk)  
connection = data.connect()
print("2 ", connection)
get_msg()