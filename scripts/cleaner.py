import re
import emoji
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemma = WordNetLemmatizer()



def cleaner(tweet_list):
    # clean tweets
    clean_tweets = [tweet_cleaner(x) for x in tweet_list]
    # remove empty strings
    no_empty_strings = [i for i in clean_tweets if i]
    # unicode
    uni_tweets = [unicode_maker(x) for x in no_empty_strings]
    # tokinze
    tokens = [text_to_token(s) for s in uni_tweets]
    # lemmatize
    lemmas = [get_lemm(s) for s in tokens]
    # one long list of keywords
    flattened = [word for sublist in lemmas for word in sublist]
    return flattened



def tweet_cleaner(tweet):
    '''removes the usual clutter in everyday tweets'''
    # removes mentions
    mentions_free = re.sub("@\w+", "", tweet)
    # removes hashtags
    hashtag_free = re.sub("#\w+", "", mentions_free)
    # special shortcuts
    rt_free = re.sub("^RT", "", hashtag_free)
    # removes url
    url_free = re.sub(r'http\S+', '', rt_free)
    # removes emojis
    emo_free = emoji.get_emoji_regexp().sub(u'', url_free)
    # removes white space
    stripped = emo_free.strip()

    return stripped




def unicode_maker(text):
    # creating a unicode string
    text_encode = text.encode(encoding="ascii", errors="ignore")
    text_decode = text_encode.decode()
    clean_text = " ".join([word for word in text_decode.split()])

    return clean_text




def text_to_token(sentence):
    # remove numbers
    number_free = ''.join(word for word in sentence if not word.isdigit())
    # remove punctuation
    punctuation_free = "".join(
        [i for i in number_free if i not in string.punctuation])
    # lower case
    upper_free = punctuation_free.lower()
    # tokenize
    word_tokens = word_tokenize(upper_free)
    # remove stopwords
    important_words = [w for w in word_tokens if not w in stop_words]

    return important_words




def get_lemm(l):
    lemm = [lemma.lemmatize(word) for word in l]

    return lemm
