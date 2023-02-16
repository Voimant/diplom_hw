import requests
from pprint import pprint
import json




TOKEN =



class VkbackUp():
    def __init__(self,token: str):
        self.token = token

    def get_list_photo(self,id_album: str, id_user: str):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id':id_user,
                  'album_id': id_album,
                  'access_token':self.token,
                  'extended': "1",
                  'count': '5',
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
        vk_sizes = ['w', 'z', 'y', 'x', 'm', 's']
        pack = []
        si = []
        for photo in album:
            size = {}
            size['name'] = photo['likes']['count']
            pack.append(size)


        return pack


    def max_size(self,album):
        vk_sizes = ['w', 'z', 'y', 'x', 'm', 's']


        p = []
        for vk_size in vk_sizes:
            for x in album:
                for y in x['sizes']:
                    if vk_size in y['type']:
                        p.append(y)
                        break
        return p








        # vk_sizes = ['w','z','y','x','m','s']
#'wzyrqpoxms'
        # pprint(puck_for_load)
            # with open('data.txt', 'w') as outfile:
            #     json.dump(name_dict, outfile)

if __name__ == '__main__':
    #Даннные на вход
    vk = VkbackUp(TOKEN)
    res = vk.get_list_photo('profile','1')

    # тело

    unpack = vk.get_unpack_photo(res)
    name_list_size = vk.get_list(unpack)
    max_list = vk.max_size(unpack)
    pprint(max_list)
    pprint(name_list_size)