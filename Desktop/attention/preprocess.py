import unicodedata
import string
import re
import random

import konlpy
from konlpy.tag import Hannanum, Okt
from konlpy.utils import pprint
Hannanum = Hannanum()
Okt = Okt()

SOS_token = 0
EOS_token = 1

MAX_LENGTH = 80
MAX_word = 10

eng_path = "./eng368.txt"
kor_path = "./kor368.txt"

eng_prefixes = (
    "i am ", "i m ",
    "he is", "he s ",
    "she is", "she s",
    "you are", "you re ",
    "we are", "we re ",
    "they are", "they re ")

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  #  SOS 와 EOS 단어 숫자 포함

    def addSentence(self, sentence):
        for word in Okt.morphs(sentence):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1
            
# 유니 코드 문자열을 일반 ASCII로 변환하십시오.
# http://stackoverflow.com/a/518232/2809427 에 감사드립니다.
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )
# 소문자, 다듬기, 그리고 문자가 아닌 문자 제거
# 한글 문자열 노머라이징 
def normalizeString1(s):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣 ^☆; ^a-zA-Z.!?]+')
    result = hangul.sub('', s)
    return result

def normalizeString2(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

def readText():
    #print("Reading lines...")

    # Read the file and split into lines
    inputs = open(kor_path, encoding = 'utf-8').read().strip().split("\n")
    outputs = open(eng_path, encoding = 'utf-8').read().strip().split("\n")

    # 모든 줄을 쌍으로 분리하고 정규화 하십시오
    inputs = [s for s in inputs]
    outputs = [s for s in outputs]
    #print(len(inputs))
    #print(len(outputs))    
    inp = Lang('input')
    outp = Lang('output')
    
    pair = []
    for i in range(len(inputs)):
        pair.append([inputs[i], outputs[i]])
        
    return inp, outp, pair
   #input과 output을 갖는 pair라는 리스트를 생성한다.

def filterPair(p):
    return len(p[0].split(' ')) < MAX_word and \
        len(p[1].split(' ')) < MAX_word
#        p[1].startswith(eng_prefixes)

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData():
    input_lang, output_lang, pairs = readText()
    pairs = filterPairs(pairs)
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    return input_lang, output_lang, pairs
