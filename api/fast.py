from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BABY.OpenAi import OpenAi
import os
from dotenv import load_dotenv

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
def predict(model, prompt, secret):
    # Check if secret is right:
    if secret != SECRET:
        return {'error': 'Wrong secret... :('}

    # Return error if model is wrong
    if model not in ['ada', 'curie', 'babbage', 'davinci']:
        return {'error': 'Wrong model... :/'}

    # Return error if prompt is too long
    if len(prompt) > 256:
        return {'error': 'Your prompt is too long... :|'}

    try:
        # Try to return answer
        gpt3 = OpenAi(
            model=model,
            search_model='ada',
            max_tokens=25
        )

        response = gpt3.predict(prompt)
        return {'response': response[0]}
    except Exception as e:
        # Otherwise return error
        return {'error': str(e)}
