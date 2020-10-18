import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from DatabaseUpdater import vip_users_id_list
from EmojiGenerator import em

def events_update(tb):
    while True:
        with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
            print("Обновление данных о событиях\n")
            c = conn.cursor()
            old_title = list(c.execute("SELECT title FROM events"))
            c.execute("DELETE FROM events")
            conn.commit()
            day = []
            title = []
            org = []
            url = []
            datetime = []
            r = requests.get("https://events.dev.by/filter/4372/city")
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all("time"):
                datetime.append(tag.text)

            for i in range(0, len(datetime), 3):
                day.append(datetime[i + 2].strip('\n'))

            for tag in soup.find_all("a", {"class": "title"}):
                title.append(tag.text)
                a = requests.get("https://events.dev.by/" + tag.get('href'))
                url.append(a.text.split("div class='text'")[1].split("</a>")[0].split('"')[1].split('"')[0])

            for tag in soup.findAll("div", {"class": "item-body left"}):
                try:
                    org.append(tag.text.split('Организатор:\n')[1].split('\n')[0])
                except IndexError:
                    org.append('нет данных')

            if len(title) > len(old_title):
                for (chat,) in vip_users_id_list():
                    tb.send_message(chat, "Новое событиееее!!!!!")

            for i in range(len(title)):
                record = (title[i], day[i], org[i], url[i])
                c.execute("INSERT INTO events VALUES (?, ?, ?, ?)", record)
                conn.commit()
        time.sleep(600)

def get_event_inf():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        event_inf = list(c.execute("SELECT * FROM events"))
        title = []
        day = []
        org = []
        url = []
        for i in range(len(event_inf)):
            title.append(event_inf[i][0])
            day.append(event_inf[i][1])
            org.append(event_inf[i][2])
            url.append(event_inf[i][3])
        return day, title, org, url,

def weather_update():
    while True:
        with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
            print("Обновление погодных данных")
            c = conn.cursor()
            c.execute("DELETE FROM weather")
            conn.commit()
            tm = []
            temp = []
            weathers = []
            weather_emoji = []
            r = requests.get("https://yandex.by/pogoda/gomel")
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            weather_img = {'bkn_n.svg': ":cloud:",
                           'bkn_d.svg': ":partly_sunny:",
                           'skc_n.svg': ":new_moon:",
                           'ovc.svg': ":cloud:",
                           'fct_sn_rs.svg': ":sunrise:",
                           'fct_sn_dwn.svg': ":city_sunset:",
                           'ovc_-ra.svg': ":cloud_with_rain:",
                           'ovc_+ra.svg': ":cloud_with_rain:",
                           'ovc_ra.svg': ":cloud_with_rain:",
                           'skc_d.svg': ":sunny:"}
            for tag in soup.findAll("div", {"class": "fact__hour-label"}):
                tm.append(tag.text)
            for tag in soup.findAll("div", {"class": "fact__hour-temp"}):
                temp.append(tag.text)
            i = 0
            for tag in soup.findAll("img"):
                if i != 0:
                    if i < len(tm) + 1:
                        weathers.append(weather_img[tag.get('src').split('/')[-1]])
                        i = i + 1
                else:
                    i = 1
            for code in weathers:
                weather_emoji.append(em(code))

            for i in range(len(weathers)):
                record = (tm[i], weathers[i], temp[i])
                c.execute("INSERT INTO weather VALUES (?, ?, ?)", record)
                conn.commit()
        time.sleep(3600)

def get_weather_inf():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        event_inf = list(c.execute("SELECT * FROM weather"))
        tm = []
        weather = []
        temp = []
        for i in range(len(event_inf)):
            tm.append(event_inf[i][0])
            weather.append(event_inf[i][1])
            temp.append(event_inf[i][2])

        return tm, weather, temp,

def update_horoscope():
    while True:
        print("Обновления данных гороскопа")
        accord = {"ЛЕВ": 'lev',
                  "ОВЕН": 'oven',
                  "БЛИЗНЕЦЫ": 'blizneci',
                  "РАК": 'rak',
                  "ТЕЛЕЦ": 'telec',
                  "ДЕВА": 'deva',
                  "ВЕСЫ": 'vesi',
                  "СКОРПИОН": 'scorpion',
                  "СТРЕЛЕЦ": 'strelec',
                  "КОЗЕРОГ": 'kozerog',
                  "ВОДОЛЕЙ": 'vodoley',
                  "РЫБЫ": 'ribi'}
        with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM horoscope")
            conn.commit()
        r =requests.get('https://mogilev.biz/spravka/horoscope/obsch/')
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        sign = []
        text = []
        for tag in soup.findAll("div", {'class': 'newslist'}):
            data = tag.text.split('\n')
            sign.append(data[1].split(' ')[0])
            text.append(data[2])
        del sign[0]
        del text[0]
        with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
            for i in range(0, 12):
                c = conn.cursor()
                record = (accord[sign[i]], text[i])
                c.execute("INSERT INTO horoscope VALUES (?,?)", record)
        conn.commit()
        time.sleep(7200)

def get_horoscope(sign):
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        query = "SELECT text FROM horoscope WHERE sign = '{}'".format(sign)
        return list(c.execute(query))[0][0]
