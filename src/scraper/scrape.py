import urllib.request
from bs4 import BeautifulSoup
import requests
import facebook
import re
import json

res = requests.get('https://lostdogsofamerica.org/')
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")

graph = facebook.GraphAPI(
    access_token="EAACEdEose0cBAIRN2RxdR3kCo46bxAglRngv14f3RMdre8IVqWJv00Ib9vrxl03UcrfSZCcZCbXDr5OchX0nHmbfr5osPBGkYBdqLyuZBKR9F8z2nCnODlKB1RvMd5d4UYH9ZB03TV9fBIWgAnZCg0peUUfJEx74vSX8YMGnd5IEdgFOwP12p4MWZA8PaWNXVbN1L7VK6GRQZDZD",
    version=2.10)


def scrape(pg_id):
    item = graph.get_object(id=pg_id, fields='feed')["feed"]["data"]
    return [graph.get_object(i["id"], fields='from, place, link, picture,  created_time, description, application') for
            i in item]


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

imageList = [ClImage(
    url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]

# Search using a URL
search = app.inputs.search_by_image(
    url='http://cdn2-www.dogtime.com/assets/uploads/gallery/german-shepherd-dog-breed-pictures/standing-7.jpg')
print([images.url for images in search if images.score >= 0.59])


# with open('dataset.json', 'r+') as f:
#     data = json.load(f)
#     data['id'] = []  # <--- add `id` value.
#     f.seek(0)  # <--- should reset file position to the beginning.
#     json.dump(data, f, indent=4)
#     f.truncate()  # remove remaining part


def getTop_matches(threshold, image):
    img_search = app.inputs.search_by_image(url=image)
    return [images.url for images in img_search if images.score >= threshold]


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
