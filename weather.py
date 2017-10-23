import requests

from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime


cities = {
    'murmansk': '_murm',
    'moscow': '_msk',
    'saint-petersburg': '_spb',
    '10899': '_snej',
    '10898': '_sever',
    '21665': '_gadg',
    '10895': '_kanda',
    '20153': '_kovdor',
    '101069': '_umba',
    '10894': '_apat',
    '20152': '_kirovsk',
    '20156': '_pz',
    '20155': '_oleneg',
    '101068': '_lovozero',
    '10896': '_monch',
    '100660': '_nikel',
    '20151': '_zap',
    '20773': '_kirk'
}


condition_codes = {
    "Ясно": "A",
    "A": "B",# Ясно с 20:59 по 5:00
    "Малооблачно": "C",
    "B": "D", # Малооблачно с 20:59 по 5:00
    "Облачно с прояснениями": "E",
    "E": "F", # Облачно с прояснениями с 20:59 по 5:00
    "Пасмурно": "G",
    "Небольшой дождь": "H",
    "Дождь": "I",
    "Сильный дождь": "J",
    "Сильный ливень": "K",
    "Сильный дождь, гроза": "L",
    "Гроза": "M",
    "Небольшой снег": "N",
    "Снег": "O",
    "Снегопад": "P",
    "Очень сильный снег": "Q",
    "Дождь со снегом": "R",
    "H": "S",  # Небольшой дождь с 20:59 по 5:00
    "N": "T"  # Небольшой снег с 20:59 по 5:00
}

weather_info = {
    "A":"Без осадков",
    "B":"Без осадков",
    "C":"Без осадков",
    "D":"Без осадков",
    "E":"Без осадков",
    "F":"Без осадков",
    "G":"Без осадков",
    "N":"Снег",
    "O":"Снег",
    "P":"Снег",
    "Q":"Снег",
    "T":"Снег",
    "H":"Дождь",
    "I":"Дождь",
    "J":"Дождь",
    "K":"Дождь",
    "S":"Дождь",
    "R":"Дождь со снегом",
    "L":"Гроза",
    "M":"Гроза"
}

def write_file(data, filename, flag):
    with open(filename, flag, encoding="utf-8") as file:
        file.write(str(data))


def get_yandex_weather(city):
    response = requests.get("https://yandex.ru/pogoda/" + city)
    return BeautifulSoup(response.content, "lxml")


def parse_temp(city):
    weather_data = get_yandex_weather(city)
    temp = weather_data.find("span", "temp__value").text
    temp.replace("−", "-")
    return temp + "°" if temp is not None else ""


def parse_condition(city):
    weather_data = get_yandex_weather(city)
    condition = weather_data.find("div", "fact__condition").text
    return condition if condition is not None else ""


def get_condition_code(condition):
    # можно вынести отсюда и передать аргументом
    hour = int(datetime.today().strftime("%H"))
    if condition in condition_codes:
        condition_code = condition_codes[condition]
        if 5 > hour >= 21:
            condition_code = condition_codes[condition_code]
        return condition_code

    return ""

def reduction_weather_data (condition_code):
    if condition_code in weather_info:
        return weather_info[condition_code]


if __name__ == '__main__':
    for city in cities:
        temp, cond = parse_temp(city), parse_condition(city)
        cond_code = get_condition_code(cond)
        w_info = reduction_weather_data(cond_code)


        if cond not in condition_codes:
            write_file(cond + '\n',"Jornal_W.txt","a")

        for data, prefix in zip([temp, w_info, cond_code], ["T", "WI", "W"]):
            write_file(data, prefix + cities[city] + ".txt", "w")

        print(cities[city][1:], temp, cond, "(" + w_info + ")", cond_code)

        sleep(0.1)
