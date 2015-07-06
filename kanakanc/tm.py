#!usr/bin/python
#-*-coding:utf-8-*-

import argparse
from collections import defaultdict

def train(train_file):
    for line in open(train_file):
        words = line.strip().split()
        for kana_kan in words:
            kana,kan = kana_kan.split('_')
            kan_dict[kan] += 1
            emit_dict['%s %s' % (kan,kana)] += 1


def save(model_file):
    m_file = open(model_file,'w')
    for kan_kana,value in sorted(emit_dict.items()):
        m_file.write('%s\t%f\n' % (kan_kana,float(value)/kan_dict[kan_kana.split()[0]]))
        print kan_kana,float(value)/kan_dict[kan_kana.split()[0]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--train',dest='train',default='../../data/wiki-ja-train.pron_word',help = 'input train data')
    parser.add_argument('-w','--model',dest='model',default='tm.txt',help = 'make model file')
    args = parser.parse_args()
    emit_dict = defaultdict(lambda:0)
    kan_dict = defaultdict(lambda:0)
    train(args.train)
    save(args.model)
