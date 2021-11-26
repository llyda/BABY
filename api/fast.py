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
            secret,
            temperature,
            n,
            max_tokens,
            hateSpeechDetector=False):
    # Check if secret is right:
    if secret != SECRET:
        return {'response': ['Error: Wrong secret... :(']}

    # Return error if model is wrong
    if model not in ['ada', 'curie', 'babbage', 'davinci']:
        return {'response': ['Error: Wrong model... :/']}

    # Return error if prompt is too long
    if len(prompt) > 256:
        return {'response': ['Error: Your prompt is too long... :|']}

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

        response = gpt3.predict_haiku(prompt, float(temperature), int(n))
        return {'response': response}
    except Exception as e:
        # Otherwise return error
        return {'response': str(e)}
