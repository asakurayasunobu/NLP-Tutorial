#!/usr/bin/python
# --*--coding:utf-8--*--
import math
import sys
from collections import defaultdict
my_file = open(sys.argv[1],"r")
my_file2 = open(sys.argv[2],"r")
my_dict = {}


count=0
ramuda=0.95
v=1000000
h=0
unk=0

for line in my_file:#辞書を入力
  array=line.strip().split(" ") 
  my_dict[array[0]] = float(array[1])   

lista=[]
for line2 in my_file2:
  lista=line2.strip().split(" ")
  lista.append("</s>")
  for word in lista:
    count+=1
    print count
    p=(1-ramuda)/v
    if word in my_dict:
      p+=ramuda*my_dict[word]
    else:
      unk += 1
    h += -math.log(p,2)

print count
print unk
print lista
print  h/count
print (count-unk)/float(count)
