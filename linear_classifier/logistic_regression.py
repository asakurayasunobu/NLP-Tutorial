#!/usr/bin/python
#-*-coding:utf-8-*-

from collections import defaultdict
import math
import random


def create_features(x):
    phi = defaultdict(lambda:0)
    words = x.split()
    for word in words:
        phi['UNI:{}'.format(word)] += 1
    return phi

def predict_one(weight, phi):
    score = 0
    for word, freq in phi.items():
        if word in weight:
            score += freq * weight[word]
    prob = float(1)/(1+math.exp(score))
    prob_d = float(math.exp(score))/(1+math.exp(score))**2
    if score >= 1:
        return 1, prob_d
    else:
        return -1 , prob_d

def update_weights(weight, phi, y, prob_d, a):
    for word, freq in phi.items():
        weight[word] += freq * y * prob_d * a

def predict_all(weight, test_file):
    for line in test_file:
        phi = create_features(line.strip())
        pred_y ,prob_d= predict_one(weight, phi)
        print(pred_y)

def main():
    train_file = open('../nlptutorial/data/titles-en-train.labeled','r')
    test_file = open('../nlptutorial/data/titles-en-test.word','r')
    #--train--
    iterations = range(10)
    weight = defaultdict(lambda:0)
    train_list = list(train_file)
    count = 0
    a = float(1)/(1+count)
    for i in iterations:
        random.shuffle(train_list)
        for line in train_list:
            count += 1
            y, x = line.strip().split('\t')
            phi = create_features(x)
            pred_y, prob_d = predict_one(weight,phi)
            if pred_y != int(y):
                update_weights(weight, phi, int(y), prob_d, a)
    #--test--
    predict_all(weight, test_file)

if __name__ == '__main__':
    main()
