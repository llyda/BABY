from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from BABY.OpenAi import OpenAi
from BABY.data import get_json_output
# from BABY.HateSpeech import HateSpeechDetector
import os
from dotenv import load_dotenv
import json

# API

load_dotenv()

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))  # This is your Project Root
PATH_TO_MODELS = os.path.join(ROOT_DIR,
                                   'models.json')

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

@app.get("/output")
def output():
    # Get All Outputs Generated in The Past <3
    return get_json_output()


@app.get("/predict")
def predict(model,
            prompt,
            personality_type,
            secret,
            _type):

    # Check if secret is right:
    if secret != SECRET:
        return {'response': 'Error: Wrong secret... :('}

    # Return error if model is wrong
    print(model)
    if model not in [
            'Ada', 'Curie', 'Babbage', 'Davinci',
            'Curie Rap',
            'Curie Haiku',
            'Curie Poems'
    ]:
        return {'response': 'Error: Wrong model... :/'}

    # Return error if prompt is too long
    if len(prompt) > 64:
        return {'response': 'Error: Your prompt is too long... :|'}

    # Limit the number of potential answers
    # if int(n) > 4:
    #     return {'response': ['Error: You can\'t request that many answers. Try 2!']}
    hate_list = ["allah akbar", "blacks", "chink", "chinks", "dykes", "faggot", "faggots", "fags", "homo", "inbred", "nigger", "niggers", "queers", "raped", "savages", "slave", "spic", "wetback", "wetbacks", "whites", "a dirty", "a nigger", "all niggers", "all white", "always fuck", "ass white", "be killed", "beat him", "biggest faggot", "blame the", "butt ugly", "chink eyed", "chinks in", "coon shit", "dumb monkey", "dumb nigger", "fag and", "fag but", "faggot a", "faggot and", "faggot ass", "faggot bitch", "faggot for", "faggot smh", "faggot that", "faggots and", "faggots like", "faggots usually", "faggots who", "fags are", "fuckin faggot", "fucking faggot", "fucking gay", "fucking hate", "fucking nigger", "fucking queer", "gay ass", "get raped", "hate all", "hate faggots", "hate fat", "hate you", "here faggot", "is white", "jungle bunny", "kill all", "kill yourself", "little faggot", "many niggers", "married to", "me faggot", "my coon", "nigga ask", "niggas like", "nigger ass", "nigger is", "nigger music", "niggers are", "of fags", "of white", "raped and", "raped by", "sand nigger", "savages that", "shorty bitch", "spear chucker", "spic cop", "stupid nigger", "that fag", "that faggot", "that nigger", "the faggots", "the female", "the niggers", "their heads", "them white", "then faggot", "this nigger", "to rape", "trailer park", "trash with", "u fuckin", "ugly dyke", "up nigger", "white ass", "white boy", "white person", "white trash", "with niggas", "you fag", "you nigger", "you niggers", "your faggot", "your nigger", "a bitch made", "a fag and", "a fag but", "a faggot and", "a faggot for", "a fucking queer", "a nigga ask", "a white person", "a white trash", "all these fucking", "are all white", "be killed for", "bitch made nigga", "faggots like you", "faggots usually have", "fuck outta here", "fuck u talking", "fuck you too", "fucking hate you", "full of white", "him a nigga", "his shorty bitch", "how many niggers", "is a fag", "is a faggot", "is a fuckin", "is a fucking", "is a nigger", "like a faggot", "like da colored", "many niggers are", "nigga and his", "niggers are in", "of white trash", "shut up nigger", "still a faggot", "the biggest faggot", "the faggots who", "the fuck do", "they all look", "what a fag", "white bitch in", "white trash and", "you a fag", "you a lame", "you a nigger", "you fuck wit", "you fucking faggot", "your a cunt", "your a dirty", "your bitch in", "a bitch made nigga", "a lame nigga you", "faggot if you ever", "full of white trash", "how many niggers are", "is full of white", "lame nigga you a", "many niggers are in", "nigga you a lame", "niggers are in my", "wit a lame nigga", "you a lame bitch", "you fuck wit a"]

    # Split prompt into words:
    # if ',' in prompt:
    topics = prompt.split(',')
    print(topics)

    # Hate Speech Detector
    for topic in topics:
        if topic in hate_list:
            return {'response':
                'Error: We don\'t accept hate speech or any (potentially) offensive topics. Please be respectful if you want to use BABY.'}

    # Reunite Topics
    if len(topics) > 2:
        _topics = ' and '.join(topics[3:])
    elif len(topics) == 2:
        _topics = ' and '.join(topics)
    else:
        _topics = topics[0]

    with open(PATH_TO_MODELS) as f:
        customModels = json.load(f)

    try:
        # Get the params from our API wrapper
        _temperature = 1
        _presence_penalty=0
        _frequency_penalty=0
        _stop=None
        _api_key=None
        _custom_prompt=None

        # Try to return answer

        for customModel in customModels:
            if customModel['model'] == model:
                model = customModel['id']
                _temperature = customModel['temperature']
                _presence_penalty = customModel['presence_penalty']
                _frequency_penalty = customModel['frequency_penalty']
                _stop = customModel['stop']
                _api_key = customModel['apiKey']
                _custom_prompt = customModel['prompt']
                _description = customModel['description']


        print(_temperature)
        print(_api_key)

        gpt3 = OpenAi(
            model=model,
            search_model='curie',
            max_tokens=75,
            apiKey=_api_key
        )

        # Building the Basic Prompt HERE
        if personality_type == 'myself':
            _prompt = f"The following is a {_type} about {_topics}"
        else:
            _prompt = f"The following is a {_type} about {_topics} by {personality_type}"

        if _custom_prompt:
            # Make the custom prompt
            prompt_p1 = _custom_prompt.split('TOPICS')[0]
            prompt_p2 = _custom_prompt.split('TOPICS')[1].split('PERSON')[0]
            prompt_p3 = _custom_prompt.split('PERSON')[1]

            _prompt = prompt_p1 + _topics + prompt_p2 + personality_type + prompt_p3

        print(_prompt)

        response = gpt3.completion(_prompt,
                                   temperature=_temperature,
                                   n=1,
                                   top_p=1,
                                   presence_penalty=_presence_penalty,
                                   frequency_penalty=_frequency_penalty,
                                   stop=_stop)

        print(response)

        # Output in JSON File!
        gpt3.output(_prompt, response, model, _description)

        return {'response': response['choices'][0]['text'], 'prompt': _prompt}
    except Exception as e:
        # Otherwise return error
        return {'response': str(e)}
