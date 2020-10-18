import sqlite3

def users_id_list():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return list(c.execute("SELECT chat_id FROM users"))

def add_new_user(chat_id, f_name, s_name, vip=0):
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        record = (chat_id, f_name, s_name, vip)
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", record)
        conn.commit()

def superusers_id_list():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return list(c.execute("SELECT chat_id FROM superusers"))

def vip_users_id_list():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return list(c.execute("SELECT chat_id FROM users WHERE vip=1"))

def events_update():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM events")
        conn.commit()

def get_event_inf():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM events")

        conn.commit()

def get_len_title():
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return len(list(c.execute("SELECT title FROM events")))

def get_horoscope(sign):
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return c.execute("SELECT text FROM horoscope WHERE sign="+sign)

def add_vip(chat_id, is_vip):
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        return list(c.execute("UPDATE users SET vip=" + is_vip + " WHERE chat_id=" + chat_id))

def get_chat_id_by_name(name):
    with sqlite3.connect('db.sqlite3', check_same_thread=False) as conn:
        c = conn.cursor()
        first_name = name.split(' ')[0]
        try:
            second_name = name.split(' ')[1]
        except:
            second_name = ''
        if len(second_name):
            return list(c.execute("SELECT chat_id FROM users WHERE first_name='" + first_name +
                                  "' AND second_name='" + second_name + "';"))
        else:
            return list(c.execute("SELECT chat_id from users WHERE first_name='" + first_name + "';"))
