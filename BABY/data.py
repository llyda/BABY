import pandas as pd
from google.cloud import storage
import os
import json

BUCKET_NAME = 'wagon-data-735-babyproject'
BUCKET_TRAIN_DATA_PATH = 'raw_data/twitter_dump.json'
BUCKET_TRAIN_DATA_CLEAN_PATH = 'raw_data/twitter_dump_clean.json'
BUCKET_PROMPT_HELP = 'train_data/prompt_help.json'
BUCKET_OUTPUT_FILE = 'output_data/output.json'
#MODEL_NAME = 'baby'
#MODEL_VERSION = 'v0.1'
ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))  # This is your Project Root
PATH_TO_CREDENTIALS = os.path.join(ROOT_DIR, 'generated-atlas-328014-38a22af365d4.json')

# Get Twitter Dump Data (scraped)
def get_data():
    """method to get the twitter dump data from google cloud bucket"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    return df

# Get Output data from GPT3 runs into a DF
def get_output():
    """method to get the twitter dump data from google cloud bucket"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    return df

# Get prompt help data (examples/context/documents)
# def get_data_prompt_help():
#     df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_PROMPT_HELP}")
#     res = json.loads(df.to_json(orient="columns"))
#     return res

# Save the cleaned data
def save_data(df):
    """method to save the twitter dump data to the google cloud bucket"""
    df.to_json(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_CLEAN_PATH}")
    print("Saved Dataframe on Google Cloud Platform")

def clean_data(df, test=False):
    return df

# Save the output data
def save_output(model_id, model_description, user_prompt, user_documents, answer, timestamp):
    """method to save the queries and answers of the model in one json-file, one row appended for every query"""
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    dict = {"model_id": model_id, "model_description": model_description, "user_prompt": user_prompt, "user_documents": user_documents, "answer": answer, "timestamp": timestamp}
    df = df.append(dict, ignore_index = True)
    df.to_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")
    print("Updated output.json and saved to google cloud bucket")


def get_data_prompt_help():
    client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(BUCKET_PROMPT_HELP)

    return json.loads(blob.download_as_string())

def get_data_output():
    client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(BUCKET_OUTPUT_FILE)

    print(blob.download_as_string())

    df = pd.read_json(blob.download_as_string())
    return df


def upload_data_output(model_id, model_description, user_prompt,
                       user_documents, answer, timestamp):
    client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(BUCKET_OUTPUT_FILE)

    df = pd.read_json(blob.download_as_string())
    dict = {"model_id": model_id, "model_description": model_description, "user_prompt": user_prompt, "user_documents": user_documents, "answer": answer, "timestamp": timestamp}
    df = df.append(dict, ignore_index = True)
    # df = pd.DataFrame.from_dict(dict)

    blob.upload_from_string(data=df.to_json(),
                            content_type='application/json')
    return df


if __name__ == '__main__':
    #df = get_data()
    # save_output('adatest', 'ada is good', 'write me a bukowski', 'xyz',
    #             'go fck yrself', '2021-02')
    # df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_OUTPUT_FILE}")

    # print(df)


    # print(
    #     upload_data_output('ada', 'ada is good', 'this is brombt', 'xyz', 'blabla',
    #                        '1970-01-01 00:00:00.000000001'))

    print(get_data_output())
