import pymysql.cursors
import json

db = pymysql.connect(host='40.71.253.77', passwd='RuffinitHarvard2017', user='root', db='Ruffinit',
                     cursorclass=pymysql.cursors.DictCursor)


def getDogByID(dog_id):
    c = db.cursor()
    c.execute("SELECT * FROM dogs WHERE dog_id=%s", (dog_id,))
    return json.dumps(c.fetchone())


def insertDog(geo_long, geo_lat, img_url, timestamp_img, state="none", nuetered=False, fb_post_id="none", phoneNumber="none", injured=False, type="MISSING"):
    c = db.cursor()
    c.execute("INSERT INTO dogs (geo_long, geo_lat, img_url, timestamp_img, nuetered, fb_post_id, phone_number, state, injured, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
              ,(geo_long, geo_lat, img_url, timestamp_img, nuetered, fb_post_id, phoneNumber, state, injured, type))
    db.commit()


def getDogByGeoTag(geo_lat, geo_lang, lat_length, long_length):
    c = db.cursor()
    c.execute("SELECT ")


print(getDogByID(1))

