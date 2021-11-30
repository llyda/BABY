from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BABY.OpenAi import OpenAi
# from BABY.HateSpeech import HateSpeechDetector
import os
from dotenv import load_dotenv

# API

load_dotenv()

SECRET = os.getenv("SECRET")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "This is BABY!"}

@app.get("/predict")
def predict(model,
            prompt,
            personality_type,
            secret,
            temperature,
            n,
            max_tokens,
            _type,
            hateSpeechDetector=False):
    # _type:
    # - rap, bobdylan, haiku, classical (string)

    # prompt:
    # - Write a rap song verse about living in San Francisco (string)

    # secret:
    # - Password to access the API (string)

    # Temperature
    # - 0 to 1 (float)

    # n
    # - Number of answers to return (max=4)

    # Check if secret is right:
    if secret != SECRET:
        return {'response': ['Error: Wrong secret... :(']}

    # Return error if model is wrong
    if model not in ['ada', 'curie', 'babbage', 'davinci']:
        return {'response': ['Error: Wrong model... :/']}

    # Return error if prompt is too long
    if len(prompt) > 64:
        return {'response': ['Error: Your prompt is too long... :|']}

    # Limit the number of potential answers
    if int(n) > 4:
        return {'response': ['Error: You can\'t request that many answers. Try 2!']}


    # If HateSpeechDetectorActivated:
    if hateSpeechDetector:
        # hsc = HateSpeechDetector()
        # isHateSpeech = hsc.detect(prompt)
        # if isHateSpeech in ['Hate Speech', 'Offensive Language']:
        #     return {'response': 'Error: We don\'t allow offensive language nor hate speech'}
        pass

    try:
        # Try to return answer
        gpt3 = OpenAi(
            model=model,
            search_model='curie',
            max_tokens=int(max_tokens)
        )

        # Get the params from our API wrapper
        # response = gpt3.answers(
        #     prompt,
        #     float(temperature),
        #     int(n),
        #     str(_type)
        # )

        # Building Prompt HERE
        _prompt = f"This is a {_type}, written by the fake personality of {personality_type} about {prompt}"

        response = gpt3.completion(_prompt,
                                   float(temperature),
                                   n=1,
                                   top_p=1,
                                   presence_penalty=0,
                                   frequency_penalty=0)

        return {'response': response['choices']}
    except Exception as e:
        # Otherwise return error
        return {'response': str(e)}
