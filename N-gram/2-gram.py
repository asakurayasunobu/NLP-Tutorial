#usr/bin/python
#--*--coding:utf-8--*--
import sys
from collections import defaultdict
if __name__ == "__main__":
  counts = defaultdict(lambda: 0)
  context_count = defaultdict(lambda: 0)
  trainfile = open(sys.argv[1],"r")
  for line in trainfile:
      array = line.strip().split(" ")
      array.append("</s>")              #読み込んだ１行に<s>と</s>を追加
      array.insert(0,"<s>")
      for index in (range(1,len(array)-1)): #1行に含まれる単語の数だけ繰り返す
          counts[array[index-1]+" "+array[index]] += 1 #2-gramをcountsに追加
          context_count[array[index-1]] += 1 #1-gramをcontext_countに追加
          counts[array[index]] +=1#1-gramをcountsに追加
          context_count[""] +=1  #全単語を数える
  modelfile = open("2-grammodel.txt","w")#書き込みファイルの作成
  for ngram,count in counts.items():#counts辞書で回す
      array = ngram.split(" ")#countsに入っていた各1-gram,2-gramをリストarrayに入れる
      array.pop()#arrayに入った単語リスト（1-gramか2-gram)の最後尾を取り除く
      context="".join(array)#リストarrayを文字列にし、contextに代入
      probability = float(counts[ngram])/context_count[context]#<s> I am a student </s>
      modelfile.write( "%s\t%f\n"%(ngram,probability))
  modelfile.close()#fileを閉じてまた開くとき、seek?を使う 
