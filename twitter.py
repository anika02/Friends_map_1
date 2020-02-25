
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request

app = Flask(__name__)

import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def hello_friends(js):
    return [(i["screen_name"], i["location"]) for i in js["users"]]


def twitter2(nick):
    acct = nick
    if (len(acct) > 0):
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '5'})
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        js = json.loads(data)
        return js


def map_generate(friends):
    map_1 = folium.Map(zoom_start=1000)
    geolocator = Nominatim(
        user_agent="specify_your_app_name_here", timeout=3)
    result_lst = []
    for i in friends:
        try:
            result_lst.append([i[0], geolocator.geocode(i[1]).latitude, geolocator.geocode(
                i[1]).longitude])
        except:
            pass

    # result_lst = result_lst[:20]

    fg = folium.FeatureGroup(name="friends")
    for name, lt, ln in result_lst:
        fg.add_child(folium.Marker(
            location=[lt, ln], popup=name, icon=folium.Icon()))
    map_1.add_child(fg)

    map_1.add_child(folium.LayerControl())
    friends_map = map_1.get_root().render()
    return friends_map
    # print("Map is generating...")
    # print("Please wait...")
    # print("Finished. Please have look at the map Map_friends.html")
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    nick = request.form['user_name']
    json_friends = twitter2(nick)
    friends = hello_friends(json_friends)
    friends_map = map_generate(friends)
    contex = {'friends_map': friends_map}
    return render_template("Map_friends.html", **contex)


if __name__ == "__main__":
    app.run()



