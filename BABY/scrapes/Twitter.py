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

    def tweets_from_user(self, user_id, max_results = 100):
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

    def tweets_search_recent(self, keyword, start_date, end_date, max_results = 100):
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

    def ref(self, _data, author_name, segment):
        data = []
        for tweet in _data['data']:
            data.append({
                'id': tweet['id'],
                'author_id': tweet['author_id'],
                'created_at': tweet['created_at'],
                'lang': tweet['lang'],
                'text': tweet['text'],
                'author_name': author_name,
                'segment': segment}
            )
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
    segments = get_accounts()
    # print(accounts)
    total_scrape = 0

    for segment in segments:
        time.sleep(5)
        print(f'Slept 5 seconds...')
        _segment = segment['segment']

        for account in segment["data"]:
            # print(account)
            _author_name = account["url"]
            # Get tweets from User
            url, params = tw.tweets_from_user(
                account['id']
            )

            # Pagination
            next_token = None

            for i in range(0, 20):
                name = account['url']
                print(f'Total Tweet Scraped: {str(total_scrape)}')
                print(f'Scraping {name}, page {str(i)}')
                try:
                    res, next_token = tw.connect_to_endpoint(url, headers, params, next_token=next_token)
                except Exception as e:
                    print(f'Error: {e}')
                finally:
                    try:
                        data = tw.ref(res, _author_name, _segment)
                        # Dump data every run
                        print(f'Tweet found: {str(len(data))}')
                        total_scrape += len(data)
                        dump(data)
                        # print(json.dumps(data, indent=2))
                    except Exception as e:
                        print(f'Error: {e}')
                    finally:
                        pass

# 38 accounts
# 100 Tweets/req
# next_token = 10?
