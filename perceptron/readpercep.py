#usr/bin/python
#--*--coding:utf-8--*--
import sys
from collections import defaultdict

def create_features(x):#辞書に１行の文を単語に分割し頻度を数える
  phi = defaultdict(lambda:0)
  words = []
  words = x.strip().split(' ')
  for word in words:
    phi['UNI:'+word] += 1
  return phi

def predict_one(w,phi):#辞書と単語の重み辞書を受け取って、
  score = 0
  for name,value in phi.items():
    if name in w:
      score += value * w[name]
  if score >= 0:
    return 1
  else:
    return -1

def update_weight(w,phi,y):
  for name,value in phi.items():
    w[name] += value * y #

if __name__ == '__main__':
   inputfile = open('../../data/titles-en-train.labeled','r')
   w = defaultdict(lambda:0)
   for iter_ in range(5):
       for line in inputfile:  #入力ファイル
         value,key = line.strip().split('\t')
         y = int(value)
         x = key
         phi = create_features(x) #一文の単語の頻度のdict
         ydash = predict_one(w,phi)
         if ydash != y:
           update_weight(w,phi,y)
   for key,value in sorted(w.items(),key = lambda x:x[1]):
     print key,value
