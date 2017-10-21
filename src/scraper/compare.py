import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='af6f6b9ff13a46fb92a7db31486aeb09')

imageList = [ClImage(url="http://cdn2-www.dogtime.com/assets/uploads/gallery/golden-retriever-dogs-and-puppies/golden-retriever-dogs-puppies-6.jpg")]

# Search using a URL
search = app.inputs.search_by_image(
    url='http://cdn2-www.dogtime.com/assets/uploads/gallery/german-shepherd-dog-breed-pictures/standing-7.jpg')

for search_result in search:
    print("Score:", search_result.score, "| URL:", search_result.url)

from multiprocessing import Process

def loop_a():
    count = 100;
    while count:
        print("a")


def loop_b():
    count = 100;
    while count:
        print("b")
        count = count - 1

if __name__ == '__main__':
    Process(target=loop_a).start()
    Process(target=loop_b).start()