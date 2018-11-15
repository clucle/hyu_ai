import re
import nltk
from nltk.corpus import stopwords


# https://github.com/chandong83/python_hangul_check_function
def is_hangul(text):
    return len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text)) > 0


# state : 0 negative / 1 positive
def train(text, state):
    if is_hangul(text):
        pass
        # train_hangul(text, state)
    else:
        train_not_hangul(text, state)


def train_hangul(text, state):
    print(text)


def train_not_hangul(text, state):
    # 소문자로 처리
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    stemmer = nltk.stem.PorterStemmer()
    words = nltk.word_tokenize(text)
    words_filtered = []

    for w in words:
        if w not in stop_words:
            words_filtered.append(stemmer.stem(w))
    # print(text)
    # print(words_filtered)
    tags = nltk.pos_tag(words_filtered)
    print(text)
    print(tags)


with open("ratings_train.txt", encoding="utf-8") as f:
    for line in f:
        if line[-1] is "\n":
            line = line[:-1]

        split = line.split("\t")
        id_movie = split[0]
        document_movie = split[1]
        label_movie = split[2]

        train(document_movie, label_movie)
