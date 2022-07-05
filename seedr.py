import requests
import json
from pprint import pprint as pp

class Seedr:

    def __init__(self, access_token=""):
        self.access_token = access_token
        self.session = requests.Session()

    def login(self):

        data = {
            "grant_type" : "password",
            "client_id" : "seedr_chrome",
            "type" : "login",
            "username" : self.username,
            "password" : self.password
        }
        response = self.session.post("https://www.seedr.cc/oauth_test/token.php", data=data)
        if response.status_code != 200:
            return -1
        
        self.access_token = response.json()["access_token"]

    def get_device_code(self):
        response = self.session.get("https://www.seedr.cc/api/device/code?client_id=seedr_xbmc")
        if response.status_code != 200:
            return -1
        return response.json()

    def get_token_from(self, device_code):
        params = {
            "client_id" : "seedr_xbmc",
            "device_code" : device_code
        }
        response = self.session.get("https://www.seedr.cc/api/device/authorize", params=params)
        if response.status_code != 200:
            return -1
        return response.json()

    def set_token(self, token):
        self.access_token = token

    def items(self, folder_id=0):

        params = {
            "access_token" : self.access_token,
        }

        response = self.session.get("https://www.seedr.cc/api/folder/{}/items".format(folder_id), params=params)
        if response.status_code != 200:
            return -1

        return response.json()


    def folder(self, folder_id=""):

        params = {
            "access_token" : self.access_token
        }
        response = self.session.get("https://www.seedr.cc/api/folder/{}".format(folder_id), params=params)
        if response.status_code != 200:
            return -1

        return response.json()

    def download_file(self, file_id):

        data = {
            "access_token" : self.access_token,
            "func" : "fetch_file",
            "folder_file_id" : file_id,
        }
        response = self.session.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if response.status_code != 200:
            return -1

        return response.json()["url"]

    def download_folder(self, folder_id):

        data = {
            "access_token" : self.access_token,
            "func" : "fetch_archive",
            "archive_arr" : json.dumps([{
                "type" : "folder",
                "id" : folder_id
            }])
        }
        response = self.session.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if response.status_code != 200:
            return -1

        return response.json()["archive_url"]

    def delete_folder(self, folder_id):

        data = {
            "access_token" : self.access_token,
            "func" : "delete",
            "delete_arr" : json.dumps([{
                "type" : "folder",
                "id" : folder_id
            }])
        }
        response = self.session.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if response.status_code != 200:
            return -1

        return 0

    def add_torrent(self, magnet):

        data = {
            "access_token" : self.access_token,
            "func" : "add_torrent",
            "torrent_magnet" : magnet,
        }

        response = self.session.post("https://www.seedr.cc/oauth_test/resource.php", data=data)
        if response.status_code != 200 or (not response.json()["result"]):
            return -1

        return response.json()
