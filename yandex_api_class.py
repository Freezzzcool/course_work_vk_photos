import requests


class YandexAPI:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'OAuth {token}'}

    def create_new_folder(self, name_folder):
        """
        Создание папки в яндекс диске
        :param name_folder: путь к новой папке
        :return: статус запроса
        """
        response = requests.put(self.API_BASE_URL,
            params={'path': name_folder},
            headers=self.headers)

        return response

    def upload_photo(self, url_source, path):
        """
        Загрузка фото на диск
        :param url_source: ссылка на загружаемое фото
        :param path: путь к папке, в которую нужно загрузить фото
        :return: статус запроса
        """
        response = requests.post(self.API_BASE_URL + '/upload',
                                 params={
                                     'url': url_source,
                                     'path': path},
                                 headers=self.headers)

        return response

    def get_url_for_upload(self, path):
        """
        Получение ссылки для загрузки файла на диск
        :param path: путь, по которому следует загрузить файл
        :return: ссылка для загрузки файла
        """
        response = requests.get(self.API_BASE_URL + '/upload',
                                params={'path': path},
                                headers=self.headers)

        return response.json()['href'], self.headers
