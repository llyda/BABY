import os
from google.resumable_media.requests import upload
import openai
from dotenv import load_dotenv
import pandas as pd
import json
import random
from google.cloud import storage

from BABY.data import save_data

BUCKET_NAME = 'wagon-data-735-babyproject'
BUCKET_PROMPT_HELP = 'train_data/prompt_help.json'
BUCKET_OUTPUT_FILE = 'output_data/output.json'

# from data import get_data_prompt_help
ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))  # This is your Project Root
PATH_TO_CREDENTIALS = os.path.join(ROOT_DIR,
                                   'generated-atlas-328014-38a22af365d4.json')

load_dotenv()
credentials = {
  "type": "service_account",
  "project_id": "generated-atlas-328014",
  "private_key_id": "38a22af365d4908157d367fe752448b1c7463f49",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBEdd6Bz6iXRfx\nGgRgo0xCCe8CirCN1cDL030y+QC5jEM/431DxN+D7ZcmVjWF0exI+T+UMdMgenW7\nLCH8VLxPFNSCvDyQLtXEAnE/0J86ZOWfan3vQEHonZhmXu/7Wz9zPfwlwPVbMDfC\nWG7i2crsMsdfAi1TjN0Ilk5q1szSAmC760xmTe1esEBrkJRSLT663LRa/8CPF5C+\n5RuK1bD/QhxKLpcu+uh9uhF65Ozn+2LqTOWtKOa7HpncNqsrln389WBiVWdpjP5O\nwQouxxrbk11UBs07O1bRYtMBGNXb7KDZrvcuWX6yjcqZjifewJdBMnw838Cg6Xk4\nVzJb/9j9AgMBAAECggEACNnlC4Keg/oJmXOMZNPHsLVc4Dx0eKQmiRGiiT4yIs+D\n2791pDA34Qf46HiGTqK/lt7aY9Re7fu/Pvv4eOV3lpaJYY74pdGH2ksUXw0U56vt\nfP/4Uwoam2vyKytKDDd0MrfSQfbVKL+OptnAB6VdcLOpQTlL06s/DOA7Kxm63RvL\nVCR+ozDFSwwjgrNg0cinaR0XVnmH0ti5PphCU1ovksNV8P3AHOBUGA7ZSWuRFuCh\njndQPuO0RUvW7yL4FH8V1Tp1ZLFX4ZYtrUD2k3jQ0qfqIzD9VrasF2bquw33nnVB\nKhmejoe32vt34OSg2Jr1QpzM7VpTO3xYatOfqaVXMQKBgQDzqcnX36KnAA2PHMhG\nHrkTEVXJ5xBh1n7j7NXBEHWWktPuhdVYMazJaUbG+ry83vFloy6s1zaYynNKTulT\nT2HtSCo90uY4Dz7ukUsdqJVeJpF3IZ7cMIFqY3ioGozgNYhtoIFf74gEfXVWERJ1\neQ0ClxoeysXKskchYX6aDpFX2QKBgQDK2EqLASjpbQqCtskHKxsdPVvDbFIDOIdJ\nD3NDgXJNCj0gJhsJgyAc6rRb0ShFo8Djfq7iCV9Pr9GBfAN+gPqOCcLcFRoECB5+\njj6uwXbFZoNNKKOgHzeeSiCwFEkEDlpZMd5r59e1BlUtDrlSmzosn1qmy2r73ryY\nPW4WxGDXxQKBgQCMtpXI4+5TkPVDm3SRAfcRauZnFdhhF/TpfYEn4HB3x006pvFA\n4FcPbYuhJ3XNgNZZQraWvCZccDXKSO333ZUI6a7zSxMGds96CFAfzZaM66r/6FuM\nfzqNjOpF8ic+58tku9da5sJfDXCwhmVpj8GSqF4+QA2fc/sd7Oam4xjOaQKBgQCp\nc55yGPnwZmMNZ1zwXBY+iu+JhYfNoP+DDSEhF5ZAvXjqzmpvu9ar0XXx7fxSkMWm\nRkIaGfJBQ4MlRFA28dBdr9HUwNwG2jF/T50VqBBsP4MYhgaK0QlJdmtwLMICXWsk\ncAB67CbK1wt4pIA0ffBPLqAwDmbFGgE6vLam1k6AcQKBgCLfeGiJfS2b/h3YVvLZ\n3t5qmFmWK4tlVRUOtpgG4W/kq6ES7/TFBxbKvlu0bJuIxdwvjyZimk4mJyLGMZEG\nhuPmqw6FBMrEvuM2Eav2kCf25YuqJkYhGOAgdqQsPJOJMwSwDzvlY26GvkqYZA2m\n6+2uNxtWpiqSAJemqD6zMSkf\n-----END PRIVATE KEY-----\n",
  "client_email": "baby735@generated-atlas-328014.iam.gserviceaccount.com",
  "client_id": "111571287254775447615",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/baby735%40generated-atlas-328014.iam.gserviceaccount.com"
}

