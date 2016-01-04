#!usr/bin/python
#coding:utf-8
import math
import random
from collections import defaultdict


def create_features(sentence):
    phi = defaultdict(lambda:0)
    words = []
    words = sentence.strip().split(' ')
    for word in words:
        phi['UNI:'+word] += 1
    return phi


def make_network():
    network = []
    for i in range(node):
        if i == node - 1:
            layer = 2
            weight_dict = defaultdict(lambda:0)
        else:
            layer = 1
            weight_dict = defaultdict(lambda:random.uniform(-0.01,0.01))
        network.append((layer,weight_dict))
    return network


def predict_one(weight_dict,phi):
    score = 0
    for word, freq in phi.items():
        score += freq*weight_dict[word]
    return math.tanh(score)


def predict_nn(network,phi):
    y = [phi,{},{}]#各層の値
    for i in range(node):
        layer,weight = network[i]
        answer = predict_one(weight,y[layer - 1])#前の層の値に基づいて計算
        y[layer][i] = answer
    return y

def update_nn(network,phi,label):
    delta = list()
    lam = 0.5
    k = 1
    for i in range(node):
        delta.append(0)
    y = predict_nn(network,phi)
    for j in range(node -1, -1, -1):
        layer = network[j][0]
        if j == node -1:
            delta[j] = yy - y[2][2]
        else:
            right_node = len([n for n in network if n[0] == layer += 1])
            for i in range(right_node):
                delta[j] += (1 - y[layer][j]*y[layer][j]*delta[j+j+i]*network[j+k+i][1][i])
        k += 1
        if network[j][0] != network[j-1][0]:
            k = 1
    for j in range(node):
        layer, w = network[j]
        for name, val in y[layer -1].items():
            w[name] += lam*delta[j]*val
        network[j] = (layer, w)
    return network


def train_perceptron(iter_):
    train_file = open('../../data/titles-en-train.labeled')
    test_file = open('../../data/titles-en-test.word')
    network = make_network()
    for i in range(iter_):
        for line in input_file:
            sentence, label = line.strip().split('\t')
            label = int(label)
            phi = create_features(sentence)
            network = update_nn(network,phi,label)
    return network

if __name__ == '__main__':
    node = 3
    iter_ = 10
    train_perceptron(iter_)


