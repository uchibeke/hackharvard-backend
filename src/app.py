from flask import Flask, request
from api_requests import *

app = Flask(__name__)


@app.route("/get")
def hello():
    return "Hello World!"


@app.route("/get_dog_by_id/<int:dog_id>")
def get_dog_by_id(dog_id):
    return getDogByID(dog_id)


@app.route("/insert_dog")
def get_dog_by_id():
    return insertDog(request.data["geo_long"], request.data["geo_lat"], request.data["img_url"],
                     request.data["timestamp_img"], request.data.get("nuetered", False))


if __name__ == "__main__":
    app.run()
