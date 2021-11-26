import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

# Load your API key from a .env file

openai.api_key = os.getenv("OPEN_AI_KEY")

#this will train it on the .jsonl file that was prepared
openai.FineTune.create(
  training_file="TRAIN_FILE_ID_OR_PATH",
  model="BASE_MODEL"
  )
