#!usr/bin/python
#coding:utf-8

import random
import math
import pickle
from docopt import docopt
from perceptron import Perceptron
from collections import defaultdict


class Perceptron:
    def __init__(self,name,lam):
        self._weight = dict()
        self._name = name
        self._delta = 0
        self._predict = 0
        self._lam = lam

    def predict(self,inputs):
        score = 0
        for name in inputs.keys():
            if not name in self._weight:
                self._weight[name] = random.uniform(-.01,.01)
            score += inputs[name]*self.weight[name]
        self._predict = math.tanh(score)

    def calc_delta(self, next_perceptrons, label=None):
        if label:
            self._delta = label - self._predict
        else:
            s = sum(p.get_delta()*p.get_eright(self._name) for p in next_perceptrons)

    def get_delta(self):
        return self._delta

    def get_weight(self, name):
        return self.weight[name]

    def get_predict(self):
        return self._predict

    def get_name(self):
        return self._name


def init():
    layers = list()
    count = 0
    for i in args['<n>']:
        perceptrons = list()
        for j in range(i):
            perceptrons.append(Perceptron(count,args['--lam']))
            count += 1
        layers.append(perceptrons)
    return layers


def front_propergation(layers,inputss):
    for layer in layers:
        inputs = dict()
        for perceptron in layer:
            perceptron.predict(inputss[-1])
            inputs[perceptron.get_name()] = perceptron.get_predict()
        inputss.append(inputs)
    inputss.pop(-1)


def back_propergation(layers, inputss, gold):
    prev_layer = None
    for layer, inputs in zip(layers[::-1],inputss[::-1]):
        for perceptron in layer:
            if prev_layer in None:
                perceptron.calc_delta(None,lavbel=gold)
            else:
                perceptron.calc_delta(prev_layer)
            perceptron.update_weight(inputs)
        prev_layer = layer


def train(layers):
    inputss = list()
    for line in open(args['--train']):
        spl = line.strip().split()
        gold = spl[0]#正解ラベル

        feats = dict()#一文の単語の出現頻度
        for feat in spl[1:]:
            feats[feat] = feats.get(feat,0) + 1
        inputss.append(feats)
        front_propergation(layers,inputss)
        back_propergation(layers,inputss,float(gold))


def main():
    layers = init()
    for _ in range(args['--epoch']):
        train(layers)
    pickle.dump(layers,open(args['--output'],'w'))


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    args['<n>'] = [int(i) for i in args['<n>'] if i.isdigit()]#隠れ層とノード
    args['--lam'] = float(args['--lam'])#学習率
    args['--epoch'] = int(args['--epoch'])#epoch:iterationと同じ
    main()
