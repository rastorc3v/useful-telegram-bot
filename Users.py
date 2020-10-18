from DatabaseUpdater import users_id_list, add_new_user


def check_and_add(chat_id, f_name, s_name, vip=0):
    if (chat_id,) not in users_id_list():
        add_new_user(chat_id, f_name, s_name, vip)
