#!/usr/bin/python
#-*-coding:utf-8-*-

import random
import math
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, name, lam, input_d):
        self._weight = np.random.uniform(-0.1, 0.1 , input_d)
        self._name = name
        self._delta = 0
        self._predict = 0
        self._lam = lam
        self._loss = 0

    def predict(self, inputs):
        print(self._weight, inputs)
        score = np.dot(self._weight, inputs)
        self._predict = math.tanh(score)
    def calc_delta(self, next_perceptrons, label = None):
        if label:
            self._delta = label - self._predict
            self._loss += abs(self._delta)
        else:
            s = sum(p.get_delta() *p.get_weight()[self._name] for p in next_perceptrons)
            self._delta = (1-self._predict ** 2) * 2
    def get_all_weight(self):
        return self._weight
    def update_weight(self, inputs):
        self._weight += self._lam * self._delta * inputs
    def get_delta(self):
        return self._delta
    def get_name(self):
        return self._name
    def get_weight_d(self):
        return len(self._weight[0])
    def get_weight(self):
        return self._weight
    def get_predict(self):
        return self._predict
def make_ids(train_list):
    ids = defaultdict(lambda: len(ids))
    for line in train_list:
        sent = line.strip().split('\n')[-1]
        for word in sent.split():
            ids['UNI:{}'.format(word)]
    return ids
def init(layer_and_node, ids):
    lam = 0.5
    layers = list()
    input_d = len(ids)
    for layer in layer_and_node:#[2,1]
        count = 0
        perceptrons = list()
        for node in range(layer):
            perceptrons.append(Perceptron(count, lam, input_d))
            count += 1
        layers.append(perceptrons)
        input_d = layer
    return layers

def create_features(sentence, ids):
    phi = np.zeros(len(ids))
    for word in sentence.strip().split():
        phi[ids['UNI:{}'.format(word)]] += 1
    return phi

def forward_prop(layers, inputss):
    for layer in layers:
        inputs = list()
        for perceptron in layer:
            perceptron.predict(inputss[-1])
            inputs.append(perceptron.get_predict())
        inputss.append(np.ndarray(inputs))
    inputss.pop(-1)

def back_prop(layers, inputss, gold):
    prev_layer = None
    for layer, inputs in zip(layers[::-1], inputss[::-1]):
        for perceptron in layer:
            if prev_layer is None:
                perceptron.calc_delta(None, label=gold)
            else:
                perceptron.calc_delta(prev_layer)
            perceptron.update_weight(inputs)

def train(layers, ids, train_list):
    inputss = list()
    for line in train_list:
        gold, sentence = line.strip().split('\t')
        phi = create_features(sentence, ids)
        inputss.append(phi)
        forward_prop(layers, inputss)
        back_prop(layers, inputss, float(gold))

def main():
    train_list = list(open('../nlptutorial/data/titles-en-train.labeled'))
    test_file = open('../nlptutorial/data/titles-en-test.word')
    layer_and_node = [2,1]
    epoch = 10
    loss_list = list()
    ids = make_ids(train_list)
    layers = init(layer_and_node,ids)
    for i in range(epoch):
        random.shuffle(train_list)
        train(layers, ids, train_list)
        loss_list.append(layers[-1][0]._loss)
        layers[-1][0]._loss = 0
    x = np.arange(0, epoch, 1)
    y = loss_list
    plt.plot(x,y)
    plt.show()




if __name__ == '__main__':
    main()
