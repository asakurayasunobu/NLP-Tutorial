#!/usr/bin/python
#-*-coding:utf-8-*-

from collections import defaultdict
import math


def read_model(model_file):
    transition = defaultdict(lambda:0)
    emission = defaultdict(lambda:0)
    possible_tags = defaultdict(lambda:0)
    for line in model_file:
        type_, context, word, prob = line.strip().split()
        possible_tags[context] += 1
        if type_ == 'T':
            transition["{} {}".format(context,word)] = float(prob)
        else:
            emission["{} {}".format(context,word)] = float(prob)
    return transition, emission, possible_tags

def main():
    test_file = open('../nlptutorial/data/wiki-en-test.norm','r')
    transition, emission, possible_tags = read_model(open('model_file.txt','r'))
    lambda_ = 0.999
    V = 10*10
    for line in test_file:
        best_score = defaultdict(lambda:0)
        best_edge = defaultdict(lambda:'')
        best_score['0 <s>'] = 0
        best_edge['0 <s>'] = ''
        words = line.strip().split()
        l = len(words)
        for i in range(l):
            for prev in possible_tags.keys():
                for next_ in possible_tags.keys():
                    if '{} {}'.format(i, prev) in best_score and '{} {}'.format(prev, next_) in transition:
                        Pt = transition['{} {}'.format(prev, next_)]
                        Pe = lambda_*emission['{} {}'.format(next_, words[i])] + (1-lambda_)/V
                        score = best_score["{} {}".format(i,prev)] - math.log(Pt,2) - math.log(Pe,2)
                        if '{} {}'.format(i+1, next_) not in best_score or best_score['{} {}'.format(i+1, next_)] > score:
                            best_score['{} {}'.format(i+1, next_)] = score
                            best_edge['{} {}'.format(i+1, next_)] = '{} {}'.format(i, prev)
        for prev in possible_tags.keys():
            if '{} {}'.format(l,prev) in best_score and '{} </s>'.format(prev) in transition:
                Pt = transition['{} </s>'.format(prev)]
                Pe = lambda_*emission['</s> </s>'] + (1-lambda_)/V
                score = best_score['{} {}'.format(l,prev)] - math.log(Pt,2) - math.log(Pe,2)
                if '{} </s>'.format(l+1) not in best_score or best_score['{} </s>'.format(l+1)] > score:
                    best_score['{} </s>'.format(l+1)] = score
                    best_edge['{} </s>'.format(l+1)] = '{} {}'.format(l, prev)
        tags = list()
        next_edge = best_edge["{} </s>".format(l+1)]
        while next_edge != "0 <s>":
            position, tag = next_edge.split()
            tags.append(tag)
            next_edge = best_edge[next_edge]
        tags.reverse()
        print(' '.join(tags))





if __name__ == '__main__':
    main()
