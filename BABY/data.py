import pandas as pd
from google.cloud import storage
import os

AWS_BUCKET_PATH = "s3://wagon-public-datasets/taxi-fare-train.csv"
BUCKET_NAME = 'wagon-data-735-babyproject'
BUCKET_TRAIN_DATA_PATH = 'raw_data/twitter_dump.json'
BUCKET_TRAIN_DATA_CLEAN_PATH = 'raw_data/twitter_dump_clean.json'
#MODEL_NAME = 'taxifare'
#MODEL_VERSION = 'v2'

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    return df

def save_data(df):
    """method to save the training data to the google cloud bucket"""
    df.to_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_CLEAN_PATH}")
    print("Saved Dataframe on Google Cloud Platform")

def clean_data(df, test=False):
    return df

if __name__ == '__main__':
    df = get_data()
