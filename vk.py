import time
import requests
from urllib.parse import urlencode

# url_authorize = 'https://oauth.vk.com/authorize'
# auth_date = {'client_id': 6112358, 'display': 'mobile', 'redirect_uri': 'https://oauth.vk.com/blank.html',
#              'scope': 'friends', 'v':'5.67','response_type':'token'}
# ulr_token = ('?'.join((url_authorize, urlencode(auth_date))))


with open('../vk_token.txt') as f:
    token = f.read()


def account_friends(token):
    params = {'access_token': token, 'v': '5.67', 'fields': 'first_name,last_name'}
    r_profile = requests.get('https://api.vk.com/method/account.getProfileInfo', params).json()
    r_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
    account_friends = []
    friends_id = []
    for i in r_friends['response']['items']:
        account_friends.append(f"{i['last_name']} {i['first_name']}")
        friends_id.append(i['id'])

    print('Список друзей аккаунта {} {}'.format(r_profile['response']['first_name'], r_profile['response']['last_name']),
          '\nВсего {} человека - {}'.format(r_friends['response']['count'], ', '.join(account_friends)))
    return friends_id


def friends_friends(token):
    counter = 0
    set_fridens_fridens = set()
    friends_id = account_friends(token)
    with open('friends_friends.txt', 'w', encoding='utf-8') as f:
        print('\nОжидайте, данные записываются в файл {} ...'.format(f.name))
        for i in friends_id:
            params = {'access_token': token, 'v': '5.67', 'fields': 'first_name,last_name', 'user_id': i}
            r_user_profil = requests.get('https://api.vk.com/method/users.get', params).json()
            r_user_fridens = requests.get('https://api.vk.com/method/friends.get', params).json()
            time.sleep(1)
            counter += r_user_fridens['response']['count']
            f.write('{} {} - {}друзей. \n'.format(r_user_profil['response'][0]['first_name'], r_user_profil['response'][0]['last_name'], r_user_fridens['response']['count']))
            for i in r_user_fridens['response']['items']:
                f.write(i['first_name']+' '+i['last_name']+', ')
                set_fridens_fridens |= {i['id']}
            f.write('\n---------------\n')
        f.write('\nОбщее колво всех друзей - {}. \nУникальных друзей - {}.'.format(counter, len(set_fridens_fridens)))
    print('Данные успешно записаны\n', '\nОбщее колво всех друзей - {}. \nУникальных друзей - {}.'.format(counter, len(set_fridens_fridens)))

friends_friends(token)
