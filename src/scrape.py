import urllib.request
from bs4 import BeautifulSoup
import requests
import facebook
import re
import json
from api_requests import *

res = requests.get('https://lostdogsofamerica.org/')
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

graph = facebook.GraphAPI(
    access_token="EAARBTTogYy0BACJh1cCljz1VkpfvRDjspIjuaRcQxIYZCAPe8VX16O0SqG2Vndm0oU1b94Ic3cgrx1VCmHC1V1FbQkSN3sfZBZBfZBDWiiuE3aXZCfuDtSRGni0lorMNoC4ZBoYkzG1xqSt9TBRribSDGHWqrpGRUOKlIIQhwEcEfzNByHKIALIBDt8Oxszw3WmbwYUsUi0gZDZD",
    version=2.10)


def get_phone(str):
    nums = re.findall((r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'), str)
    if (len(nums) > 0):
        num = [num for num in nums if len(num) >= 9]
        if len(num) > 0:
            return re.sub('[^0-9]', '', num[0])
    else:
        return 0


def reform(fb_res):
    toRet = {}
    toRet["geo_long"] = 0.0
    toRet["geo_lat"] = 0.0
    if 'picture' in fb_res:
        toRet["img_url"] = fb_res["picture"]
    else:
        toRet["img_url"] = "none"
    toRet["timestamp_img"] = fb_res["created_time"]
    toRet["nuetered"] = "none"
    toRet["fb_post_id"] = fb_res["id"]
    if 'message' in fb_res:
        toRet["phoneNumber"] = get_phone(fb_res["message"])
    else:
        toRet["phoneNumber"] = "none"

    if 'state' in fb_res:
        toRet["state"] = fb_res["state"]
    else:
        toRet["state"] = fb_res["from"]["name"].split(" ")
    return toRet;


def scrape(pg_id):
    dddd = []
    item = graph.get_object(id=pg_id, fields='feed', limit=100)["feed"]["data"]
    fb_res = [graph.get_object(i["id"],
                               fields='from, message, permalink_url, place, link, picture, created_time, description, application')
              for i in item]
    for item in fb_res:
        item = reform(item)
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], 100000, False, item["fb_post_id"])
        dddd.append(item)
    # insertBatchDog(dddd)

    return dddd;
# (geo_long, geo_lat, img_url, timestamp_img, nuetered, fb_post_id, phone_number)

from multiprocessing import Process


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


for pr in soup.findAll('p'):
    p = Process(target=get_new_posts, args=(pr,))
    p.start()

print("\n\n")

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp()


# imageList = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]

# Search using a URL
# search = app.inputs.search_by_image(
#     url='http://cdn2-www.dogtime.com/assets/uploads/gallery/german-shepherd-dog-breed-pictures/standing-7.jpg')
# print([images.url for images in search if images.score >= 0.59])


# with open('dataset.json', 'r+') as f:
#     data = json.load(f)
#     data['id'] = []  # <--- add `id` value.
#     f.seek(0)  # <--- should reset file position to the beginning.
#     json.dump(data, f, indent=4)
#     f.truncate()  # remove remaining part


def getTop_matches(threshold, pet_data):
    if pet_data["state"].lower() == 'colorado':
        pet_data["state"] = "Co"
    f_name = "LostDogs" + pet_data["state"] + '_output.json'
    print(f_name)
    with open(f_name) as f:
        print(f)
        try:
            data = json.load(f)
        except ValueError:
            data = []
            print(data)
        imageList = [ClImage(url=pet["picture"]) for pet in data]
        img_search = app.inputs.search_by_image(url=pet_data["picture"])
        print(imageList)
        if len(img_search) > 0:
            return img_search
            # return [img_search.url for images in img_search if images.score >= threshold]
        else:
            return []


dt = {
    "description": "This article backs up our recommendation to NOT offer a reward online for your missing pet.  In addition, we want to remind you that you do not need to pay any website or service to list your missing pet.  There are many, many FREE services like HelpingLostPets.com that will list your pet for FREE. And we are also partnered with many amazing volunteer groups across the country.\n\nhttps://www.timeslive.co.za/news/south-africa/2017-10-16-beware-social-media-scammers-when-posting-a-reward-for-lost-pets/",
    "id": "1724090464482250_2410902259134397",
    "created_time": "2017-10-20T16:14:32+0000",
    "picture": "https://external.xx.fbcdn.net/safe_image.php?d=AQB_GMq7EuxjVdq-&w=130&h=130&url=https%3A%2F%2Flh3.googleusercontent.com%2FxdueXhNlC5WHrs6epxdOJn3O2TTH5wCEq-y2AyQaM2SD7OxEludQ1reSIVXqdQxvU9jhHFymcfh1NLCM_6HmjA%3Ds1000&cfs=1&_nc_hash=AQCKMEIV1GmxvKTc",
    "from": {
        "id": "1724090464482250",
        "name": "Lost Dogs Alabama"
    },
    "state": "Alabama",
    "link": "https://www.timeslive.co.za/news/south-africa/2017-10-16-beware-social-media-scammers-when-posting-a-reward-for-lost-pets/",
    "message": "This article backs up our recommendation to NOT offer a reward online for your missing pet. In addition, we want to remind you that you do not need to pay any website or service to list your missing pet. There are many, many FREE services like HelpingLostPets.com that will list your pet for FREE. And we are also partnered with many amazing volunteer groups across the country.\nhttps://www.timeslive.co.za/\u2026/2017-10-16-beware-social-med\u2026/",
    "permalink_url": "https://www.facebook.com/LostDogsAlabama/posts/2410902259134397"
}
getTop_matches(0, dt)


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


sample_post_body = {
    "from": "",
    "place": "",
    "link": "",
    "picture": "",
    "created_time": "",
    "description": "",
    "application": "",
    "state": ""
}
