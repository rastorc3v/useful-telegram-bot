import datetime
import telebot
from telebot import types
from DatabaseUpdater import get_len_title, superusers_id_list, users_id_list, add_vip, get_chat_id_by_name
from EmojiGenerator import get_em
from MessageConstructor import get_events_message, get_weather_message, get_horoscope_message
from Parser import get_event_inf, get_weather_inf
import environment
import argparse
from printer import Printer
from Users import User
from Parser import Parser
from printer import printer

printer.push_context('starting', "info1")

printer.info2('parse console args')
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--dev', type=bool, help='run in development mode')
console_args = arg_parser.parse_args()

if console_args.dev:
    printer.info2('passed dev arg - True')

if console_args.dev or not environment.IS_PROD:
    printer.info3('development mode')
    token = environment.DEV_TOKEN
else:
    printer.info3('production mode')
    token = environment.PROD_TOKEN

tb = None
try:
    tb = telebot.TeleBot(token)
except:
    printer.error('unable to create TeleBot instance')
    exit(-1)
printer.info3('bot instance created')

emoji = get_em()
user = User()

parser = Parser()



@tb.message_handler(regexp="События")
def handle_get_events(message):
    user.handle_message(message.chat.id, message.chat.first_name, message.chat.last_name, message.text)
    li = get_event_inf()

    if not get_len_title():
        tb.send_message(message.chat.id, "Пока что ничего... Мы сообщим когда появится что-то")

    for i in range(get_len_title()):
        tb.send_message(message.chat.id, get_events_message(li[0], li[1], li[2], li[3], i))
    tb.send_message(message.chat.id, "Для получения уведомлений вы должны получить статус вип.")


@tb.message_handler(regexp="Погода")
def handle_get_events(message, param=1):
    user.handle_message(message.chat.id, message.chat.first_name, message.chat.last_name, message.text)
    weath_li = get_weather_inf()
    tb.send_message(message.chat.id, text=get_weather_message(weath_li[0], weath_li[1], weath_li[2], show_param=param, tb=tb))


@tb.message_handler(regexp=emoji['blizneci'] + " Гороскоп")
def handle_get_weather(message):
    user.handle_message(message.chat.id, message.chat.first_name, message.chat.last_name, message.text)
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3
    oven = types.InlineKeyboardButton(emoji['oven'] + ' Овен', callback_data='oven')
    telec = types.InlineKeyboardButton(emoji['telec'] + 'Телец', callback_data='telec')
    blizneci = types.InlineKeyboardButton(emoji['blizneci'] + 'Близнецы', callback_data='blizneci')
    rak = types.InlineKeyboardButton(emoji['rak'] + 'Рак', callback_data='rak')
    lev = types.InlineKeyboardButton(emoji['lev'] + 'Лев', callback_data='lev')
    deva = types.InlineKeyboardButton(emoji['deva'] + 'Дева', callback_data='deva')
    vesi = types.InlineKeyboardButton(emoji['vesi'] + 'Весы', callback_data='vesi')
    scorpion = types.InlineKeyboardButton(emoji['scorpion'] + 'Скорпион', callback_data='scorpion')
    strelec = types.InlineKeyboardButton(emoji['strelec'] + 'Стрелец', callback_data='strelec')
    kozerog = types.InlineKeyboardButton(emoji['kozerog'] + 'Козерог', callback_data='kozerog')
    vodoley = types.InlineKeyboardButton(emoji['vodoley'] + 'Водолей', callback_data='vodoley')
    ribi = types.InlineKeyboardButton(emoji['ribi'] + 'Рыбы', callback_data='ribi')
    markup.add(oven, telec, blizneci, rak, lev, deva, vesi, scorpion, strelec, kozerog, vodoley, ribi)
    tb.send_message(message.chat.id, text="Выберите знак", reply_markup=markup, parse_mode='markdown')


@tb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        try:
            user.handle_message(call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name, call.message.text)
            tb.edit_message_text(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 text=get_horoscope_message(call.data),
                                 parse_mode='Markdown')
        except:
            pass


# broadcast режим для массовой рассылки сообщений админами
@tb.message_handler(regexp="broadcast")
def broadcast(message):
    if (message.chat.id,) in superusers_id_list():
        user.handle_message(message.chat.id, message.chat.first_name, message.chat.last_name, message.text, "broadcast")
        for (chats,) in users_id_list():
            # if m.chat.id != chats:
            try:
                tb.send_message(chats, message.text.lstrip("broadcast"))
            except:
                pass
    print('-----NEW BROADCAST-----\nfrom ' + str(message.chat.first_name) + " " + str(message.chat.last_name) +
            " chat_id - " + str(message.chat.id) + "\n" + message.text.lstrip("broadcast") + "\n" + str(
            str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().hour) + ":" +
            str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second)) + "\n")

@tb.message_handler(commands=['start', 'update'])
def start(message):
    user.check_and_add(message.chat.id, message.chat.first_name, message.chat.last_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    events = types.KeyboardButton(emoji['calendar'] + ' События')
    weath = types.KeyboardButton(emoji['weath'] + ' Погода')
    horoscope = types.KeyboardButton(emoji['blizneci'] + ' Гороскоп')
    markup.add(events, weath, horoscope)
    tb.send_message(message.chat.id, '''Добро пожаловать в обновлённую версию, **{}**!\n\nЯ самый полезный бот на этой планете!=)\n__Помни что с ВИП 
аккаунтом открываются новые возможности.'''.format(message.chat.first_name), reply_markup=markup,
                    parse_mode='markdown')


@tb.message_handler(regexp="send")
def sender(message):
    if (message.chat.id,) in superusers_id_list():
        user.handle_message(message.chat.id, message.chat.first_name, message.chat.last_name, message.text, "private")
        tb.send_message(message.text.lstrip("send ").split('-')[0], message.text.split('-')[1])
        print(str(message.chat.first_name) + " " + str(message.chat.last_name) + str(message.chat.id) + "\n" + str(
            message.text.split('-')[1]) + "\n" + str(
            str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().hour) + ":" +
            str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second)) + "\n")

# 8029353 vip 1 - give 8029353 user vip status
@tb.message_handler(regexp="vip")
def sender(m):
    if (m.chat.id,) in superusers_id_list():
        add_vip(m.text.split(' vip ')[0], m.text.split(' vip ')[1])
        tb.send_message(m.chat.id, text="Пользователь с айди " + m.text.split(' vip ')[0]
                                        + "получил/потерял статус vip(" + m.text.split(' vip ')[1] + ")")

@tb.message_handler(regexp=" chat id")
def get_chat_id(m):
    if (m.chat.id,) in superusers_id_list():
        if len(get_chat_id_by_name(m.text.split(' chat id')[0])):
            tb.send_message(m.chat.id, get_chat_id_by_name(m.text.split(' chat id')[0]))
        else:
            tb.send_message(m.chat.id, "Пользователь не найден")


tb.polling()
tb.polling(none_stop=True)
tb.polling(interval=3)

while True:
    pass
