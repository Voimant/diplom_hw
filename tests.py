import requests
from pprint import pprint
import json




TOKEN = "vk1.a.u9bnCQbWa7YR08urFndcZdjxHAvObPUpE-Sc_nUWOvxqfwfUSz8Z91lyW1bPAaB1g7V0uxtDeE9gyOGT4jjg7aklFyq8zDbmJkQiuETeOzP0JCfxQJMq12pL5m3Mq_NJrP_VKkV1zh0oNLa-CFPosH-it651J65FkGp3eStHTtgVVAOir25Xu2NJSqQHmDXUIstIBdUyZPtznrzK6_JVSQ"




class VkbackUp():
    def __init__(self,token: str):
        self.token = token

    def get_list_photo(self,id_album: str, id_user: str):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id':id_user,
                  'album_id': id_album,
                  'access_token':self.token,
                  'extended': "1",
                  'v': '5.131'}


        response = requests.get(url,params=params)
        return response.json()

    def get_unpack_photo(self,):
        """принимает 1 аргумент, json файл от метода photo.get vk
        возвращает список альбомов"""

        list_albums = vk_json['response']['items']
        return list_albums





if __name__ == '__main__':
    vk = VkbackUp(TOKEN)


    res = vk.get_list_photo('profile', '1')
    pprint(res)
    #
    # [{'file_name': 721337, 'size': 'z'},
    #  {'file_name': 978769, 'size': 'w'},
    #  {'file_name': 873739, 'size': 'w'},
    #  {'file_name': 664427, 'size': 'x'},
    #  {'file_name': 753201, 'size': 'z'},
    #  {'file_name': 598877, 'size': 'w'},
    #  {'file_name': 1475537, 'size': 'z'},
    #  {'file_name': 574726, 'size': 'z'},
     # {'file_name': 269411, 'size': 'z'}]