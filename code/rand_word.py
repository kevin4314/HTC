# -*- coding: utf-8 -*-

import random

import synonym_freq
import word_freq
import synonyms

_dick, _invdick = None, None
_loaded_freq_dick = {}

def sub(tokens, author):
    """Returns a list of tuples"""

    if _dick is None:
        _dick, _invdick = synonyms.read_wordbank('../data/wordbank.txt')

    if author not in _loaded_freq_dick:
        _loaded_freq_dick[author] = word_freq.load_file('../wordfreq/%s/1.txt' % (author)) # tmp
    freq_dick = _loaded_freq_dick[author]

    def subsub(word):
        candidates = synonym_freq.query(word, _dick, _invdick, freq_dick)
        d = random.random()

        acc = 0.
        for c, w in candidates:
            acc += w
            if acc > d:
                return c

        raise Exception('')

    return [subsub(word) for word, _ in tokens]
