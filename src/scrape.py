from bs4 import BeautifulSoup
import requests
import facebook
import re
from src.api_requests import *
import time

res = requests.get('https://lostdogsofamerica.org/')
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

graph = facebook.GraphAPI(
    access_token="EAACEdEose0cBAHtjJlIBgv9wJ9l9EdfSeDKwhLRxmeBK3dWGdZCu3T5gOj1opetFZAGcR8ZB2ijqgmBehcivjMnzq7eeZBTqm8VXrpjMR2ZBOHJkk1r1dL9hn5hXBWfPn9U6hhm3ad2mReVXi9bf8g2S2ZAg9OLGexXnbXrhxTZCaOYmZAZBuz11LkMLMCjZCPDAFkhoIJrH2IrAZDZD",
    version=2.10)


def get_phone(str):
    nums = re.findall((r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'), str)
    if (len(nums) > 0):
        num = [num for num in nums if len(num) >= 9]
        if len(num) > 0:
            return re.sub('[^0-9]', '', num[0])
        else:
            return "none"
    else:
        return "none"


def reform(fb_res):
    toRet = {}
    toRet["geo_long"] = 0.0
    toRet["geo_lat"] = 0.0
    if 'picture' in fb_res:
        toRet["img_url"] = fb_res["picture"]
    else:
        toRet["img_url"] = "none"

    pattern = '%Y-%m-%dT%H:%M:%S'
    epoch = int(time.mktime(time.strptime(fb_res["created_time"].split("+")[0], pattern)))
    toRet["timestamp_img"] = epoch
    toRet["nuetered"] = "none"
    toRet["fb_post_id"] = fb_res["id"]
    if 'message' in fb_res:
        toRet["phoneNumber"] = get_phone(fb_res["message"])
    else:
        toRet["phoneNumber"] = "none"

    if 'state' in fb_res:
        toRet["state"] = fb_res["state"]
    else:
        toRet["state"] = fb_res["from"]["name"].split(" ")[len(fb_res["from"]["name"].split(" ")) - 1]
    return toRet;


def scrape(pg_id):
    count = 0;
    dddd = []
    item = graph.get_object(id=pg_id, fields='feed', limit=80)["feed"]["data"]
    fb_res = [graph.get_object(i["id"],
                               fields='from, message, permalink_url, place, link, picture, created_time, description, application')
              for i in item]
    for item in fb_res:
        item = reform(item)
        print(count)
        count += 1
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], item["timestamp_img"],item["state"], False, item["fb_post_id"],
                  item["phoneNumber"])
        dddd.append(item)
    return dddd;


def get_new_posts(pr):
    link = pr.findAll('a')
    # if len(link) > 0 and ("LostDogsTennessee" in str(link[0]) or "NewYork" in str(link[0])):  ## For testing
    if len(link) > 0 and "/www.facebook.com/Lost" in str(link[0]):
        pg_id = link[0]['href'].split('/')[3].split('?')[0]
        with open("scraper/"+pg_id + '_output.json', 'w+') as f:
            try:
                data = json.load(f)
            except ValueError:
                data = []
            data = data + scrape(pg_id)
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part


# Main entry point
def start_code():
    for pr in soup.findAll('p'):
        get_new_posts(pr)


# start_code()

# TO RUN ON MULTIPLE THREADS
# from multiprocessing import Process
# for pr in soup.findAll('p'):
# p = Process(target=get_new_posts, args=(pr,))
# p.start()
# x = 0


