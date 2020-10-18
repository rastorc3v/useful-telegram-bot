from Parser import events_update, weather_update, update_horoscope, get_horoscope
from threading import Timer
from EmojiGenerator import get_em, em

emojis = get_em()
days = ['пн,', 'вт,', 'ср,', 'чт,', 'пт,', 'сб,', 'вс,']


def start_parsing(tb):
    Timer(0, events_update, (tb,)).start()
    Timer(0, weather_update, ()).start()
    Timer(0, update_horoscope, ()).start()


def get_events_message(day, title, org, url, i):
    result = ""
    result = result + emojis['clock'] + day[i] + "\n" \
                    + emojis['megaphone'] + title[i] + "\n" \
                    + emojis['org'] + org[i] + "\n" \
                    + emojis['link'] + str(url[i]) + "\n\n"
    return result


# TODO: optimize function
def get_weather_message(tm, weather, temp, show_param, tb):
    params = {1: (0, 5), 2: (5, 10), 3: (10, 15), 4: (15, 20), 5: (20, 25)}
    tm_space = "   "
    result = ""
    try:
        for j in range(len(list(params.keys()))):
            for i in range(params[show_param][0], params[show_param][1]):
                for day in days:
                    if day in tm[i]:
                        tm[i] = tm[i].split(',')[1]
                if len(tm[i]) == 5:
                    result = result + tm[i] + tm_space
                else:
                    result = result + "0" + tm[i] + tm_space
            result = result + "\n"

            for i in range(params[show_param][0], params[show_param][1]):
                result = result + "  " + em(weather[i]) + "      "
            result = result + "\n"

            for i in range(params[show_param][0], params[show_param][1]):
                a = len(temp[i])
                if a == 4:
                    if i == params[show_param][0] + 2:
                        result = result + "  " + temp[i] + "    "
                    else:
                        result = result + " " + temp[i] + "    "
                elif a == 3:
                    if i == params[show_param][0] + 2:
                        result = result + "   " + temp[i] + "     "
                    else:
                        result = result + "  " + temp[i] + "    "
                elif a == 5:
                    result = result + "" + temp[i] + "    "
                else:
                    result = result + "" + temp[i] + "  "

            result = result + "\n"

            for i in range(40):
                result = result + "_"
            result = result + "\n\n"

            show_param = show_param + 1
        return result
    except:
        tb.send_message(827073258, "Бот накрылся!")
        return "Фунция недоступна на данный момент.\nВедутся техниские работы"

def get_horoscope_message(sign):
    return "*Ваш гороскоп на сегодня*\n\n" + get_horoscope(sign)
