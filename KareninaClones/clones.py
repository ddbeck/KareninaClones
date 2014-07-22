# -*- coding: utf-8 -*-

import os
import random

from textblob import Word

# Basic grammar:

#     <plural_noun>           ::= a word from the list of plural nouns
#                                 (e.g., families, coporations, bands, etc.)
#     <negative_prefix>       ::= "un"
#     <adjective>             ::= "happy" | "satisifed" | "deserving" | …
#     <clone>                 ::= <adjective> <plural_noun> "are all alike;"
#                                 "every" <negative_prefix><adjective>
#                                 <plural_noun> "is"
#                                 <negative_prefix><adjective>
#                                 "in its own way."

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def data(fpath):
    with open(os.path.join(ROOT_DIR, fpath)) as fp:
        lines = fp.readlines()
    return [line.rstrip('\n') for line in lines]


def karenina_clone(nouns=None, adjectives=None):
    """Generate a Karenina Principle snowclone from a list of nouns and
    adjectives.
    """
    nouns = DEFAULT_NOUNS if nouns is None else nouns
    adjectives = DEFAULT_ADJECTIVES if adjectives is None else adjectives

    noun = random.choice(nouns)
    plural_noun = Word(noun).pluralize()
    adjective = random.choice(adjectives)

    return SNOWCLONE_FMT.format(adjective=adjective, plural_noun=plural_noun,
                                singular_noun=noun).capitalize()

SNOWCLONE_FMT = ("{adjective} {plural_noun} are all alike; "
                 "every un{adjective} {singular_noun} is un{adjective} "
                 "in its own way.")

TEST_ADJECTIVES = ['affected', 'deserving', 'flawed', 'happy', 'satisifed']
TEST_NOUNS = ['bot', 'duck', 'family', 'hydrophone', 'stopwatch', 'wolf']

DEFAULT_ADJECTIVES = data('data/adjectives.txt')
DEFAULT_NOUNS = data('data/nouns.txt')
