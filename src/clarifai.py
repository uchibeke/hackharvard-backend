from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
app = ClarifaiApp()

imageList = []


# imageList  = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]
# imageList = []
# app.inputs.bulk_create_images(imageList)

def getTop_matches(threshold, pet_data):
    if pet_data["state"].lower() == 'colorado':
        pet_data["state"] = "Co"
    f_name = "scraper/LostDogs" + pet_data["state"] + '_output.json'

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

# print(getTop_matches(0.7, pet_item))