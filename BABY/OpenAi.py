import os
import openai
from dotenv import load_dotenv
import pandas as pd
import json
import random
from google.cloud import storage

# BUCKET_NAME = 'wagon-data-735-babyproject'
# BUCKET_PROMPT_HELP = 'train_data/prompt_help.json'
# from data import get_data_prompt_help

load_dotenv()

# Load your API key from a .env file
openai.api_key = os.getenv("OPEN_AI_KEY")

def get_data_prompt_help():
    # df = pd.read_json(f"gs://{BUCKET_NAME}/{BUCKET_PROMPT_HELP}")
    # res = json.loads(df.to_json(orient="columns"))

    # Static (gcp doesn't work yet)
    res = {
        "rap": {
            "examples_context":
            "Whether in a penthouse or a cave dweller. I can tell you 'bout now I'm not a fortune teller. Grab a treat from Yosi my muffin seller. Got mad technique like Rudy Van Geller. And yes I got a plan I'm a carry out it. Yes I'm pro-choice I'm a scream and shout it. Yes I love life and I try not to doubt it. Yes I'm gonna body 'cause I'm 'bout it 'bout it. When it rains I don't use an umbrella. When I write rhymes, I use indella, the ink. That will make you think. Flowing like water that you love to drink.",
            "examples":
            [[
                "Write a gangsta rap song verse about lifestyle",
                "Summertime white porsche carrera is milky. Im on the grind let my paper stack when I'm filthy. Funny how a nigga get the screw facing at me. Anyhow, they aint got the heart to get at me. I'll get down, southsides the hood that I come from. So I dont cruise to nobodys hood without my gun. You know the kid aint gonna follow that bullshit. try and stick me imma let off a full clip. It aint my fault you done fucked up your re-up. At the dice game who told you put a G up. Everybody mad when their paper dont stack right. When I come around y'all niggas better act right. When we got the tops down, you can hear the system thump. When we rollin' rollin' rollin'."
            ],
             [
                 "Write an egotrip rap song verse",
                 "Rip Whitney Houston. God bless her soul. I'm just vibin' dog. But for you haters. Nothing's gonna stop me. I swear to god. Nothing's gonna stop me. Andi, Kiko, Renegades. Nothing's gonna stop me. Nothing's gonna stop me. Money talks so what's your conversation?. Counting my blesses, my sweet elaborated. Being broke ain't a joke, that feeling is devastating. Night met 'er so that force never stated. Calculating every dollar bill. Reminiscin', they missin' like someone not a mill. Still trippin', this life I'm livin' the dream still. Look at my niggas loyalty's mad real. That's cuz we got this from the bottom up. Number slidin' in my homie momma truck. We did what we had to do, we ain't give a fuck. Now we the niggas winnin' dog, wuddup?."
             ],
             [
                 "Write a rap song verse about girls and love",
                 "So soft and slow. Never knew a girl could be so goddamn cold,. I know, the way she move got me spendin my dough. And yo, If you would've seen what i seen on that pole. Just know,. That I was wrong for fallin in love. I was wrong for fallin in love. [They always say don't love a ho]. I was wrong for fallin in love. [Don't do it yo']. I was wrong for fallin in love. [They always say don't love a ho]. But I just went against the grain. It was a feelin I can't explain. And it felt like harmony. Singin in my face like. diddy-duhdee doo-dah-day."
             ],
             [
                 "Write a rap song verse about success and wealth",
                 "What makes you want to live again. goodbye my enemies, hello my friends. and what would make you forgive the man. who was once your enemy but now your friend. the sunshine is waiting for me on the other side of the rainbow. the point of no return, my life's changing. for the better. the better. 'cause now I know better. so, thanks to my past. oh, baby now it's all better. let's make this shit last. oh, yes, 'cause now I know better. so, thanks to my past. oh, yes, I know there nothing better than now. hello pretenders, hello my friends. hello to those who didn't want us to win. hello backstabber and your cheap grin. there's more just like you that's listening. the sunshine is waiting for me on the other side of the rainbow. the point of no return, my life's changing. for the better. the better. 'cause now I know better. so, thanks to my past. oh, baby now it's all better. let's make this shit last. oh, yes, 'cause now I know better. so, thanks to my past. oh, yes, I know there nothing better than now. I know there nothing better than now. 'cause now I know better. so, thanks to my past. oh, baby now it's all better. let's make this shit last. oh, yes, 'cause now I know better. so, thanks to my past. oh, yes, I know there nothing better than now"
             ],
             [
                 "Write a rap song verse about god and girls",
                 "I'm gon' praise him, praise him till I'm gone. I'm gon' praise him, praise him till I'm gone. When the praises go up, the blessings come down. When the praises go up, the blessings come down. It seems like blessings keep falling in my lap. It seems like blessings keep falling in my lap. I don't make songs for free I make 'em for freedom. Don't believe in kings, believe in the kingdom. Chisel me into stone, prayer whistle me into song air. Dying laughing with Krillin. saying something 'bout blonde hair. Jesus black life ain't matter. I know I talked to his daddy. Said you the man of the house now. look out for your family. He has ordered my steps. gave me a sword with a crest. And gave Donnie a trumpet. in case I get shortness of breath. I'm gon' praise him, praise him till I'm gone. Don't be mad. I'm gon' praise him, praise him till I'm gone. When the praises go up. Good God."
             ],
             [
                 "Write a rap song verse about life and motivation",
                 "Whether in a penthouse or a cave dweller. I can tell you 'bout now I'm not a fortune teller. Grab a treat from Yosi my muffin seller. Got mad technique like Rudy Van Geller. And yes I got a plan I'm a carry out it. Yes I'm pro-choice I'm a scream and shout it. Yes I love life and I try not to doubt it. Yes I'm gonna body 'cause I'm 'bout it 'bout it. When it rains I don't use an umbrella. When I write rhymes, I use indella, the ink. That will make you think. Flowing like water that you love to drink."
             ]],
            "documents": [
                "Your body's an isosceles. And I'm just tryna try angles. Your love is trigonometry. Just tryna solve the whole equation. What's it about you (about you). I wanna love you. Figure it out, figure it out. So I can touch you. Should we do that? Can I do that? (baby). Answers are usually in the back. Substitution, add me in. Multiply my love. Is that too much?. Substitution. What's the problem, girl?. Add me in. Baby just add me, baby just add me in. Baby just add me, baby just add me in.",
                "In my mind I'm a fighter, my heart's a lighter. My soul is the fluid, my flow sparks it right up. Arsenic writer, author with arthritis. Carpel tunnel, Marshall will start shit-itis. Hard headed and hot headed, bull headed and pig headed. dick headed, a prick, a big headache I'm sick. quick witted, for every lyric spitted. There are six critics who wait for me to slip with it, so quick. This dynamite stick buried the wick. it's gonna explode any minute, some lunatic lit it, and it's not Nelly. Do not tell me to stop yelling, when I stop selling, I quit so.",
                "Yeah, ya know? Critics man. Critics never got nothin' nice to say, man. You know the one thing I notice about critics, man?. Is critics never ask me how my day went. Well, I'mma tell 'em. Yesterday my dog died, I hog tied a ho, tied her in a bow. Said next time you blow up try to spit a flow. You wanna criticize dog try a little mo'. I'm so tired of this I could blow, fire in the hole. I'm fired up so fire up the lighter and the 'dro. Better hold on a little tighter here I go. Flows tighter, hot headed as ghost rider. Cold hearted as spiderman throwin' a spider in the snow. So ya better get to blowin in flow rider. Inside of a low rider with no tires in the hole. Why am I like this? Why is winter cold?. Why is it when I talk, I'm so biased to the hoes?. Listen dog.",
                "I thought that I was dreaming. When you said you love me. It started from nothing. I had no chance to prepare. I couldn't see you coming. It started from nothing. I could hate you now. It's quite alright to hate me now. When we both know that deep down. The feeling still deep down is good. . If I could see through walls. I could see you're faking. If you could see my thoughts. You would see our faces. Safe in my rental like an armored truck back then. We didn't give a fuck back then. I ain't a kid no more. We'll never be those kids again. We'd drive to Syd's, had the X6 back then. Back then. No matter what I did. My waves wouldn't dip back then. Everything sucked back then. We were friends. . I thought that I was dreaming. When you said you love me. It started from nothing. I had no chance to prepare. I couldn't see you coming. It started from nothing. I could hate you now. It's quite alright to hate me now. When we both know that deep down. The feeling still deep down is good. . In the halls of your hotel. Arm around my shoulder so I could tell. How much I meant to you. Meant it sincere back then. We had time to kill back then. You ain't a kid no more. We'll never be those kids again. It's not the same, ivory's illegal. Don't you remember?. I broke your heart last week. You'll probably feel better by the weekend. Still remember, had you going crazy. Scream my name. The feeling deep down is good. . I thought that I was dreaming. When you said you love me. It started from nothing. I had no chance to prepare. I couldn't see you coming. It started from nothing. I could hate you now. It's alright to hate me now. When we both know that deep down. The feeling still deep down is good. . All the things I didn't mean to say. I didn't mean to do. There were things you didn't need to say. Didn't need to...need to. I could dream all night. Dream all night. I could drive all night. Drive all night. Dreaming, dreamin'",
                "This right here it's payback. from way back I dont play that x 4. recognise a real dime when you see one. and don't try to be one, ya fuckin biatch. I been like Dion for eons. You aint nothin but a biatch. You messed around and let me read up. I come abck through and tear the street up. Ice cube nigga you better D up. And when I come by bitch, you better be up. Ass suck, face in the pillow. I dont give a fizzle. got to do my nizzle. the only nizzle that I never ever fizzled. origional, you niggas know. (right here right now) who wants some you better get em up. (right here right now)come get some you better get em up x3. got to get with ya. hit you wit these things that Im holdin. who wanna squab wit that frozen. now who wanna battle with the chosen.",
                "Haha, yeah. Whattup ma? How you been. Yeah I know, I know, hehe. It's all good... (Murder Inc.). Girl your stare, those eyes I. (love it when you look at me baby). Your lips, your smile I. (love it when you kiss me baby). Your hips, those thighs, I. (love it when you thug me baby). And I can't, deny I. (love it when I'm witchu baby). I, got a fetish for fuckin you witcha skirt on. On the backstreet in the back seat of the Yukon. What's takin so long? I'm gettin anxious. But patiently waitin for you. To tell a nigga to move on. Between me and you, we can find each other. flyin abroad in my private G-2. I ain't tryin to G you, ma I'm tryin to see you. Bend over, you know how we do it. Feet to shoulders. Bring heat to coldest night, so ferocious. Now you street promotin the dick game is potent. Cause in the bed a nigga go hard like Jordan. Sweat pourin, lovin the way you be moanin. Grippin the sheets, lookin at me lickin at me. Cause every woman just."
            ]
        }
    }

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

    def completion(
        self,
        prompt,
        temperature=1,
        n=1,
        top_p=1,
        presence_penalty=0,
        frequency_penalty=0
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
            frequency_penalty=frequency_penalty
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
    # print(
    #     gpt3.answers('Write a rap song vers about drinking and gambling', data['examples'], data['examples_context'], data['documents'],
    #                 0.9, 2, _type='rap'))

    print(
        gpt3.completion('Write a haiku about flowers'))