# Load your API key from a .env file
# openai.api_key = os.getenv("OPEN_AI_KEY")

def get_data_prompt_help():
    client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.get_blob(BUCKET_PROMPT_HELP)

    # df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_PROMPT_HELP}")
    # res = json.loads(df.to_json(orient="columns"))

    return json.loads(blob.download_as_string())

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
    return

class OpenAi:

    def __init__(
        self,
        model,
        search_model,
        max_tokens,
        apiKey=None
        ):
        # Model to use for the prediction
        self.model = model
        # Model to use for search
        self.search_model = search_model
        # Define a maximum number of tokens
        self.max_tokens = max_tokens
        self.apiKey = apiKey

        if self.apiKey:
            openai.api_key = self.apiKey
        else:
            openai.api_key = os.getenv("OPEN_AI_KEY")

    def completion(self):
        return

    # Question (required) - is the "prompt"
    # Exemples (required) - a list of key/value pair exemples to inspire the model
    # Exemples_context (required) - the probable output from the prompt
    # Documents (optional) needs to be a jsonl file or a dict/array
    def answers(
        self,
        question,
        temperature=1,
        n=1,
        _type='rap'
        ):

        # Get the examples, context, documents and pick automatically according to _type
        _data = get_data_prompt_help()

        if _type == 'rap':
            _data = _data['rap']
        elif _type == 'haiku':
            _data = _data['haiku']
        elif _type == 'classical':
            _data = _data['classical']
        elif _type == 'bobdylan':
            _data = _data['bobdylan']
        else:
            # Return Error if _type doesn't exist
            return {'response': ['Error: We don\'t have this type yet...']}

        response = openai.Answer.create(
            # search_model=self.search_model,
            model=self.model,
            question=question,
            max_tokens=self.max_tokens,
            examples=_data['examples'],
            examples_context=_data['examples_context'],
            documents=_data['documents'],
            temperature=temperature,
            n=n
        )
        return response

    def completion(
        self,
        prompt,
        temperature=1,
        n=1,
        top_p=1,
        presence_penalty=0,
        frequency_penalty=0,
        stop=None
        ):

        response = openai.Completion.create(
            # search_model=self.search_model,
            model=self.model,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=temperature,
            n=n,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stop=stop
        )

        return response

    def output(self, prompt, res, model_id, model_description):
        upload_data_output(res['model'], model_description, prompt, '',
                           res['choices'][0]['text'], res['created'])
        return


if __name__ == '__main__':
    # Initialise OpenAi with model and search model you desire
    # Be aware of the max number of tokens it returns
    gpt3 = OpenAi(
        model='curie:ft-user-6qfzuqjhvk29sbtb6ezmcw63-2021-11-27-16-36-49',
        search_model='curie',
        max_tokens=150)

    # data = get_data_prompt_help()
    # print(json.dumps(data, indent=2))
    # # print(data)
    # print(
    #     gpt3.answers('Write a rap song vers about drinking and gambling',
    #                 0.9, 2, _type='rap'))

    prompt = 'The following is a haiku about cryptos and nft'
    res = gpt3.completion(prompt)
    print(res)
    # gpt3.output(prompt, res)
