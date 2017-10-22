import urllib.request
from bs4 import BeautifulSoup
import requests
import facebook
import re
import json
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
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], item["timestamp_img"], item["state"], False,
                  item["fb_post_id"],
                  item["phoneNumber"])
        dddd.append(item)
    return dddd;


def get_new_posts(pr):
    link = pr.findAll('a')
    # if len(link) > 0 and ("LostDogsTennessee" in str(link[0]) or "NewYork" in str(link[0])):  ## For testing
    if len(link) > 0 and "/www.facebook.com/Lost" in str(link[0]):
        pg_id = link[0]['href'].split('/')[3].split('?')[0]
        with open(pg_id + '_output.json', 'w+') as f:
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


# To start the code
# start_code()


# TO RUN ON MULTIPLE THREADS
# from multiprocessing import Process
# for pr in soup.findAll('p'):
# p = Process(target=get_new_posts, args=(pr,))
# p.start()
# x = 0

import random

sam_urls = [
    "http://animalli.com/wp-content/uploads/2016/09/dogs-dog-rottweiler-new-wallpaper-1920x1080.jpg",
    "https://i.pinimg.com/736x/96/78/22/967822c0f1fb9171b424bcf1b765edb5--pom-puppies-cutest-dogs-puppies.jpg",
    "https://cdn.psychologytoday.com/sites/default/files/field_blog_entry_images/2017-09/bored2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ef/Cute_dog_-_Silves_-_ancient_capital_of_Algarve_-_The_Algarve%2C_Portugal_%281388880640%29.jpg",
    "http://2.bp.blogspot.com/-Tfsm19GRWew/VWtb6w47swI/AAAAAAABX84/E7uHzSliHwg/s1600/cute-dogs-075-26.jpg",
    "http://www.thenewsminute.com/sites/default/files/styles/news_detail/public/dog-753269_1280.jpg?itok=dq3BKhqm",
    "https://images.pexels.com/photos/85363/puppy-buddy-look-50mm-85363.jpeg?h=350&auto=compress&cs=tinysrgb",
    "https://media-cdn.tripadvisor.com/media/photo-s/09/5b/64/ad/chiufen-jiufen-old-street.jpg",
    "http://images2.onionstatic.com/clickhole/1892/original/600.jpg",
    "http://bearshapedsphere.com/wp-content/uploads/2012/04/IMG_0101.jpg",
    "http://www.esdaw-eu.eu/uploads/1/0/2/4/10241201/9294877_orig.jpg",
    "http://s1.scoopwhoop.com/cd1/4.JPG",
    "https://cdn.pixabay.com/photo/2016/07/31/12/31/cat-1558863_960_720.jpg",
    "https://1.bp.blogspot.com/-Bmxj1_E_oGs/Vyzj3d3akqI/AAAAAAAABuU/yp7jRobAqXk9kTNLAltKeCpLueHlHqM8ACLcB/s1600/Dogs_1479300f.jpg",
    "https://pbs.twimg.com/media/BozqlBmIIAAoDI-.jpg",
    "http://i.dailymail.co.uk/i/pix/2014/02/24/article-0-1BC8EC0900000578-527_964x585.jpg",
    "https://dncache-mauganscorp.netdna-ssl.com/thumbseg/1364/1364942-bigthumbnail.jpg",
    "https://c4.staticflickr.com/4/3654/3343824492_6695000ebf_z.jpg?zz=1"
]

pet_stat = ["SIGHTING", "MISSING", "FOUND"]


def ran_btw(rang, floating):
    if floating == True:
        return random.uniform(rang[0], rang[1])
    elif floating == "img":
        return random.choice(sam_urls)
    else:
        return random.randint(rang[0], rang[1])


tmp = []


def insert_samp(n):
    for _ in range(n):
        samp = {};
        samp["long"] = ran_btw([-71.113973, -71.039257], True)
        samp["lat"] = ran_btw([42.304662, 42.378863], True)
        samp["url"] = sam_urls[_]
        samp["time"] = ran_btw([1324000, 1328292], False)
        samp["phone"] = "781" + str(ran_btw([1324234, 4000000], False))
        samp["stat"] = random.choice(pet_stat)
        print(samp)
        tmp.append(samp)
        # insertDog(samp["long"], samp["lat"], samp["url"], samp["time"], "Massachusetts", False, "none", samp["phone"],False, samp["stat"])
    print(tmp)
    return

# For inserting sample post
insert_samp(len(sam_urls))
