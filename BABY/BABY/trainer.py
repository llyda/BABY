from pathlib import Path
import json
from cleaner import cleaner


def get_data():
    '''needs connection to GCP to load files from cloud'''
    # reads data from data directory into a long list
    your_path = 'twitter_dump.json'
    tweet_list = []

    # for file in Path(your_path).rglob('*.json'):
    with open(your_path) as f:
        json_file = json.load(f)

    for dictionary in json_file:
        tweet_list.append(dictionary["text"])      # this just works assuming the key is called text
    return tweet_list


tweet_list = get_data()
tweet_string = cleaner(tweet_list)

with open("baby_food.txt", "w") as food:
    food.write(tweet_string)


# cleansed tweets must go to GTP3 maybe in another form?
