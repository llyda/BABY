import pandas as pd
from google.cloud import storage
import os

BUCKET_NAME = 'wagon-data-735-babyproject'
BUCKET_TRAIN_DATA_PATH = 'raw_data/twitter_dump.json'
BUCKET_TRAIN_DATA_CLEAN_PATH = 'raw_data/twitter_dump_clean.json'
BUCKET_OUTPUT_FILE = 'output_data/output.json'
#MODEL_NAME = 'baby'
#MODEL_VERSION = 'v0.1'

def get_data():
    """method to get the twitter dump data from google cloud bucket"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    return df

def save_data(df):
    """method to save the twitter dump data to the google cloud bucket"""
    df.to_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_CLEAN_PATH}")
    print("Saved Dataframe on Google Cloud Platform")

def clean_data(df, test=False):
    return df

def save_output(model_id, model_description, user_prompt, user_documents, answer, timestamp):
    """method to save the queries and answers of the model in one json-file, one row appended for every query"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    dict = {"model_id": model_id, "model_description": model_description, "user_prompt": user_prompt, "user_documents": user_documents, "answer": answer, "timestamp": timestamp}
    df = df.append(dict, ignore_index = True)
    df.to_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    print("Updated output.json and saved to google cloud bucket")


if __name__ == '__main__':
    #df = get_data()
    save_output('adatest', 'ada is good', 'write me a bukowski', 'xyz',
                'go fck yrself', '2021-02')
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    print(df)
