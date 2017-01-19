from __future__ import print_function, unicode_literals,division
from nltk.tokenize import word_tokenize
import random
import logging
import os
import sys
import nltk
from textblob import TextBlob



os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


HELLO_WORLD = ("hello", "hi", "greetings", "what's up")

INTRO_RES = ["\nHi, its my Pleasure to meet you"]

INTRO_ASK = ["\nI am doing great. How about you?"]

MY_INF = ["\nI am a chatbot made by Kayla.",]

LOC_INF = ["At LA", "London", "Seoul",]

TIME_INF = ["Tmmrw","Next week!"]

OTHERS_INF = ["I knew {pronoun} {verb} {noun}"]


NONE_RESPONSES = [
    "um... Okay..",
    "I guess you would say that",
]

BOT_DETAIL = [
    "Why do you want to know about {noun} ",
    "I have no idea that you like {noun}",
]

BOT_ANS = [
    "Tell me more about {noun}",
]

BOT_DES = [
    "Thank you. You are also {adjctv} ",
    "Am I really {adjctv} bot?",
]



def starts_with_vowel(word):
    return True if word[0] in 'aeiou' else False

def debug(tagged):
    logger.info("debug: respond to %s", tagged)
    resp = respond(tagged)
    return resp




def bot_response(pronoun, noun, verb):

    resp = []

    #if pronoun:
        #resp.append(pronoun)

    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', 'are',): 
            if pronoun == 'you':
                resp.append("are")               
            else:
                resp.append(verb_word)
    if noun:
        #pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(verb +" "+ pronoun +" "+ noun + "?")


    return " ".join(resp)


def resp_bot(pronoun, noun, adjctv, verb, adverb):

    resp = None
    if pronoun == 'I' and (noun or adjctv):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(BOT_DETAIL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(BOT_ANS).format(**{'noun': noun})
        else:
            resp = random.choice(BOT_DES).format(**{'adjctv': adjctv})
    return resp



def preprocess_text(tagged):
    cleaned = []
    words = tagged.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)



def respond(phrase):

    tokens = word_tokenize(phrase)
    #print(tokens)
    tagged = nltk.pos_tag(tokens)
    #print(tagged)
    
    nouns = [word for word,pos in tagged \
    if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]


    verbs = [word for word,pos in tagged \
    if (pos == 'VB' or pos == 'VBP' or pos == 'VBZ')]


    adjctvs = [word for word,pos in tagged \
    if (pos == 'JJ')]


    adverbs = [word for word,pos in tagged \
    if (pos == 'WRB' or pos == 'WP')]


    pronouns = [word for word,pos in tagged \
    if (pos == 'PRP' or pos =='PRP$')]

    #print("nouns=",nouns,"verbs=",verbs,"adjctvs=",adjctvs,"adverbs=",adverbs,"pronouns=",pronouns,)


    if adverbs:
        if adverbs[0]=='who':
            return random.choice(MY_INF)
        elif adverbs[0]=='how':
            return random.choice(INTRO_ASK)
        elif adverbs[0]=='where':
            return random.choice(LOC_INF)
           

    if not pronouns:
        resp = random.choice(NONE_RESPONSES)
    elif pronouns[0] == 'I' and not verbs:
        resp = random.choice(MY_INF)
    elif pronouns and verbs and adjctvs and nouns and adverbs:
        resp = resp_bot(pronouns[0], nouns[0], adjctvs[0], verbs[0], adverbs[0])
    elif pronouns and nouns and verbs:
        resp = bot_response(pronouns[0], nouns[0], verbs[0])
    else:
        resp = ("I dont understand that.")
    if not resp:
        resp = random.choice(NONE_RESPONSES)


    return resp


def main(argv):
    if (len(sys.argv) > 0):
        phrase = sys.argv[1]
    else:
        phrase = "I am a chatbot"

    #print(tagged)
    #print(debug(phrase))


if __name__ == '__main__':
    main(sys.argv[1])
