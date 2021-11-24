import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Load your API key from a .env file
openai.api_key = os.getenv("OPEN_AI_KEY")

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

    def upload(self):
        return

    def completion(self):
        return

    # Question (required) - is the "prompt"
    # Exemples (required) - a list of key/value pair exemples to inspire the model
    # Exemples_context (required) - the probable output from the prompt
    # Documents (optional) needs to be a jsonl file or a dict/array
    def answers(self, question, examples, examples_context, documents):
        response = openai.Answer.create(
            # search_model=self.search_model,
            model=self.model,
            question=question,
            max_tokens=self.max_tokens,
            examples=examples,
            examples_context=examples_context,
            documents=documents
        )
        return response

if __name__ == '__main__':
    # Initialise OpenAi with model and search model you desire
    # Be aware of the max number of tokens it returns
    gpt3 = OpenAi(
        model='ada',
        search_model='ada',
        max_tokens=25
    )

    # Exemples for jokes
    examples = [
        ['Did you hear about the first restaurant to open on the moon?', 'It had great food, but no atmosphere.'],
        ['What did one ocean say to the other ocean?','Nothing, it just waved.'],
        ['Do you want to hear a construction joke?','Sorry, I’m still working on it.']
    ]
    examples_context = 'It had great food, but no atmosphere.'

    documents = [
        "Why did the bullet end up losing his job? He got fired.",
        "What kind of shorts do clouds wear? Thunderpants",
        "I entered ten puns in a contest to see which would win. No pun in ten did.",
        "How do you measure a snake? In inches—they don’t have feet.",
        "Where does a waitress with only one leg work? IHOP.",
        "What does a house wear? Address!",
        "Why are toilets always so good at poker? They always get a flush",
        "Why is Peter Pan always flying? Because he Neverlands. (I love this joke because it never grows old.)",
        "You heard the rumor going around about butter? Never mind, I shouldn’t spread it."
    ]

    # Call the Answers API endpoint with your parameters
    res = gpt3.answers(
        question='What do you call a lesbian dinosaur?',
        examples=examples,
        examples_context=examples_context,
        documents=documents
    )

    print(res['answers'])
    # Test with jokes:


    # Answers params exemples
    #     {
    #   "documents": ["Puppy A is happy.", "Puppy B is sad."],
    #   "question": "which puppy is happy?",
    #   "search_model": "ada",
    #   "model": "curie",
    #   "examples_context": "In 2017, U.S. life expectancy was 78.6 years.",
    #   "examples": [["What is human life expectancy in the United States?","78 years."]],
    #   "max_tokens": 5,
    #   "stop": ["\n", "<|endoftext|>"]
    # }

    # Exemple of response
    #  {
    #   "answers": [
    #     "puppy A."
    #   ],
    #   "completion": "cmpl-2euVa1kmKUuLpSX600M41125Mo9NI",
    #   "model": "curie:2020-05-03",
    #   "object": "answer",
    #   "search_model": "ada",
    #   "selected_documents": [
    #     {
    #       "document": 0,
    #       "text": "Puppy A is happy. "
    #     },
    #     {
    #       "document": 1,
    #       "text": "Puppy B is sad. "
    #     }
    #   ]
    # }
