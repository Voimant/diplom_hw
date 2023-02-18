import requests
from pprint import pprint
import json
import time
import pyprind
import configparser



class VkbackUp():
    def __init__(self,token: str):
        self.token = token

    def get_list_photo(self,id_album: str, id_user: str):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id':id_user,
                  'album_id': id_album,
                  'access_token':self.token,
                  'extended': "1",
                  'count': '6',
                  'v': '5.131'}


        response = requests.get(url,params=params)
        return response.json()

    def get_unpack_photo(self,vk_json):
        """принимает 1 аргумент, json файл от метода photo.get vk
        возвращает список альбомов"""

        album = vk_json['response']['items']

        return album


    def get_list(self,album):
        """принимает 1 аргумет, список альбомов из get_unpack_photo,
        возвращает список словарей с названиями фото по лайкам"""
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        pack = []
        for photo in album:
            name = {}
            name['name'] = photo['likes']['count']
            sizes = max(photo['sizes'], key=lambda x: vk_sizes[x["type"]])
            name['type'] = sizes['type']
            name['url'] = sizes['url']
            pack.append(name)


        return pack

    def get_for_json(self,album):
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        p = []
        for photo in album:
            name = {}
            size = max(photo['sizes'], key=lambda x: vk_sizes[x["type"]])
            name['name'] = photo['likes']['count']
            name['type'] = size['type']
            p.append(name)
        return p



class YaMyloader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
                }

    #
    def get_file_list(self):
        file_list_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(file_list_url,headers=headers)
        return response.json()


    def get_create_folder(self,path):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        response = requests.put(f'{folder_url}/?path={path}',headers=headers)


    def _link_load_file(self,disk_file_path):
        """получаем ссылку на загрузку файла"""
        link_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(link_url, headers=headers, params=params)
        return response.json()


    def load_file(self,disk_file_path,file_name):
        result = self._link_load_file(disk_file_path=disk_file_path)
        url = result.get('href')
        response = requests.put(url, data=open(file_name,'rb'))
        response.raise_for_status()
        if response.raise_for_status() == 201:
            print('victory!!!')


    def load_url_file(self,pack,folder_name):
        """скачивание с урла"""
        bar = pyprind.ProgBar(len(pack))
        link_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for link_file in pack:
            params = {'url': link_file['url'],
                      'path': f"{folder_name}/{str(link_file['name'])}"}
            requests.post(link_url,headers=headers, params=params)
            try:
                response = requests.get(link_file['url'])
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print("фото по данному URL, не существует")
                print(link_file['url'])
            bar.update()

def get_save_json(file):
    with open("name_list.json", 'w') as f:
        json.dump(file,f, ensure_ascii=False, indent=2)


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('cfg.ini')
    config.sections()
    TOKEN_VK = config['DEFAULT']['TOKEN_VK']
    TOKEN_YA = config['DEFAULT']['TOKEN_YA']
    # Даннные на вход
    vk = VkbackUp(token=TOKEN_VK)
    ya = YaMyloader(token=TOKEN_YA)
    folder_name = 'vk_backup' # название папки на Яндекс диске
    res = vk.get_list_photo('profile','551501510') # Сюда пожалуйста во второй аргумент ваш ID ВК

    unpack = vk.get_unpack_photo(res)
    name_list_size = vk.get_list(unpack)
    for_json = vk.get_for_json(unpack)
    get_save_json(for_json)
    ya.get_create_folder(folder_name)
    ya.load_url_file(name_list_size,folder_name)







    # 551501510
