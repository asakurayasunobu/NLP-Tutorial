#!usr/bin/pyhton
#-*-coding:utf-8-*-

import argparse
from collections import defaultdict


def train_hmm(train_file):
    for line in open(train_file):
        words = line.strip().split()
        words.insert(0,'<s>_<s>')
        words.append('</s>_</s>')
        pre_tag = ''
        for word_tag in words:
            word,tag = word_tag.split('_')
            tag_dict[tag] += 1
            #emit_dict:(tag word)の組み合わせの頻度
            emit_dict['%s %s' % (tag,word)] += 1
            if pre_tag is not '':
                #前のtagから今のtagになる頻度 exp:(名詞 動詞)=10回 名詞の次に動詞が来る頻度
                trans_dict["%s %s" % (pre_tag,tag)] += 1
            pre_tag = tag


def save_file(model_file):
    m_file = open(model_file,'w')
    for key,value in sorted(emit_dict.items()):
        #emit_dict:(tag word)がキーでその頻度がvalueとなるdict
        #(tag word)/tag:tagの内(tag word)の組み合わせの確率を計算し、model_fileに書き込む
        m_file.write('E %s %f\n' % (key, value / tag_dict[key.split()[0]]))
        print 'E',key,value /tag_dict[key.split()[0]]
    for key, value in sorted(trans_dict.items()):
        #(pre_tag tag)の頻度/pre_tagの頻度
        m_file.write('T %s %f\n' % (key, value / tag_dict[key.split()[0]]))
        print 'T',key,value/tag_dict[key.split()[0]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default= '../../data/wiki-en-train.norm_pos', help='input model data')
    parser.add_argument('-m','--model',dest='model',default= 'train05_hmm.model', help = 'writing model file')
    args = parser.parse_args()
    tag_dict = defaultdict(lambda:.0)
    emit_dict = defaultdict(lambda:.0)
    trans_dict = defaultdict(lambda:.0)
    train_hmm(args.train)
    save_file(args.model)