import time
import requests
import json

with open('./vk_token.txt') as f:
    token = f.read()


USER_ID = input("Введите имя или ID пользователя: ")


def account_friends(token):
    params = {'access_token': token, 'v': '5.67', 'fields': 'first_name,last_name', 'user_id': USER_ID, 'extended': 1}
    r_profile = requests.get('https://api.vk.com/method/users.get', params).json()
    r_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
    r_groups = requests.get('https://api.vk.com/method/groups.get', params).json()

    acc_friends = [{i['last_name']: i['first_name']} for i in r_friends['response']['items']]
    friends_id = [i['id'] for i in r_friends['response']['items']]
    groups_id = [i['id'] for i in r_groups['response']['items']]

    print('Список друзей пользователя {} {}'.format(r_profile['response'][0]['first_name'],
                                                    r_profile['response'][0]['last_name']),
          '\nВсего {} человека - {}'.format(r_friends['response']['count'], acc_friends))
    print('Группы, в которых состоит наш пользователь: {}.\nВсего групп - {}.\n'.format(
        '; '.join([i['name'] for i in r_groups['response']['items']]), r_groups['response']['count']))
    return friends_id, groups_id


def groups_friends(token):
    friends_id, groups_id = account_friends(token)
    print('\nОжидайте, данные обрабатываются ...\nНомер шага соответсвует номеру друга и их не может быть более чем {}'.format(
        len(friends_id)))
    counter = 0
    for j, i in enumerate(friends_id, start=1):
        try:
            params = {'access_token': token, 'v': '5.67', 'fields': 'first_name,last_name', 'user_id': i, 'extended': 1}
            r_groups = requests.get('https://api.vk.com/method/groups.get', params).json()
            time.sleep(0.4)
            friend_groups_id = [i['id'] for i in r_groups['response']['items']]
            groups_id = set(groups_id) - set(friend_groups_id)
            if counter != len(groups_id):
                counter = len(groups_id)
                print(f'Шаг {j}. Колво индивидуальных групп - {counter}')
                print(f'Осталось обработать {len(friends_id)-j}')
            if len(groups_id) == 0:
                break
        except KeyError:
            continue
    print('----------------------------------')
    return groups_id


def output_data(token):

    counter = groups_friends(token)
    if len(counter) > 0:
        print('Данные успешно обработаны\n', 'Колво индивидуальных групп - {}шт.\n'.format(len(counter)))
    else:
        print('Данные успешно обработаны\n Индивидуальных групп НЕТ!')

    individ_groups = requests.get('https://api.vk.com/method/groups.getById',
                            {'group_ids': ','.join(list(map(str, counter))), 'fields': 'members_count'}).json()

    for i in individ_groups['response']:  # Вот тут у меня ерунда. 2-мя способами сделал и ни один мне не нравится!!
        del (i['screen_name'], i['is_closed'], i["photo"], i["photo_medium"], i["photo_big"], i["type"])
        # list.append({'gid': i['gid'], 'name':i['name'],'members_count': i['members_count'] })

    with open('individual_groups.json', 'w', encoding='utf-8') as f:
        json.dump(individ_groups['response'], f, indent=2, ensure_ascii=False)
        print('Индивидуальные группы записаны в файл {}'.format(f.name))


def main():
    output_data(token)


if __name__ == '__main__':
    main()
