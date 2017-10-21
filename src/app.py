from flask import Flask, request
import api_requests as APIReqs

app = Flask(__name__)


@app.route("/get")
def hello():
    return "Hello World!"


@app.route("/get_dog_by_id/<int:dog_id>")
def get_dog_by_id(dog_id):
    return APIReqs.getDogByID(dog_id)


@app.route("/insert_dog")
def get_dog_by_id():
    return APIReqs.insertDog(request.data["geo_long"], request.data["geo_lat"], request.data["img_url"],
                     request.data["timestamp_img"], request.data.get("nuetered", False))


if __name__ == "__main__":
    app.run()
