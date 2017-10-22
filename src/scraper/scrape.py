import urllib.request
from bs4 import BeautifulSoup
import requests
import facebook
import re
import json
<<<<<<< HEAD
from ..api_requests import *
=======
from src.api_requests import *
import time;
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f

res = requests.get('https://lostdogsofamerica.org/')
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

graph = facebook.GraphAPI(
<<<<<<< HEAD
    access_token="EAARBTTogYy0BACJh1cCljz1VkpfvRDjspIjuaRcQxIYZCAPe8VX16O0SqG2Vndm0oU1b94Ic3cgrx1VCmHC1V1FbQkSN3sfZBZBfZBDWiiuE3aXZCfuDtSRGni0lorMNoC4ZBoYkzG1xqSt9TBRribSDGHWqrpGRUOKlIIQhwEcEfzNByHKIALIBDt8Oxszw3WmbwYUsUi0gZDZD",
=======
    access_token="EAACEdEose0cBAEryIZACUchzSu9fYXIhLEbPlALMERbPWMmBuIKZChjQouia2bGFwJEPJzFsYO8yaB3ZBf96BBuR3gUx1wzW66xKFRBbvObBQOvEWXYksKZBkJfPogrelcRJhULvPmwIpdg50FCbeqnvyDZBvW9JiDo1UY9jdryYAZChZCC9BrVnaWn8fZATI2sZD",
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
    version=2.10)


def get_phone(str):
    nums = re.findall((r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'), str)
    if (len(nums) > 0):
        num = [num for num in nums if len(num) >= 9]
        if len(num) > 0:
            return re.sub('[^0-9]', '', num[0])
<<<<<<< HEAD
    else:
        return 0
=======
        else:
            return "none"
    else:
        return "none"
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f


def reform(fb_res):
    toRet = {}
    toRet["geo_long"] = 0.0
    toRet["geo_lat"] = 0.0
    if 'picture' in fb_res:
        toRet["img_url"] = fb_res["picture"]
    else:
        toRet["img_url"] = "none"
<<<<<<< HEAD
    toRet["timestamp_img"] = fb_res["created_time"]
=======
    pattern = '%Y-%m-%dT%H:%M:%S'
    epoch = int(time.mktime(time.strptime(fb_res["created_time"].split("+")[0], pattern)))
    toRet["timestamp_img"] = epoch
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
    toRet["nuetered"] = "none"
    toRet["fb_post_id"] = fb_res["id"]
    if 'message' in fb_res:
        toRet["phoneNumber"] = get_phone(fb_res["message"])
    else:
        toRet["phoneNumber"] = "none"

    if 'state' in fb_res:
        toRet["state"] = fb_res["state"]
    else:
<<<<<<< HEAD
        toRet["state"] = fb_res["from"]["name"].split(" ")
=======
        toRet["state"] = fb_res["from"]["name"].split(" ")[len(fb_res["from"]["name"].split(" ")) - 1]
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
    return toRet;


def scrape(pg_id):
<<<<<<< HEAD
    dddd = []
    item = graph.get_object(id=pg_id, fields='feed', limit=100)["feed"]["data"]
=======
    count = 0;
    dddd = []
    item = graph.get_object(id=pg_id, fields='feed', limit=80)["feed"]["data"]
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
    fb_res = [graph.get_object(i["id"],
                               fields='from, message, permalink_url, place, link, picture, created_time, description, application')
              for i in item]
    for item in fb_res:
        item = reform(item)
<<<<<<< HEAD
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], 100000, False, item["fb_post_id"])
        dddd.append(item)
    # insertBatchDog(dddd)

    return dddd;
# (geo_long, geo_lat, img_url, timestamp_img, nuetered, fb_post_id, phone_number)
=======
        print(count)
        count += 1
        insertDog(item["geo_long"], item["geo_lat"], item["img_url"], item["timestamp_img"], False, item["fb_post_id"],
                  item["phoneNumber"])
        dddd.append(item)

    return dddd;
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f



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


        # start_code()

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

<<<<<<< HEAD

# imageList = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]
=======
imageList = []


# imageList  = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]
# imageList = []
# app.inputs.bulk_create_images(imageList)
# print(imageList)

>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f

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
<<<<<<< HEAD
    print(f_name)
    with open(f_name) as f:
        print(f)
=======
    # print(f_name)
    with open(f_name) as f:
        # print(f)
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
        try:
            data = json.load(f)
        except ValueError:
            data = []
<<<<<<< HEAD
            print(data)
        imageList = [ClImage(url=pet["picture"]) for pet in data]
        img_search = app.inputs.search_by_image(url=pet_data["picture"])
        print(imageList)
        if len(img_search) > 0:
            return img_search
            # return [img_search.url for images in img_search if images.score >= threshold]
=======
        for pet in data:
            imageList.append(ClImage(url=pet["img_url"]))
        # app.inputs.bulk_create_images(imageList)
        print(pet_data["img_url"])
        img_search = app.inputs.search_by_image(url=pet_data["img_url"])
        print("\n\n")
        if len(img_search) > 0:
            return [{"url": image.url, "score": image.score} for image in img_search if image.score > threshold]
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f
        else:
            return []


<<<<<<< HEAD
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
=======
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
print(getTop_matches(0.8, pet_item))
>>>>>>> 5c0fdc89f3f5fbb956d920c99b923aa1dafba62f


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
