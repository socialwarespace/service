#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import json
import getter
import time
import keyboards
import database as data

def auth():
    token = getter.get_token()
    token = token[0:len(token)-1] #need to fix token.txt
    print(token)
    vk = vk_api.VkApi(token=token)
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
    print(sql)
    res = data.executeSQL(sql = sql, connection = connection)
    if res == 0:
        sql = "INSERT INTO USERS (id) VALUES("+str(id)+")"
        print(sql)
        data.executeSQL(sql = sql, connection = connection)
        print("iixaaa")

def data_processing(id, pay, msg):
    add_user(id = id)
    get_main_keyboard(id,connection)
    print("tut")
    if pay=='"command":"start"' or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": "Привет! Я бот Макс.\nЯ представляю лучшую компанию по аренде авто в Чите 'Прокат Сервис Чита'\n Я могу помочь подобрать для тебя авто, рассказать о нашей компании или просто показать все авто, которые ты можешь у нас арендовать!\n Со мной следует общаться посредством графической клавиатуры, так я пока не очень умный бот:) Начем?😎", "keyboard": key['main_menu_on']})
    else: 
        vk.method("messages.send", {"user_id":id, "message": "ffffffff"})
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
                        print(pay)
                else:
                    pay = "0"
                    print(msg)
                data_processing(id=id, pay=pay, msg=msg)
        except Exception:
            time.sleep(0.1)
key = keyboards.get_keyboards() 

vk = auth()
print("1 ",vk)  
connection = data.connect()
print("2 ", connection)
get_msg()