import re
import nltk
from decimal import Decimal
from collections import defaultdict
from konlpy.tag import Twitter
from nltk.corpus import stopwords

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
    pair_word_tag_list = t.pos(text, norm=True, stem=True)
    for _word, tag in pair_word_tag_list:
        if _word not in word_ko_dict:
            word_ko_dict[_word].append(0)
            word_ko_dict[_word].append(0)

        if state == '0':
            word_ko_dict[_word][0] += 1
        else:
            word_ko_dict[_word][1] += 1


stop_words = set(stopwords.words('english'))
stemmer = nltk.stem.PorterStemmer()


def train_not_hangul(text, state):
    text = text.lower()
    words = nltk.word_tokenize(text)
    words_filtered = []

    for w in words:
        if w not in stop_words:
            words_filtered.append(stemmer.stem(w))
    pair_word_tag_list = nltk.pos_tag(words_filtered)

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


ignore_ko_tag = ['Suffix', 'Josa', 'Punctuation']


def classify_hangul(text):
    pair_word_tag_list = t.pos(text, norm=True, stem=True)
    pos = prob_pos
    neg = prob_neg

    length = pair_word_tag_list.__len__()
    power = start_power

    for _word, tag in pair_word_tag_list:
        power += (1 / length) * inc_power
        if tag in ignore_ko_tag:
            continue
        if _word in word_ko_dict:
            pos += (Decimal(
                word_ko_dict[_word][1] / (word_ko_dict[_word][0] + word_ko_dict[_word][1])).log10()) * Decimal(power)
            neg += (Decimal(
                word_ko_dict[_word][0] / (word_ko_dict[_word][0] + word_ko_dict[_word][1])).log10()) * Decimal(power)

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
            pos += Decimal(
                word_not_ko_dict[_word][1] / (word_not_ko_dict[_word][0] + word_not_ko_dict[_word][1])).log10()
            neg += Decimal(
                word_not_ko_dict[_word][0] / (word_not_ko_dict[_word][0] + word_not_ko_dict[_word][1])).log10()

    if pos > neg:
        return '1'
    else:
        return '0'


print("training start")
with open("ratings_train.txt", encoding="utf-8") as f:
    f.readline()
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

prob_pos = Decimal(cnt_positive / (cnt_positive + cnt_negative))
prob_neg = Decimal(cnt_negative / (cnt_positive + cnt_negative))

print("classify start")

threshold = 0.8
start_power = 1
inc_power = 1.2

for key in word_ko_dict:
    word_ko_dict[key][0] += threshold
    word_ko_dict[key][1] += threshold
for key in word_not_ko_dict:
    word_not_ko_dict[key][0] += threshold
    word_not_ko_dict[key][1] += threshold

result_cnt = 0
result_correct = 0
with open("ratings_test.txt", encoding="utf-8") as f:
    header = f.readline()

    with open("ratings_result.txt", 'w', encoding="utf-8") as result_f:
        result_f.write(header)
        for line in f:
            if line[-1] is "\n":
                line = line[:-1]

            split = line.split("\t")
            id_movie = split[0]
            document_movie = split[1]
            label_movie = classify(document_movie)

            result_f.write("{} {} {}\n".format(id_movie, document_movie, label_movie))

print("classify end")
