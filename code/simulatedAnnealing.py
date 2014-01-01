#-*- coding: utf-8 -*-

import formatter
import math
import random
import codecs
import copy
import sys
import jieba as jb
import jieba.posseg as ps

gram_path = '../ngram/normalized_truncate/cityup_%d.txt'
gram_num = 3
file_name = 'in.txt'

# simulated annealing
def sa(s, gram_dict, k_max=100, tem=lambda x: 1.0-x):
    s_now = s
    e_now = energy(s_now, gram_dict)
    k_now = 0
    while k_now < k_max:
        print "k_now = %d, %s" % (k_now, tokens_to_str(s_now))
        s_nxt = get_neighbor(s_now)
        e_nxt = energy(s_nxt, gram_dict)
        if (e_nxt > e_now) or random.random() < math.exp(-(e_now-e_nxt)*1.0/tem(k_now*1.0/k_max)):
            a_now = a_nxt
            e_now = e_nxt
        
        k_now = k_now +1
    return 

# tokens to string
def tokens_to_str(tokens):
    return "".join(map(lambda x:x.word, tokens))
    
# get neighbor
def get_neighbor(_tokens, magic = 0.5):
    tokens = list(_tokens)
    if random.random() < magic:
        # shuffle
        pos1 = random.randint(0, len(tokens)-1)
        pos2 = random.randint(0, len(tokens)-1)
        tmp = lst[pos1]
        lst[pos1] = lst[pos2]
        lst[pos2] = tmp
    else:
        # duplicate
        pos = random.randint(0, len(tokens)-1)
        tokens.insert(pos, tokens[pos])
    return tokens

# fine ngrams
def find_ngrams(lst):
	return zip(*[lst[i:] for i in range(gram_num)])

# calc the energy of current tokens
def energy(tokens, gram_dict):
    lst = find_ngrams(map(lambda x:x.flag, tokens))
    energy_count = 0.0
    for gram in lst:
        energy_count += gram_dict.get(gram, 0)
    return energy_count

# get dictionary from eval the target file
def get_dict():
    fin = open(gram_path % gram_num, 'r')
    return eval(fin.readline().strip())

# sort of preprocessing ...
def solve(inputStr, gram_dict):
    tokens = ps.cut(inputStr)
    print tokens_to_str(tokens)
    after_tokens = sa(tokens, gram_dict)
    return tokens_to_str(after_tokens)

if __name__ == "__main__":
    # input interface
    if len(sys.argv) == 2:
        gram_num = int(sys.argv[1])
    elif len(sys.argv) == 3:
        gram_num = int(sys.argv[1])
        file_name = sys.argv[2]
    # init
    gram_dict = get_dict()
    jb.load_userdict('../data/dict.txt')
    
    # process input
    fin = codecs.open(file_name, 'r', encoding='utf8')
    for line in fin:
        inp = formatter.clean_str(line, u'“”﹝﹞「」”＂『』《》—')
        inp.strip()
        inp = formatter.clean_str(inp)
        print solve(inp, gram_dict)
    fin.close()