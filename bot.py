#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import json
import getter
import requests
import sys
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

def data_processing(id, pay, msg):
    add_user(id = id)
    if pay=='"command":"start"' or pay == "admin":
        photo_path = []
        photo_path.append("img/fan.png")
        print("tut")
        photo = upload.photo_messages(photo_path)
        print(photo)
        vk.method("messages.send", {"user_id": id, "message": "Привет, я бот Макс!\nЯ представляю лучшую компанию по аренде авто 'Прокат Сервис Чита'\n\nЯ могу рассказать тебе о компании, подобрать авто или показать список всех доступных авто!\n\nСо мной следует общаться посредством графической клаватуры, это очень важно.\nИтак, начнем😎", "keyboard": get_main_keyboard(id = id, connection = connection)})
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": "Опять по новой? Ну, ладно...", "keyboard":key['start']})
    elif pay == "about_us":
        vk.method("messages.send", {"user_id": id, "message": "Компания 'Прокат Сервис Чита' просто охуенная!\nСкорее бери у нас тачку и будет тебе счастье!\n\nи еще много текстааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааи еще много текстааааааааааааааааааааааааааааааааааааааа", "keyboard":get_main_keyboard(id = id, connection = connection)})
    
    elif pay == "subscribe":
        subscribe(id)
    
    elif pay == "show_auto":
        sql = "select name, power, price, img from CARS"
        res = data.executeSQL(sql, connection)
        msg = ""
        photos = []
        i = 1
        for car in res:
            msg += str(i)+". Авто: "+str(car[0])+"\n"+"Мощность: "+str(car[1])+"\n"+"Цена: "+str(car[2])+" рублей/день.\n\n"
            i = i+1
            photos.append(car[3])
        vk.method("messages.send", {"user_id": id, "message": msg, "keyboard":get_main_keyboard(id, connection), "attachment": str(photos[0])+","+str(photos[1])+","+str(photos[2])})
            

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
                    finally:
                        print("pay: ",pay)
                else:
                    pay = "0"
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