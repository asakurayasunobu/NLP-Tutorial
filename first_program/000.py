#!/user/bin/python

from collections import defaultdict
import string
import sys
my_dict = defaultdict(lambda:0)
my_file = open(sys.argv[1],"r")
count = 0
for line in my_file:
  line=line.strip()
  array=line.split(" ")
  array.insert(0,"<s>")
  array.append("</s>")
  for i in array:
    my_dict[i]+=1
    count +=1
for key,value in my_dict.items():
  print key, float(value)/count



