import os
import openai
from dotenv import load_dotenv
import pandas as pd
import json
import random
from google.cloud import storage

BUCKET_NAME = 'wagon-data-735-babyproject'
BUCKET_PROMPT_HELP = 'train_data/prompt_help.json'
# from data import get_data_prompt_help

load_dotenv()

# Load your API key from a .env file
openai.api_key = os.getenv("OPEN_AI_KEY")

def get_data_prompt_help():
    df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_PROMPT_HELP}")
    res = json.loads(df.to_json(orient="columns"))
    return res

class OpenAi:

    def __init__(
        self,
        model,
        search_model,
        max_tokens
        ):
        # Model to use for the prediction
        self.model = model
        # Model to use for search
        self.search_model = search_model
        # Define a maximum number of tokens
        self.max_tokens = max_tokens

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

if __name__ == '__main__':
    # Initialise OpenAi with model and search model you desire
    # Be aware of the max number of tokens it returns
    gpt3 = OpenAi(
        model='davinci',
        search_model='curie',
        max_tokens=60
    )

    data = get_data_prompt_help()['rap']
    # print(data)
    print(
        gpt3.answers('Write a rap song vers about drinking and gambling', data['examples'], data['examples_context'], data['documents'],
                    0.9, 2, _type='rap'))
