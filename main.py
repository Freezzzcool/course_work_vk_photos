from vk_api_class import VKAPI
from yandex_api_class import YandexAPI
from tqdm import tqdm
import json
import requests
import configparser

""" Заполните файл example.ini перед работой """

def read_ini():
    """
    Получение токенов из конфигурационного файла
    :return: кортеж с токенами
    """
    config = configparser.ConfigParser()
    config.read("example.ini", encoding="utf-8")
    vk = config["TOKEN"].get("vk")
    ya = config["TOKEN"].get("ya")

    return vk, ya

def input_user_id(vk_token):
    """
    Получение id от пользователя
    """
    user_id = input('Введите id или screen_name пользователя VK: ')
    vk_access = VKAPI(vk_token, user_id)
    user_id = vk_access.get_user_id()

    return user_id, vk_access

def input_amount_photo_to_save():
    """
    Получения количества фото для загрузки от пользователя (по умолчанию 5).
    """
    amount_photo = input('Введите количество фото, которые вы хотите сохранить в облаке\n'
                         '(при некорректном вводе будет принято значение по умолчанию - 5): ')
    if amount_photo.isdigit() and int(amount_photo) > 0:
        return int(amount_photo)
    else:
        print('Некорректный ввод. Придется сохранить 5 фото :)')
        return 5

def get_url_for_upload_from_yandexapi(yad_access, path):
    """
    Получение ссылки для загрузки файла на диск
    :param yad_access: экземпляр класса яндекс API
    :param path: путь, по которому следует загрузить файл
    :return: возвращает ссылку для загрузки файла, и headers
    """

    return yad_access.get_url_for_upload(path)

def upload_file_json_with_yandexapi(yad_access, data, path):
    """
    Загрузка файла на диск
    :param yad_access: экземпляр класса яндекс API
    :param data: данные для записи в файл json и загрузки на диск
    :param path: путь, по которому следует загрузить файл
    :return: статус запроса
    """
    url_for_upload, headers = get_url_for_upload_from_yandexapi(yad_access, f'{path}/result.json')
    with open('result.json', 'w') as f:
        json.dump(data, f, indent=4)
    with open('result.json') as f:
        response = requests.put(url_for_upload,
                     headers=headers)

    return response

def main_func():
    vk_token, ya_token = read_ini()
    user_id, vk_access = input_user_id(vk_token)
    yad_access = YandexAPI(ya_token)
    all_photo_and_url_dict, info_photos_for_json_file = vk_access.get_name_photo_and_url(input_amount_photo_to_save())
    yad_access.create_new_folder(user_id)
    for name_photo, url_photo in tqdm(all_photo_and_url_dict.items()):  # прогресс-бар для галочки
        yad_access.upload_photo(url_photo, f'{user_id}/{name_photo + '.jpg'}')
    upload_file_json_with_yandexapi(yad_access, info_photos_for_json_file, user_id)
    print('Загрузка завершена')

main_func()
