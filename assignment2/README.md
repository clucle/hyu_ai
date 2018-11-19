# classify

보고서 docx가 깨지는 것 같아서 pdf같이 첨부합니다

2014005123_asssignment_2.pdf

# Usage

```bash

# python3, 기타 설치
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install g++ openjdk-8-jdk python-dev python3-dev

# virtual env
sudo apt-get install python3-venv
# 이미 생성 해둠 virtualenv -p python3 venv_2014005123
source venv_2014005123/bin/activate

# stopwords down
python3
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')

```

2014005123_assignment_2.py 실행하면 

ratings_train.txt 를 훈련시키고

ratings_test.txt 를 읽어서

ratings_result.txt 를 생성합니다

