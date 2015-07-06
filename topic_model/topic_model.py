#!usr/bin/python
#coding:utf-8
import random
import math
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',dest= 'in_file',default = '../../data/wiki-en-documents.word')
#parser.add_argument('-i','--input',dest= 'in_file',default = '../../test/07-train.txt')
args = parser.parse_args()
NUM_TOPICS = 10
ALPHA = .001
BETA = .001
Nw = 0
Nt = NUM_TOPICS

words_corpus = []
topics_corpus = []
words_count = defaultdict(int)
topics_count = defaultdict(int)


def AddCount(word, topic, docid, amount):#カウントの追加
    words_count[str(topic)] += amount#topic数をカウント
    words_count[word+'|'+str(topic)] += amount#そのtopicにおけるword数をカウント
    topics_count[str(docid)] += amount#単語の文IDをカウント
    topics_count[str(topic)+'|'+str(docid)] += amount#文において、ある単語がどのtopicになりやすいか

def SampleOne(probs):
    remaining = random.uniform(0,sum(probs))
    for i in range(0,len(probs)):
        remaining -= probs[i]
        if remaining <= 0:
            return i
    print "error"
    exit()

if __name__ == '__main__':
#----------初期化-----------
    for line in open(args.in_file):
        docid = len(words_corpus)#文のID
        topics = []
        words = line.strip().split()
        for word in words:
            topic = random.randint(0,NUM_TOPICS-1)
            topics.append(topic)
            AddCount(word, topic, docid, 1)
            Nw += 1#単語数
        words_corpus.append(words)#1文の単語リストのリスト
        topics_corpus.append(topics)#1文のtopicリストのリスト
#-------サンプリング---------
    ll = 0
    for loop_num in range(0,1000):
        for docid in range(0, len(words_corpus)):
            for wordid in range(0,len(words_corpus[docid])):
                word = words_corpus[docid][wordid]
                topic = topics_corpus[docid][wordid]
                AddCount(word,topic,docid,-1)
                probs = []
                for topic in range(0,NUM_TOPICS):
                    prob = (float(words_count[word+'|'+str(topic)]+ALPHA)/(words_count[str(topic)]+ALPHA))*(float(topics_count[str(topic)+'|'+str(docid)]+BETA)/(topics_count[str(docid)]+BETA))
                    probs.append(prob)
                new_topic = SampleOne(probs)
                ll -= math.log(probs[new_topic])#デバッグのための変数？
                AddCount(word,new_topic,docid,1)
                topics_corpus[docid][wordid] = new_topic
#                if __debug__: print loop_num,'周,対数尤度:',ll,'\n\n'
    result_dict = defaultdict(list)
    for docid in range(0,len(words_corpus)):
        for wordid in range(0,len(words_corpus[docid])):
            result_dict[topics_corpus[docid][wordid]].append(words_corpus[docid][wordid])
    for topic,words in result_dict.items():
        print topic,': ',
        for word in sorted(set(words)):
            print word,
        print ''

