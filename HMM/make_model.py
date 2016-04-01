#!/usr/bin/python
#-*-coding:utf8-*-

from collections import defaultdict

def main():
    train_file = open('../nlptutorial/data/wiki-en-train.norm_pos','r')
    model_file = open('model_file.txt','w')
    emit = defaultdict(lambda:0)
    transition = defaultdict(lambda:0)
    context = defaultdict(lambda:0)
    for line in train_file:
        previous = '<s>'
        context[previous] += 1
        wordtags = line.strip().split()
        for wordtag in wordtags:
            word, tag = wordtag.split('_')
            transition[previous+' '+tag] += 1
            context[tag] += 1
            emit[tag+' '+word] += 1
            previous = tag
        transition[previous+' </s>'] += 1
    for key, value in transition.items():
        previous, word = key.split()
        model_file.write('T\t{}\t{}\n'.format(key,float(value)/context[previous]))
    for key, value in emit.items():
        tag,word = key.split()
        model_file.write('E\t{}\t{}\n'.format(key,float(value)/context[tag]))


if __name__ == '__main__':
    main()
