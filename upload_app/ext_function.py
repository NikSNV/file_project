import os

import requests
from django.core.files import File


def get_name(url_str):
    # Имя файла без пути
    nom_slesh = url_str.rfind('/')
    str_file = url_str[nom_slesh + 1:]
    return str_file


def create_img_url(url, file):

    if file:
        name = get_name(str(file['file']))
        data = {'picture': file['file'], 'name': name}
        return data

    if url:
        all_data = {'picture': '', 'name': ''}
        img = requests.get(url, stream=True)
        name = get_name(str(url))
        img_temp = open(name, 'wb')
        img_temp.write(img.content)
        img_temp.close()
        all_data['picture'] = File(open(img_temp.name, "rb"))
        os.remove(img_temp.name)
        all_data['name'] = name
        return all_data
