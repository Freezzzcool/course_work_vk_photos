import requests
from time import strftime, gmtime


class VKAPI:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.vk_id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_users_info(self):
        """
        Получения информации о пользователе.
        (используется для проверки доступа)
        :return: статус запроса
        """
        params = {'user_ids': self.vk_id}
        response = requests.get(self.API_BASE_URL + '/users.get',
                                params={**self.params, **params})

        return response

    def get_user_id(self):
        """
        :return: возвращает id пользователя
        """
        return str(self.get_users_info().json()['response'][0]['id'])

    def get_name_photo_and_url(self, amount=5):
        """
        :param amount: количество фото, которые нужно получить
        :return: возвращает словарь фото и ссылки из профиля
        """
        params = {
            'album_id': 'profile',
            'extended': 1,
            'count': amount,
            'owner_id': self.get_user_id(),
            'photo_sizes': 1}
        response = requests.get(self.API_BASE_URL + '/photos.get',
                                params={**self.params, **params})
        amount_photos = int(response.json()['response']['count'])
        if amount_photos > amount:
            amount_photos = amount
        all_photo_and_url_dict = {}
        info_photos_for_json_file = []
        for _ in range(amount_photos):
            date = float(response.json()['response']['items'][_]['date'])
            max_size = 'A'
            current_url = ''
            photo_size_type = ''
            for photo in response.json()['response']['items'][_]['sizes']:
                if photo['type'] > max_size:
                    max_size = photo['type']
                    current_url = photo['url']
                    photo_size_type = photo['type']
            likes = response.json()['response']['items'][_]['likes']['count']
            file_name = str(likes) + '_likes|' + str(
                strftime("%B %d %Y", gmtime(date))).replace(' ', '_')
            all_photo_and_url_dict[file_name] = current_url
            info_photos_for_json_file.append({'file_name': f'{file_name}.jpg', 'size': photo_size_type})

        return all_photo_and_url_dict, info_photos_for_json_file
