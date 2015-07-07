#!/usr/bin/python
# _*_ coding:utf-8 _*_

import sys
import math
from collections import defaultdict

def transition_prob(model_transition):

    transition_prob_dict = defaultdict(lambda: 0)
    for line in model_transition:
        ngram, prob = line.rstrip().decode("utf-8").split("\t")
        transition_prob_dict[ngram] = float(prob)
    return transition_prob_dict

def emission_prob(model_emission):

    emission_prob_dict = defaultdict(dict)
    for line in model_emission:
        kana_kanji, prob = line.rstrip().decode("utf-8").split("\t")
        # rstrip()じゃないと[かな 漢字]のかなの部分にスペースが消える
        kana, kanji = kana_kanji.split(" ")
        emission_prob_dict[kana][kanji] = float(prob)   
    return emission_prob_dict

def prob_of_bigram(prev_word, curr_word):
  
    P1 = 0.95*transition_prob_dict[prev_word] +0.05/(10**6)
    P2 = 0.95*transition_prob_dict[prev_word+" "+curr_word]+0.05*P1

    return P2

def forwardstep(line): # 前向きステップ

    best_score = defaultdict(dict)
    best_edge  = defaultdict(dict)
    
    best_score[0]["<s>"] = 0
    best_edge[0]["<s>"]  = "NULL"

    for word_end in range(1, len(line)+1):
        for word_begin in range(word_end):
            moji = line[word_begin:word_end]
            my_tm = emission_prob_dict[moji]
            if moji not in my_tm and len(moji) == 1:
               my_tm = {moji:0.0}
            for curr_word, tm_prob in my_tm.items():
                best_score[word_end][curr_word] = 10**10
                for prev_word, prev_score in best_score[word_begin].items():
           
                    p_emit     = -math.log(0.95*tm_prob + 0.05/(10**6))
                    p_trans    = -math.log(prob_of_bigram(prev_word, curr_word))
                    curr_score = prev_score + p_emit + p_trans

                    if word_end not in best_score or curr_score < best_score[word_end][curr_word]:
                       best_score[word_end][curr_word] = curr_score
                       best_edge[word_end][curr_word]  = (word_begin, prev_word)
    l = len(line)
    
    for prev_word, prev_score in best_score[l].items():
        curr_score = prev_score - math.log(prob_of_bigram(prev_word, "</s>"))
        if l+1 not in best_score or curr_score < best_score[l+1]["</s>"]:
           best_score[l+1]["</s>"] =curr_score
           best_edge[l+1]["</s>"]  = (l, prev_word)
    return best_edge

def backwardstep(best_edge, length): # 後ろ向きステップ
    partition = list()
    next_edge = best_edge[length+1]["</s>"]
    while next_edge != (0, "<s>"):
          position, word = list(next_edge)
          partition.append(word.encode("utf-8"))
          next_edge = best_edge[position][word]
    partition.reverse()
    print " ".join(partition)

def kana_kanji(model_emission, model_transition, test_file):

    global transition_prob_dict
    global emission_prob_dict

    transition_prob_dict = transition_prob(model_transition) 
    emission_prob_dict   = emission_prob(model_emission)

    for line in test_file:
        line = line.decode("utf-8").strip()
        best_edge = forwardstep(line)
        backwardstep(best_edge, len(line))

def main():
    
    model_transition  = open(sys.argv[1], "r")
    model_emission    = open(sys.argv[2], "r")
    test_file         = open(sys.argv[3], "r")
    kana_kanji(model_emission, model_transition, test_file)
    model_emission.close()
    model_transition.close()
    test_file.close()

if __name__=="__main__":
    main()
    
