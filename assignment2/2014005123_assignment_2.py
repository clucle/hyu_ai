import re
import nltk

from konlpy.tag import Twitter;


# https://github.com/chandong83/python_hangul_check_function
def is_hangul(text):
    return len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text)) > 0


# state : 0 negative / 1 positive
def train(text, state):
    if is_hangul(text):
        train_hangul(text, state)
    else:
        train_not_hangul(text, state)


t = Twitter()


def train_hangul(text, state):
    tokens = t.pos(text)
    pair_word_tag_list = nltk.pos_tag(tokens)
    print(pair_word_tag_list)


def train_not_hangul(text, state):
    text = text.lower()
    words = nltk.word_tokenize(text)
    pair_word_tag_list = nltk.pos_tag(words)
    print(pair_word_tag_list)


with open("ratings_train.txt", encoding="utf-8") as f:
    for line in f:
        if line[-1] is "\n":
            line = line[:-1]

        split = line.split("\t")
        id_movie = split[0]
        document_movie = split[1]
        label_movie = split[2]

        train(document_movie, label_movie)

