import requests
import json
import time
import config
import sys

tokken = config.unlimited_tokken
tokken2 = config.oneday_tokken
URL = 'https://api.vk.com/method/friends.getMutual'
URL2 = 'https://api.vk.com/method/users.get'


class VkUser():
    def __init__(self, id):
        try:
            user_info = get_user_id(id)
        except KeyError:
            print(f'Пользователя с id {id} нету')
            sys.exit()
        if id[0].isalpha():
            self.user_id = user_info['response'][0]['id']
            self.first_name = user_info['response'][0]['first_name']
            self.last_name = user_info['response'][0]['last_name']
        else:
            self.user_id = id
            self.first_name = user_info['response'][0]['first_name']
            self.last_name = user_info['response'][0]['last_name']
        print(f'added user id{self.user_id} {self.first_name} {self.last_name}')

    def __str__(self):
        return 'vk.com/id' + str(self.user_id)

    def __and__(self, other):
        params = {
            'source_uid': self.user_id,
            'target_uid': other.user_id,
            'v': '5.52',
            'access_token': tokken2
        }
        response = requests.get(URL, params=params)
        # print(response.status_code)
        json_ = response.json()
        # print(json_)

        return add_user(json_)

    def __del__(self):
        try:
            print(f'deleted {self.user_id}')
        except AttributeError:
            return 0


def add_user(json_):
    ids_list = json_['response']
    users_list = []
    for user in ids_list:
        users_list.append(VkUser(str(user)))
        # time.sleep(0.4)
    return users_list


def get_user_id(user):
    params = {
        'user_ids': user,
        'v': '5.52',
        'access_token': tokken
    }
    response = requests.get(URL2, params=params)
    # print(response.status_code)
    time.sleep(0.4)
    json_ = response.json()
    if json_['response'][0]['first_name'] == 'DELETED':
        print(f'Пользователь с id {user} удален')
        sys.exit()
    # print(json_)
    return json_


def print_users(users_list):
    if len(users_list) == 0:
        print('Общих друзей нету')
        return 0
    print(f'Всего {len(users_list)} общих друзей:')
    for user in users_list:
        # time.sleep(0.4)
        print(f'{user}  -   {user.first_name} {user.last_name}')


if __name__ == '__main__':
    while True:
        cmd = input('Введите команду - ')
        if cmd == 'cf' or cmd == 'common friends':
            users = input('Введите id пользователей - ').split()    # Вводим id через пробел
            if len(users) > 2 or len(users) == 1 and users[0] != 'end':
                print('Неверный ввод')
                break
            elif len(users) == 1 and users[0] == 'end':
                print('Программа завершена')
                break
            else:
                user1 = VkUser(users[0])
                user2 = VkUser(users[1])
                print_users(user1 & user2)
        elif cmd == 'p' or cmd == 'print':
            id = input('Введите id пользователя - ')
            print(VkUser(id))
        else:
            break
