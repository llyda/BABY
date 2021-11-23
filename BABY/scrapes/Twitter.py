import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time

BEARER = 'AAAAAAAAAAAAAAAAAAAAAMFEWAEAAAAAGcGC6mOxGiQ7%2FojlR3ZRGlqyQV8%3DXW64RQ9JfVVx0UxNGFmE5wV8tTCw2QkYec61eVREkAd8f59Wvr'
# BEARER = 'AAAAAAAAAAAAAAAAAAAAAMFEWAEAAAAAGcGC6mOxGiQ7%2FojlR3ZRGlqyQV8%3DXW64RQ9JfVVx0UxNGFmE5wV8tTCw2QkYec61eVREkAd8f59Wvr'
API_KEY = '1462775134759051272-urahsmDwZDFJ5PEzaFylJMxwUZGx0s'
API_SECRET = 'knBYiqbVANmaXJxK6rYs4hQ1knPtm5G0CanWuwwupfRAK'
CONSUMER_API_KEY = '3Y419bEhzyrS1Jb0SWSgv6Jiy'
CONSUMER_SECRET = 'o4OFDhh4Z6rWwPMZvo3QDvNoFMSowRSSl7He49D9Bqw4u8Jo1W'

# curl -u '3Y419bEhzyrS1Jb0SWSgv6Jiy:o4OFDhh4Z6rWwPMZvo3QDvNoFMSowRSSl7He49D9Bqw4u8Jo1W' \
#   --data 'grant_type=client_credentials' \
#   'https://api.twitter.com/oauth2/token'

class Twitter():

    def __init__(self):

        return

    # def get_bearer(self):
    #     auth_url = 'https://api.twitter.com/oauth2/token'
    #     params = {}
    #     response = requests.get(url, params=params)

    #     return response.json()

    def create_headers(self):
        print(BEARER)
        headers = {"Authorization": "Bearer {}".format(BEARER)}

        # headers = {
        #         "oauth_consumer_key": CONSUMER_API_KEY,
        #         "oauth_consumer_secret": CONSUMER_SECRET,
        #         "oauth_token": API_KEY,
        #         "oauth_token_secret": API_SECRET
        #         }
        return headers

    def create_url(self, keyword, start_date, end_date, max_results = 10):

        search_url = "https://api.twitter.com/2/tweets/search/recent"

        #change params based on the endpoint you are using
        query_params = {'query': keyword,
                        'start_time': start_date,
                        'end_time': end_date,
                        'max_results': max_results,
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                        'next_token': {}}
        return (search_url, query_params)

    def connect_to_endpoint(self, url, headers, params, next_token = None):
        params['next_token'] = next_token   #params object received from create_url function
        response = requests.get(url, headers=headers, params=params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

if __name__ == '__main__':
    tw = Twitter()
    headers = tw.create_headers()
    url, params = tw.create_url(
        'elonmusk',
        '2021-11-17T11:25:30.926Z',
        '2021-11-23T11:25:30.926Z'
    )
    print(url)
    print(params)

    res = tw.connect_to_endpoint(url, headers, params)

    print(json.dumps(res, indent=2))
