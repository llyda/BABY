import re
import emoji
import string
from nltk.corpus import stopwords
import json
stop_words = set(stopwords.words('english'))




def cleaner(tweet_list):
    '''combines different cleansing methods'''
    # clean tweets
    clean_tweets = [tweet_cleaner(x) for x in tweet_list]
    # unicode
    uni_tweets = [unicode_maker(x) for x in clean_tweets]
    # remove numbers and punctuation
    number_free = [number_punct(x) for x in uni_tweets]
    # tweets longer than two words
    more_than_two = [x for x in number_free if (len(x.split())>2)]
    # remove duplicates
    clean_set = set(more_than_two)
    # remove empty strings
    no_empty_strings = [i for i in clean_set if i]
    # strip whitespace in front and end
    stripped = [x.strip() for x in no_empty_strings]
    # fix double spaces
    one_space = [re.sub(' +', ' ', x) for x in stripped]
    # make one long string with full stop and linebreak
    one_long_string = ".\n".join(one_space)

    return one_long_string




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
    '''get's rid of unicode'''
    # creating a unicode string
    text_encode = text.encode(encoding="ascii", errors="ignore")
    text_decode = text_encode.decode()
    clean_text = " ".join([word for word in text_decode.split()])

    return clean_text



def number_punct(sentence):
    '''removes numbers, punctuation, uppercase'''
    # remove numbers
    number_free = ''.join(word for word in sentence if not word.isdigit())
    # remove punctuation
    punctuation_free = "".join(
        [i for i in number_free if i not in string.punctuation])
    # lower case
    upper_free = punctuation_free.lower()

    return upper_free
