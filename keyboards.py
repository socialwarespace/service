#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import json

def get_button(label, color,payload=""):
    return{
        "action":
        {
            "type":"text",
            "payload":json.dumps(payload),
            "label":label
        },
        "color": color
    }
def convertToString(keyboard):
    return json.dumps(keyboard, ensure_ascii = False)

def get_keyboards():
    
    keyboard_start = {
        "one_time": True,
        "buttons":[
            [get_button(label="Начать",color="primary", payload="admin")]
        ]
    }
    keyboard_start = convertToString(keyboard_start)


    keyboard_main_menu_on = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Отписаться от новостей",color="default", payload="subscribe")
            ],
            [
                get_button(label="Узнать о нас",color="default", payload="about_us")
            ],
            [
                get_button(label="Посмотреть все авто",color="default", payload="show_auto")
            ]
        ]
    }
    keyboard_main_menu_on = convertToString(keyboard_main_menu_on)

    keyboard_main_menu_off = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Подписаться на новости",color="default", payload="subscribe")
            ],
            [
                get_button(label="Узнать о нас",color="default", payload="about us")
            ],
            [
                get_button(label="Посмотреть все авто",color="default", payload="show_auto")
            ]
        ]
    }
    keyboard_main_menu_off = convertToString(keyboard_main_menu_off)
    
    return {
        'start': keyboard_start,
        'main_menu_on': keyboard_main_menu_on,
        'main_menu_off':keyboard_main_menu_off
    }