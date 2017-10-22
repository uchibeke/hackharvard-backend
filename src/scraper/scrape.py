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
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], item["timestamp_img"],item["state"], False, item["fb_post_id"],
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


start_code()

# TO RUN ON MULTIPLE THREADS
# from multiprocessing import Process
# for pr in soup.findAll('p'):
# p = Process(target=get_new_posts, args=(pr,))
# p.start()
# x = 0


print("\n\n")

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp()

imageList = []


# imageList  = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]
# imageList = []
# app.inputs.bulk_create_images(imageList)
# print(imageList)

# Search using a URL
# search = app.inputs.search_by_image(
#     url='http://cdn2-www.dogtime.com/assets/uploads/gallery/german-shepherd-dog-breed-pictures/standing-7.jpg')
# print([images.url for images in search if images.score >= 0.59])


def getTop_matches(threshold, pet_data):
    if pet_data["state"].lower() == 'colorado':
        pet_data["state"] = "Co"
    f_name = "LostDogs" + pet_data["state"] + '_output.json'

    with open(f_name) as f:
        try:
            data = json.load(f)
        except ValueError:
            data = []
    for pet in data:
        imageList.append(ClImage(url=pet["img_url"]))
    # app.inputs.bulk_create_images(imageList)
    print(pet_data["img_url"])
    img_search = app.inputs.search_by_image(url=pet_data["img_url"])
    print("\n\n")
    if len(img_search) > 0:
        return [{"url": image.url, "score": image.score} for image in img_search if image.score > threshold]
    else:
        return []

pet_item = {
    "img_url": "http://cdn1-www.dogtime.com/assets/uploads/gallery/yorkshireterrier-dog-breed-pictures/1-face.jpg",
    "geo_long": 0.0,
    "timestamp_img": "2017-10-20T16:14:32+0000",
    "state": "Alabama",
    "nuetered": "none",
    "phoneNumber": 0,
    "geo_lat": 0.0,
    "fb_post_id": "1724090464482250_2410902259134397"
}

print(getTop_matches(0.3, pet_item))

def add_to_dataset(new_pet):
    with open('dataset.json', 'r+') as f:
        data = json.load(f)
        state_data = data['LostDogs' + new_pet["state"]]
        state_data.append[new_pet]
        data['LostDogs' + new_pet["state"]] = state_data
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
        # data_set.append(ClImage(url=new_pet["picture"]))  # post format
