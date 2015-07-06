#!use/bin/python
#--*--coding:utf-8--*--

import sys
import math
from collections import defaultdict

def probability(input_file):
    freqdict = defaultdict(lambda:0)
    probdict = defaultdict(lambda:0)
    linelist = []
    count = 0

    for line in input_file:
        linelist = line.strip().decode('utf-8').split(' ')
        for word in linelist:
            freqdict[word] += 1
            count += 1
    for word,freq in freqdict.items():
        probdict[word] += float(freq)/count
    return probdict




if __name__ == '__main__':
    input_file = open('../data/wiki-ja-train.word')
    test_file = open('../data/wiki-ja-test.txt')
    probdict = probability(input_file)
    lambda1 = 0.95
#-----前向きステップ--------
    for line in test_file:
        line = line.strip().decode('utf-8')
        best_edge = defaultdict(lambda: '')
        best_score = defaultdict(lambda: 0)
        for word_end in range(1,len(line)+1):
            best_score[word_end] = 10**10
            for word_begin in range(word_end):
                word = line[word_begin:word_end]
                if len(word) == 1 or word in probdict:
                    prob = probdict[word]*lambda1 + (1-lambda1)/(10**10)
                    cor_score = best_score[word_begin]-math.log(prob,2)
                    if cor_score < best_score[word_end]:
                        best_score[word_end] = cor_score
                        best_edge[word_end] = (word_begin,word_end)
                        print best_edge
#----後ろ向きステップ---------
        words = []
        next_edge = best_edge[len(best_edge)]
        while next_edge != '':
            word = line[next_edge[0]:next_edge[1]]
            words.append(word.encode('utf-8'))
            next_edge = best_edge[next_edge[0]]
        words.reverse()
        print ' '.join(words)
