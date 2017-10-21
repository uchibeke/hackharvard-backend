import pymysql.cursors
import json
db = pymysql.connect(host='40.71.253.77', passwd='RuffinitHarvard2017', user='root', db='Ruffinit', cursorclass=pymysql.cursors.DictCursor)


def getDogByID(dog_id):
    c = db.cursor()
    c.execute("SELECT * FROM dogs WHERE dog_id=%s", (dog_id,))
    return json.dumps(c.fetchone())


def insertDog(geo_long, geo_lat, img_url, timestamp_img, nuetered=False):
    c = db.cursor()
    c.execute("INSERT INTO dogs (geo_long, geo_lat, img_url, timestamp_img, nuetered) VALUES (%s, %s, %s, %s, %s);"
              ,(geo_long, geo_lat, img_url, timestamp_img, nuetered))
    db.commit()


def getDogByGeoTag(geo_long, geo_lang, radius):
    c = db.cursor()
    c.execute("SELECT ")


print(getDogByID(1))