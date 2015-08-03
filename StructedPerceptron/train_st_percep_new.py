#!usr/bin/python
#coding:utf-8




def main():
    iter_ = 1
    input_file = open('wiki~~~~~')
    weight_dict = defaultdict(float)
    possible_labels = set()
    for line in input_file:
        for word in input_file.stip().split():
            possible_labels.add(word.split('_')[1])
    for i in range(iter_):
        print 'iteration:',i+1
        for line in input_file:
            words = [word.]



if __name__ == '__main__':
    main()
