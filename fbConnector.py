#!/usr/bin/env python

import facebook
import requests
import json
import urllib
import shutil


access_token = "EAACEdEose0cBAL6XnKL9a2SgCZCqjPOZArs8iasxQ4k7GH9Fgl62fhXO3IPAalfYFZBHvzZCAwmKrinWuG24xcAJYz7uEZCHUd1XYxhkNcBfkbcuZBVM32hhsKX4wIQkMjIcj6QoF1qSvPopXgrvs0qaHb2r7k3hx54x57fgJGZBEUNCFytu5ZBb980b6AAoH7xZBst5Q7ORSsgZDZD" #generated from https://developers.facebook.com/tools/accesstoken/
app_id = "185653772156665" #hide this
client_secret = "0d3cf59054363a120248d794a3f63627" #hide this

def extendToken(access_token,app_id,client_secret):
    link = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=" + app_id +"&client_secret=" + client_secret + "&fb_exchange_token=" + access_token
    s = requests.Session()
    token = s.get(link).content
    token=json.loads(token)
    token=token.get('access_token')
    print "Extended access token..."
    return token

def getId(access_token):
    r = requests.get("https://graph.facebook.com/me?fields=id&access_token="+access_token)
    print "Getting user ID: {}".format(r.json()['id'])
    return r.json()['id']

def saveImage(friend):
    size = '/picture?width=200&height=200'
    url = 'https://graph.facebook.com/'+ friend['id'] + "/photos"
    response = requests.get(url,stream=True)
    print response.raw
    # with open('images/'+ friend['name'] + '.jpg', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)
    # del response

def getFriendIds(access_token,userId):
    g = facebook.GraphAPI(access_token=access_token,version=2.2)
    #friends = g.get_connections("me","friends")
    r = g.request(userId+"/friends")
    for friend in r['data']:
        print friend
        saveImage(friend)

extendToken(access_token,app_id,client_secret)
userId = getId(access_token)

getFriendIds(access_token,userId)
