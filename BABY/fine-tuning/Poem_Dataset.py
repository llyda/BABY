import json
import argparse
import os
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())


def create_sentences(sentences,key,dict):
    data = dict[key]
    counter = 0
    for item in data:
        #cleans data
        if item.find("[10w]")==-1:
            #skips non ascii
            if not isascii(item):
                continue
            #saves the poems with style of: <|endoftext|>love: poetry about love here<|endoftext|>
            sentences.append("<|endoftext|>\n" + key + ": " + item +
                             "\n<|endoftext|>")
    return sentences

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Tool to train a custom GPT3 BABY model")

    #"--file" can be used to change file format
    parser.add_argument(
        "-f", "--file", type=str,
        default="./all.json")
    args = parser.parse_args()
    json_file = args.file
    json_file = os.path.realpath(json_file)
    #loads the file
    with open(json_file) as f:
        data = json.load(f)
    #creates dictonary that will hold the type of poem
    type_dict = {}
    #loops through all poems and adds them to the appropriate type
    for index, item in enumerate(data):
        if item["type"] in type_dict:
            type_dict[item["type"]].append(item["content"])
        else:
            entry = [item["content"]]
            type_dict[item["type"]] = entry
    #remove empty entry
    type_dict.pop("",None)
    #prints out the different types of poetry
    print(type_dict.keys())

    sentences = []
    for key in type_dict.keys():
        #creates the data entries for training the model
        sentences = create_sentences(sentences,key,type_dict)
    #splits into train and test data for training
    train_sentences,test_sentences = train_test_split(sentences,test_size=0.2)
    #creates dataframes that will be saved with text column as a csv file
    train_df = pd.DataFrame(train_sentences,columns=['text'])
    validate_df = pd.DataFrame(test_sentences,columns=['text'])
    #drops NA items if there is any
    train_df = train_df.dropna()
    validate_df = validate_df.dropna()
    train_df.to_csv("train-poet.csv")
    validate_df.to_csv("validation-poet.csv")

