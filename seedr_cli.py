#!/usr/local/bin python3

from seedr import Seedr
import sys
import os
import configparser

dir_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(dir_path, "config.ini")

def get_token_flow():
    s = Seedr()
    result = s.get_device_code()
    if result == -1:
        print(" [!] ERROR: could not get device code")
    device_code = result["device_code"]
    user_code = result["user_code"]
    print(" [+] paste the user code at https://seedr.cc/devices")
    print(" [+] user_code: {}".format(user_code))
    input(" [+] press enter when you're done")

    result = s.get_token_from(device_code)
    if result == -1:
        print(" [!] ERROR: could not get access token")
    token = result["access_token"]
    print(" [+] this is your access token: {}".format(token))
    store_token(token)
    print(" [+] the access_token has been stored in the config.ini file")

def store_token(token):
    config_text = "[DEFAULT]\nTOKEN={}\n".format(token)
    f = open(config_path, "w")
    f.write(config_text)
    f.close()

config = configparser.ConfigParser()

if (not os.path.exists(config_path)):
    get_token_flow()

config.read(config_path)
TOKEN = config["DEFAULT"]["TOKEN"]
seed = Seedr(TOKEN)

def add_magnet(magnet_link):
    print(" [+] adding magnet...")
    result = seed.add_torrent(magnet_link)
    if result == -1:
        print(" [!] ERROR: torrent was not added")
        exit(1)
    else:
        print(" [+] SUCCESS!")

def list_items(folder_id=None):
    if folder_id is None:
        status = seed.items()
    else:
        status = seed.items(folder_id)
    if status == -1:
        print(" [!] ERROR: could not retrieve status")
        exit(1)
    if len(status["torrents"]) > 0:
        print(" [+] torrents")
        for t in status["torrents"]:
            print("      * [{}] [{}%] {}".format(t["id"], float(t["progress"]), t["name"]))
    if len(status["folders"]) > 0:
        print(" [+] folders")
        for f in status["folders"]:
            print("      * [{}] {}".format(f["id"], f["name"]))
    if len(status["files"]) > 0:
        print(" [+] files")
        for f in status["files"]:
            file_id = f["id"] if "id" in f else f["folder_file_id"]
            print("      * [{}] {}".format(file_id, f["name"]))

def get_link(item_id):
    print(" [+] fetching download link...")
    item_id = item_id.strip()
    result = None
    if len(item_id) == 9:
        result = seed.download_folder(item_id)
    else:
        result = seed.download_file(item_id)
    if result == -1:
        print(" [!] ERROR: link could not be fetched")
        exit(1)
    else:
        print("     {}".format(result))

def delete_folder(item_id):
    print(" [+] deleting folder...")
    result = seed.delete_folder(item_id)
    if result == -1:
        print(" [!] ERROR: link could not be fetched")
        exit(1)
    else:
        print(" [+] SUCCESS!")

if len(sys.argv) < 2:
    exit(1)

command = sys.argv[1]

if command == "add":
    if len(sys.argv) < 3:
        print(" [!] usage: seedr add <magnet_link>")
        exit(1)
    magnet_link = sys.argv[2]
    add_magnet(magnet_link)
elif command == "list":
    if len(sys.argv) < 3:
        list_items()
    else:
        folder_id = sys.argv[2]
        list_items(folder_id)
elif command == "link":
    if len(sys.argv) < 3:
        print(" [!] usage: seedr link <id>")
        exit(1)
    item_id = sys.argv[2]
    get_link(item_id)
elif command == "rm":
    if len(sys.argv) < 3:
        print(" [!] usage: seedr link <id>")
        exit(1)
    item_id = sys.argv[2]
    delete_folder(item_id)
else:
    print(" [!] ERROR: invalid command '{}'".format(command))
    exit(1)

