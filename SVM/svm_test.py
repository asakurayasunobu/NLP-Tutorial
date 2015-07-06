#!usr/bin/python
#coding:utf-8

from svm import *
from collections import defaultdict
import math
def main():
    model_file = open('svm_model_file')
    input_file = open('../../data/titles-en-test.word')
    w = defaultdict(lambda:0)
    for line in model_file:
        name, weight = line.strip().split()
        w[name] = float(weight)

    for line in input_file:
        phi = create_features(line)
        print int(math.copysign(1,predict_one(w,phi)))



if __name__ == '__main__':
    main()
