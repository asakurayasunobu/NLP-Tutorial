#--*--coding:utf-8--*--

from readpercep import *
import sys
model_file = open('model_file')
input_file = open(sys.argv[1],'r')
if __name__ == '__main__':
  w = {}
  for line in model_file:
      name,value = line.strip().split(' ')
      w[name] = int(value)
  for x in input_file:
      phi = create_features(x)
      ydash = predict_one(w,phi)
      print ydash
