from urllib.request import urlopen
import requests
import json

VK_API_VERSION = '5.103'


# TODO: handle request errors

def get_photo_server_link(token, group_id):
    method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    data = {
        'access_token': token,
        'gid': group_id,
        'v': VK_API_VERSION
    }
    response = requests.post(method_url, data).json()
    return response['response']['upload_url']


def upload_photo_to_server(vk_photo_url, img_bytes):
    img = {'photo': ('img.jpg', img_bytes)}
    response = requests.post(vk_photo_url, files=img).json()
    return {
        'photo': response['photo'],
        'hash': response['hash'],
        'server': response['server']
    }


def save_photo_on_vk_server(token, group_id, photo, hash, server):
    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    data = {
        'access_token': token,
        'gid': group_id,
        'photo': photo,
        'hash': hash,
        'server': server,
        'v': VK_API_VERSION
    }
    response = requests.post(method_url, data).json()
    return response['response'][0]['id'], response['response'][0]['owner_id']


def post_to_vk_wall(owner_id, group_id, photo_id, token, message_text):
    method_url = 'https://api.vk.com/method/wall.post?'

    attachements_data = 'photo{}_{}'.format(owner_id, photo_id)
    data = {
        'access_token': token,
        'owner_id': '-' + str(group_id),
        'attachments': attachements_data,
        'message':message_text,
        'v': VK_API_VERSION
    }
    requests.post(method_url, data).json()
