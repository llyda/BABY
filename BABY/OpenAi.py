import os
import openai
from dotenv import load_dotenv
import pandas as pd
import json
import random

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
    def answers(self,
                question,
                examples,
                examples_context,
                documents,
                temperature
                ):
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

    # Generate Random Exemples/Documents from the dataset provided
    # Poorly reformated yet
    def get_random_documents(self):
        df = pd.read_csv('data/poems.csv')[['author', 'content']]
        df['author'] = df['author'].str.lower()
        df['content'] = df['content'].str.replace('\r\n', ' ')

        # Generate random documents
        _amount = 100

        # Generate random examples
        examples = []
        sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
        for sample in sample_df.iterrows():
            # print(sample[1][1])
            if len(sample[1][1]) < 2048:
                examples.append(
                    [f'Write a poem like {sample[1][0]}', sample[1][1]])


        documents = []
        sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
        for sample in sample_df.iterrows():
            if len(sample[1][1]) < 2048:
                documents.append(sample[1][1])

        return examples[:5], documents[:5]

    def predict_haiku(self, question, temperature=1):
        examples_context = "you’re a beast, she said, your big white belly, and those hairy feet., you never cut your nails, and you have fat hands, paws like a cat, your bright red nose, and the biggest balls, I’ve ever seen, you shoot sperm like a, whale shoots water out of the, hole in its back, beast beast beast, she kissed me, what do you want for, breakfast?"
        examples, documents = self.get_random_documents()

        res = self.answers(question=question,
                           examples=examples,
                           examples_context=examples_context,
                           documents=documents,
                           temperature=temperature)

        return res['answers']

    def predict_haiku_test(self, question, examples, examples_context, documents):
        res = self.answers(question=question,
                           examples=examples,
                           examples_context=examples_context,
                           documents=documents)
        return res

if __name__ == '__main__':
    # Initialise OpenAi with model and search model you desire
    # Be aware of the max number of tokens it returns
    gpt3 = OpenAi(
        model='davinci',
        search_model='curie',
        max_tokens=70
    )

    # print(gpt3.predict_haiku('Write a poem for my mom', temperature=0.9))

    exemples, documents = gpt3.get_random_documents()

    print(json.dumps(exemples, indent=2))
    print(json.dumps(documents, indent=2))












    # # Exemples for jokes
    # prompt_start = 'Write a poem like'
    # examples = [
    #     [
    #         f'{prompt_start} Muddy Waters',
    #         'I hear a lotta buzzing, sound like my little honey bee, I hear a lotta buzzing, sound like my little honey bee,   She been all around the world making honey, But now she is coming back home to me.'
    #     ],
    #     [
    #         f'{prompt_start} Roberto Bolano',
    #         'I dreamt of a difficult case, I saw corridors filled with cops, I saw interrogations left unresolved, The ignominious archives, And then I saw the detective, Return to the scene of the crime, Tranquil and alone.'
    #     ],
    #     [
    #         f'{prompt_start} Robert Frost',
    #         'Whose woods these are I think I know, His house is in the village though, He will not see me stopping here, To watch his woods fill up with snow.'
    #     ]
    # ]
    # examples_context = 'Whose woods these are I think I know, His house is in the village though, He will not see me stopping here, To watch his woods fill up with snow.'

    # documents = [
    #     "you’re a beast, she said, your big white belly, and those hairy feet., you never cut your nails, and you have fat hands, paws like a cat, your bright red nose, and the biggest balls, I’ve ever seen, you shoot sperm like a, whale shoots water out of the, hole in its back., beast beast beast,, she kissed me,, what do you want for, breakfast?"
    # ]

    # print(gpt3.predict_haiku('Write a poem about fish', examples, examples_context, documents))

    # # Clean DF
    # df = pd.read_csv('data/poems.csv')[['author', 'content']]
    # df['author'] = df['author'].str.lower()
    # df['content'] = df['content'].str.replace('\r\n', ' ')

    # _amount = 100
    # # Generate random examples
    # examples = []
    # sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
    # for sample in sample_df.iterrows():
    #     # print(sample[1][1])
    #     if len(sample[1][1]) < 2048:
    #         examples.append(
    #             [f'Write a poem like {sample[1][0]}', sample[1][1]])

    # # Generate random context
    # fail = True
    # while fail:
    #     _examples_context = sample_df['content'][random.randint(0, _amount)]
    #     if len(sample_df['content'][random.randint(0, _amount)]) < 2048:
    #         examples_context = _examples_context
    #         fail = False

    # # Generate random documents
    # documents = []
    # sample_df = df.sample(frac=1).reset_index(drop=True)[:_amount]
    # for sample in sample_df.iterrows():
    #     if len(sample[1][1]) < 2048:
    #         documents.append(sample[1][1])

    # print(json.dumps(examples, indent=2))
    # print(examples_context)
    # print(json.dumps(documents, indent=2))

    # examples_context = 'Supper comes at five o\'clock, At six, the evening star, My lover comes at eight o\'clock, But eight o\'clock is far, How could I bear my pain all day, Unless I watched to see, The clock-hands laboring to bring Eight o\'clock to me.'

    # print(
    #     gpt3.predict_haiku_test('Write a poem about how today was a terrible', examples[:5], examples_context,
    #                     documents[:15]))
