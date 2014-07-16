# coding: utf-8

from functools import wraps
import json
import re

import nltk

TAGGED_WORD_FNS = [nltk.corpus.treebank.tagged_words,
                   nltk.corpus.brown.tagged_words]


def _bad_words():
    """Get the list of bad words."""
    with open('badwords.json') as fp:
        bad_words = json.load(fp)['badwords']
    return bad_words

BAD_WORDS = _bad_words()


def is_bad_word(word, ):
    """Determine if a word is or contains a bad word.

    I don't give a %#@$ about false positives.
    """
    for bad_word in BAD_WORDS:
        if bad_word in word:
            return True
        return False


def is_word(word):
    """Determine if word meets certain wordiness criteria.

    Wordiness criteria:

        * Contains letters and hyphens only.
        * Ends with a letter.

    I know this is going to be a disaster for unicode stuff. It's fine.
    """
    return bool(re.match('^[a-zA-Z-]+[a-zA-Z]$', word))


def clean(fn):
    """Decorator to scrub the set returned by ``fn`` clean of bad words and
    non-words."""
    @wraps(fn)
    def wrapper():
        original_set = fn()
        clean_set = set()

        for word in original_set:
            if is_word(word) and not is_bad_word(word):
                clean_set.add(word)
        return clean_set
    return wrapper


def make_adj_superset():
    """Get a set of all the words tagged as adjectives in TAGGED_WORD_FNS."""
    adj_set = set()
    for tagged_words_fn in TAGGED_WORD_FNS:
        adj_set |= set(word.lower() for word, tag in tagged_words_fn()
                       if tag == 'JJ')
    return adj_set


def make_unadj_set():
    un_set = set()
    for tagged_words_fn in TAGGED_WORD_FNS:
        un_set |= set(word.lower() for word, tag in tagged_words_fn()
                      if tag == 'JJ' and word.lower().startswith('un'))
    return un_set


@clean
def make_adj_set():
    """Get the set of adjectives that appear in the corpora both as <adj> and
    un<adj>.

    This avoids picking up adjectives that don't make since with an un or
    without an un.
    """
    all_adj = make_adj_superset()
    un_adj = make_unadj_set()
    return set(word for word in all_adj if 'un' + word in un_adj)


@clean
def make_noun_set():
    noun_set = set()
    for tagged_words_fn in TAGGED_WORD_FNS:
        noun_set |= set(word.lower() for word, tag in tagged_words_fn()
                        if tag == 'NN')
    return noun_set


def print_set(s):
    for word in sorted(s):
        print word


NOUNS = make_noun_set()
ADJECTIVES = make_adj_set()
