#!usr/bin/python
#-*-coding:utf-8-*-

import argparse
import math
from collections import defaultdict


def transition_prob(transition_model):##理解
    transition_prob_dict = defaultdict(lambda:0)
    for line in transition_model:
        transition,prob = line.rstrip().decode('utf-8').split('\t')#どのタイミングでデコードすればいいかわからん！
        transition_prob_dict[transition] = float(prob)
    return transition_prob_dict


def emission_prob(emission_model):##理解
    emission_prob_dict = defaultdict(dict)
    for line in emission_model:
        kana_kan,prob = line.rstrip().decode('utf-8').split('\t')
        kan, kana = kana_kan.split(" ")
     #   print kana,kan
        emission_prob_dict[kana][kan] = float(prob)
    return emission_prob_dict

def bigram_prob(prev_word,now_word):#前の単語から今の単語に遷移する確率？
    P1 = 0.95*transition_prob_dict[prev_word] + 0.05/(10**6)#前の単語の出現確率
    P2 = 0.95*transition_prob_dict[prev_word + ' ' + now_word] + 0.05*P1#前の単語と今の単語(bi_gram)の出現確率
    return P2


def forwardstep(line):
    best_score = defaultdict(dict)
    best_edge = defaultdict(dict)
    best_score[0]['<s>'] = 0
    best_edge[0]['<s>'] = 'NULL'

    for word_end in range(1,len(line) + 1):
        for word_begin in range(word_end):
            moji = line[word_begin:word_end]#文字を取得
            my_tm = emission_prob_dict[moji]#my_tm:取得した文字(かな)が変わり得る漢字dict
            if moji not in my_tm and len(moji) == 1:
                my_tm = {moji:0.0}#一文字のかなが辞書に無かったら追加(そのままの状態が辞書にない場合、追加)
            for now_word,tm_prob in my_tm.items():#変換しうる漢字で回す
 #               print now_word
                best_score[word_end][now_word] = 10**10
                for prev_word, prev_score in best_score[word_begin].items():
                    p_emission = -math.log(0.95*tm_prob + 0.05/(10**6))#その漢字(変換先)になりやすい確率
                    p_transition = -math.log(bigram_prob(prev_word,now_word))#前の文字からその漢字に遷移する確率
                    now_score = prev_score + p_emission + p_transition

                    if word_end not in best_score or now_score < best_score[word_end][now_word]:
                        best_score[word_end][now_word] = now_score
                        best_edge[word_end][now_word] = (word_begin,prev_word)

    l = len(line)

    for prev_word, prev_score in best_score[l].items():
        now_score = prev_score - math.log(bigram_prob(prev_word,'</s>'))#前の文字から</s>に遷移する確率
        if l+1 not in best_score or now_score < best_score[l+1]['</s>']:
            best_score[l+1]['</s>'] = now_score
            best_edge[l+1]['</s>'] = (l,prev_word)
#    print str(best_edge).decode("unicode-escape")
#    exit()
    return best_edge


def backwardstep(best_edge,length):
    partition = list()
    next_edge = best_edge[length+1]['</s>']
    while next_edge != (0,'<s>'):
        position,word = list(next_edge)#タプルをリストにしている
#        print str(next_edge).decode("unicode-escape")
        partition.append(word.encode('utf-8'))#encodeしないとテキストに書き込めない
        next_edge = best_edge[position][word]
    partition.reverse()
    print ''.join(partition)
#    exit()


def kana_kan(emission_model,transition_model,test_file):
    global transition_prob_dict
    global emission_prob_dict
    
    transition_prob_dict = transition_prob(transition_model)
    emission_prob_dict = emission_prob(emission_model)

    for line in test_file:
        line = line.decode('utf-8').strip()
        best_edge = forwardstep(line)
        backwardstep(best_edge,len(line))


def main():
    parser = argparse.ArgumentParser()#インポートしたargparseのクラスArgumentParser()のインスタンスを作る
    parser.add_argument('-t','--tratition',dest='lm',default='lm.txt',help = 'かなの遷移確率')#インスタンスのparserの関数に引数を渡してる
    parser.add_argument('-e','--emission',dest='em',default='em.txt',help = '漢字がかなになる確率')
    parser.add_argument('-i','--input',dest='test',default='../../data/wiki-ja-test.pron',help='input_test_file')
    args = parser.parse_args()#これなにやってるやつ？
    transition_model = open(args.lm)
    emission_model = open(args.em)
    test_file = open(args.test)
    kana_kan(emission_model,transition_model,test_file)
    transition_model.close()
    emission_model.close()
    test_file.close()


if __name__ == '__main__':
    main()

