from pathlib import Path
import json
from cleaner import cleaner


def get_data():
    # reads data from data directory into a long list
    your_path = '../data'
    tweet_list = []

    for file in Path(your_path).rglob('*.json'):
        f = open(file)
        json_file = json.load(f)
        for dictionary in json_file:
            tweet_list.append(dictionary["text"])
    return tweet_list


tweet_list = get_data()
tweet_json = cleaner(tweet_list)
