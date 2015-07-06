#!usr/bin/python
#-*-coding:utf-8-*-

import sys
from collections import defaultdict
import argparse

def n_gram(in_file):
    input_file = open(in_file)
    for line in input_file:
        word_list = line.strip().split()
        word_list.append('</s>')
        word_list.insert(0,'<s>')
        for index in (range(1,len(word_list)-1)):
            counts[word_list[index-1]+' '+word_list[index]] += 1#bi_gramを入れる
            context_count[word_list[index-1]] += 1#uni_gramを入れる
            counts[word_list[index]] += 1#uni_gramを入れる
            context_count[''] += 1#単語数を数える
    model_file = open(args.output_file,'w')
    for n_gram,count in counts.items():
        word_list = n_gram.split()#1語か２語
        word_list.pop()#0語か1語
        context = ''.join(word_list)
        prob = float(counts[n_gram])/context_count[context]
        model_file.write('%s\t%s\n'%(n_gram,prob))
    model_file.close()


if __name__ == '__main__':
    counts = defaultdict(lambda:0)
    context_count = defaultdict(lambda:0)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',dest='input_file',default='../../data/wiki-ja-train.word',help='input')
    parser.add_argument('-m','--model',dest='output_file',default='lm.txt',help='language_model_file')
    args = parser.parse_args()
    n_gram(args.input_file)

