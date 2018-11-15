import re
import nltk
from decimal import Decimal
from collections import defaultdict
from konlpy.tag import Twitter


word_ko_dict = defaultdict(list)
word_not_ko_dict = defaultdict(list)
cnt_positive = 0
cnt_negative = 0
prob_pos = 0
prob_neg = 0


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
    pair_word_tag_list = t.pos(text)

    for _word, tag in pair_word_tag_list:
        if _word not in word_ko_dict:
            word_ko_dict[_word].append(0)
            word_ko_dict[_word].append(0)

        if state == '0':
            word_ko_dict[_word][0] += 1
        else:
            word_ko_dict[_word][1] += 1


def train_not_hangul(text, state):
    text = text.lower()
    words = nltk.word_tokenize(text)
    pair_word_tag_list = nltk.pos_tag(words)

    for _word, tag in pair_word_tag_list:
        if _word not in word_not_ko_dict:
            word_not_ko_dict[_word].append(0)
            word_not_ko_dict[_word].append(0)

        if state == '0':
            word_not_ko_dict[_word][0] += 1
        else:
            word_not_ko_dict[_word][1] += 1


def classify(text):
    if is_hangul(text):
        return classify_hangul(text)
    else:
        return classify_not_hangul(text)


def classify_hangul(text):
    pair_word_tag_list = t.pos(text)
    pos = prob_pos
    neg = prob_neg
    for _word, tag in pair_word_tag_list:
        if _word in word_ko_dict:
            pos += Decimal(word_ko_dict[_word][1] / (word_ko_dict[_word][0] + word_ko_dict[_word][1])).log10()
            neg += Decimal(word_ko_dict[_word][0] / (word_ko_dict[_word][0] + word_ko_dict[_word][1])).log10()

    if pos > neg:
        return '1'
    else:
        return '0'


def classify_not_hangul(text):
    text = text.lower()
    words = nltk.word_tokenize(text)
    pair_word_tag_list = nltk.pos_tag(words)
    pos = prob_pos
    neg = prob_neg
    for _word, tag in pair_word_tag_list:
        if _word in word_not_ko_dict:
            pos += Decimal(word_not_ko_dict[_word][1] / (word_not_ko_dict[_word][0] + word_not_ko_dict[_word][1])).log10()
            neg += Decimal(word_not_ko_dict[_word][0] / (word_not_ko_dict[_word][0] + word_not_ko_dict[_word][1])).log10()

    if pos > neg:
        return '1'
    else:
        return '0'


print("training start")
with open("ratings_train.txt", encoding="utf-8") as f:
    for line in f:

        if line[-1] is "\n":
            line = line[:-1]

        split = line.split("\t")
        id_movie = split[0]
        document_movie = split[1]
        label_movie = split[2]
        if label_movie == '0':
            cnt_negative += 1
        else:
            cnt_positive += 1

        train(document_movie, label_movie)

print("training end")

# for word, value in word_ko_dict.items():
#     print(word, value[0], value[1])
# for word, value in word_not_ko_dict.items():
#     print(word, value[0], value[1])

prob_pos = Decimal(cnt_positive / (cnt_positive + cnt_negative))
prob_neg = Decimal(cnt_negative / (cnt_positive + cnt_negative))

print(prob_pos)
print(prob_neg)

print("classify..")
result_cnt = 0
result_correct = 0
with open("ratings_valid.txt", encoding="utf-8") as f:
    for line in f:
        if line[-1] is "\n":
            line = line[:-1]

        split = line.split("\t")
        id_movie = split[0]
        document_movie = split[1]
        label_movie = split[2]

        result_cnt += 1
        if label_movie == classify(document_movie):
            result_correct += 1
            print("OK : ", document_movie, label_movie)
        else:
            print("NO : ", document_movie, label_movie)

print(result_cnt)
print(result_correct)