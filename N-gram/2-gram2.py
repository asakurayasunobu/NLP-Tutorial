#!usr/bin/python
#--*--coding:utf-8--*--
import sys
import math
from collections import defaultdict
if __name__ =="__main__":
  modelfile = open(sys.argv[1],"r")
  test_file = open(sys.argv[2],"r")
  lambda1 = 0.95
  lambda2 = 0.95
  V = 1000000
  W = 0
  H = 0
  mydict = defaultdict(lambda:0)
  for line in modelfile:
      probs = line.strip().split("\t")
      # print probs
      mydict[probs[0]] = float(probs[1])
  for line in test_file:
      array = line.strip().split(" ")
      array.append("</s>")
      array.insert(0,"<s>")
      for index in range(1,len(array)-1):
          P1 = lambda1*mydict[array[index]]+(1-lambda1)/V
          P2 = lambda2*mydict[" ".join(array[index-1:index+1])]+(1-lambda2)*P1
          H += -math.log(P2,2)
          W += 1
  print "entrapy=%s"%(H/W)
