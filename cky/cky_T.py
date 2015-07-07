#!usr/bin/python


from collections import defaultdict
import math
import sys


def load_grammer(gram_file_name):
    for rule in open(gram_file_name):
        lhs, rhs, prob = rule.strip().split("\t")
        rhs_symbols = rhs.split()
        prob = math.log(float(prob) )
        # if pre-terminal symbol
        if len(rhs_symbols) == 1:
            # P(lhs -> rhs) = prob
            preterm[rhs].append((lhs, prob))
        # if non-terminal symbol
        else:
            # P(lhs -> (rhs1, rhs2)) = prob
            nonterm.append((lhs, rhs_symbols[0], rhs_symbols[1], prob) )


def add_pre_terminal_symbol(words):
    for i in range(len(words) ):
        for lhs, log_prob in preterm[words[i]]:
            best_score[lhs + str((i, i + 1) ) ] = float(log_prob)


def culc_score(i_k, k_j, i_j):
    for sym, lsym, rsym, log_prob in nonterm:
        left_sym = lsym + i_k
        right_sym = rsym + k_j
        #print right_sym, left_sym
        #print best_score.keys()
        symbol = sym + i_j
        if left_sym in best_score and right_sym in best_score:
            my_lp = best_score[left_sym] + best_score[right_sym] + log_prob
            if not symbol in best_score or my_lp < best_score[symbol]:
                best_score[symbol] = my_lp
                best_edge[symbol] = (left_sym, right_sym)
            

def internal_step(words):
    # right span
    for j in range(2, len(words) + 1):
        # left span
        for i in range(j - 2, -1, -1):
             # start poingt of rsym
             for k in range(i + 1, j):
                 # left span _ rsym start, rsym start _ right span 
                 i_k = str((i, k) ) 
                 k_j = str((k, j) )
                 i_j = str((i, j) )
                 culc_score(i_k, k_j, i_j)


def print_tree(symbol, words):
    sym = symbol.split("(")[-2]
    i = int(symbol.split("(")[-1].split(",")[0])
    # nonterminal symbol
    if symbol in best_edge:
       next_edge = best_edge[symbol]
       return "(" + sym + " " + \
           print_tree(next_edge[0], words) + " " + \
           print_tree(next_edge[1], words) + ")"
    # terminal_symbol
    else:
        return "(" + sym + " " + words[i] + ")"


def cky(gram_file_name, input_file_name):
    load_grammer(gram_file_name)
    for line in open(input_file_name):
        words = line.strip().split()
        add_pre_terminal_symbol(words)
        internal_step(words)
        print print_tree('S(0, ' + str(len(words) ) + ')', words)

if __name__ == "__main__":
    # pre-terminal_symbol
    preterm = defaultdict(list)

    # nonterminal_symbol
    nonterm = list()

    # key = sym, value = max_log_prob
    best_edge = defaultdict(tuple)

    # key = sym, value = (lsym, rsym)
    best_score = defaultdict(float)

    gram_file_name = sys.argv[1]
    input_file_name = sys.argv[2]

    cky(gram_file_name, input_file_name)


