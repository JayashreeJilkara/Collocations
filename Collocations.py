import sys
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from nltk.collocations import *
import operator
import math


def chi_squared():

    bigramtotal = sum(btable.values())
    freq = {}
    for k in btable.keys():
        expected = (((btable[k] + (utable[k.split()[0]] - btable[k])) / bigramtotal) * ((btable[k] + (utable[k.split()[1]] - btable[k])) / bigramtotal)) * bigramtotal
        chi_square = ((btable[k] - expected) ** 2) / expected
        freq[k] = chi_square

    sscores = sorted(freq.items(), key=operator.itemgetter(1), reverse=False)[:20]
    return sscores

def pmi():

    freq = {}

    for k in btable.keys():
        freq[k] = math.log(btable[k] / ( utable[k.split()[0]] * utable[k.split()[1]]))
    sscores = sorted(freq.items(), key=operator.itemgetter(1), reverse=False)[:20]
    return sscores

tokenizer = RegexpTokenizer(r'\w+')
input_text_1 = sys.argv[1]
input_text_2 = sys.argv[2]
unigrams = []
bigrams = []
with open(input_text_1, 'r') as file:
    for line in file.readlines():
        token = tokenizer.tokenize(line)
        for f in token:
            unigrams.append(f)

        bi = ngrams(token, 2)
        bi2 = [' '.join(grams) for grams in bi]
        for g in bi2:
            bigrams.append(g)


utable = {}
btable = {}

for i in unigrams:
    if i not in utable:
        utable[i]=1
    else:
        utable[i]+=1

for i in bigrams:
    if i not in btable:
        btable[i]=1
    else:
        btable[i]+=1

results = []
if input_text_2 == "chi-square":
    result= chi_squared()
    for i in result:
        print('%s Score: %s' % (i[0], i[1]))
elif input_text_2 == "PMI":
    result = pmi()
    for i in result:
        print(' %s Score: %s' % (i[0], i[1]))