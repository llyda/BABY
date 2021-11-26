from dotenv import load_dotenv
import os
from random import choice
import openai
from flask import Flask, request


OPENAI_KEY = "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"

# openai.api_key = os.getenv(OPENAI_KEY)
# openai.Engine.list()

# curl -u :OPENAI_KEY https://api.openai.com/v1/engines/ada

load_dotenv()
openai.api_key = os.environ.get(OPENAI_KEY)
completion = openai.Completion()

session_prompt = "Write a crazy poem like Charles Bukowski, reimagine and reinterprete what you know"



def write_poem(session_story=None):
    file1 = open("poems.txt","a")
    if session_story == None:
        prompt_text = session_prompt
        file1.write(session_prompt)
    else:
        prompt_text = session_story
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt_text,
      temperature=0.7,
      max_tokens=50,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.3,)

    story = response['choices'][0]['text']
    append_to_story(story, session_story)

    file1.write(story)
    return str(story)



#
response = openai.Completion.create(
  engine="davinci",
  prompt="Marv is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\nYou: Why is the sky blue?\nMarv:",
  temperature=0.3,
  max_tokens=60,
  top_p=0.3,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  stop=["\n\n"]
