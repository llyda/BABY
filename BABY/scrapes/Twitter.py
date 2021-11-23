from typing import final
import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time
from dotenv import load_dotenv

load_dotenv()
BEARER = os.getenv('BEARER_TOKEN')

BASE_URI = 'https://api.twitter.com'

class Twitter():

    def __init__(self):
        self.data = []
        return

    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(BEARER)}
        return headers

    def tweets_from_user(self, user_id, max_results = 10):
        endpoint = f'/2/users/{user_id}/tweets'
        url = BASE_URI + endpoint

        query_params = {
                'max_results': max_results,
                # 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                # 'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                'pagination_token': {}
        }
        return (url, query_params)

    def tweets_search_recent(self, keyword, start_date, end_date, max_results = 10):
        endpoint = '/2/tweets/search/recent'
        url = BASE_URI + endpoint

        query_params = {'query': keyword,
                        'start_time': start_date,
                        'end_time': end_date,
                        'max_results': max_results,
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                        'next_token': {}
        }
        return (url, query_params)

    def connect_to_endpoint(self, url, headers, params, next_token = None):
        params['pagination_token'] = next_token
        response = requests.get(url, headers=headers, params=params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json(), response.json()['meta']['next_token']

    def ref(self, _data):
        data = []
        for tweet in _data['data']:
            data.append({'id': tweet['id'], 'text': tweet['text']})
        return data

def dump(_data):
    # Load existing data
    with open('twitter_dump.json') as f:
        data = json.load(f)
    # Combine
    data += _data
    # Dump
    with open('twitter_dump.json', 'w') as f:
        json.dump(data, f)

def get_accounts():
    with open('twitter_accounts.json') as f:
        accounts = json.load(f)
    return accounts["twitter"]["profiles"]

if __name__ == '__main__':
    # Init Twitter Lib
    tw = Twitter()
    headers = tw.create_headers()

    # Get accounts
    accounts = get_accounts()
    # print(accounts)

    for account in accounts:
        # Get tweets from User
        url, params = tw.tweets_from_user(
            account['id']
        )

        # Pagination
        next_token = None

        for i in range(0, 3):
            name = account['url']
            print(f'Scraping {name}, page {str(i)}')
            try:
                res, next_token = tw.connect_to_endpoint(url, headers, params, next_token=next_token)
            except Exception as e:
                print(f'Error: {e}')
            finally:
                data = tw.ref(res)
                # Dump data every run
                dump(data)
                # print(json.dumps(data, indent=2))
