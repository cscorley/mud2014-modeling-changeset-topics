#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [The "New BSD" license]
# Copyright (c) 2014 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

if __name__ == '__main__':
    import nose
    nose.main()

import unittest
import os.path
import string
import random
from io import StringIO

from nose.tools import *

from src.preprocessing import split, remove_stops

# datapath is now a useful function for building paths to test files
module_path = os.path.dirname(__file__)
datapath = lambda fname: os.path.join(module_path, u'test_data', fname)

class PreprocessTests(unittest.TestCase):
    def test_split(self):
        """Split tokens into terms using the following rules:

            0. All digits are discarded
            1. A sequence beginning with an lc letter must be followed by lc letters
            2. A sequence beginning with an uc letter can be followed by either:
                a. One or more uc letters
                b. One or more lc letters

        """
        cases = dict({
            'camelCase': ('camel', 'Case'),
            'CamelCase': ('Camel', 'Case'),
            'camel2case': ('camel', '2', 'case'),
            'camel2Case': ('camel', '2', 'Case'),
            'word': ('word', ),
            'HTML': ('HTML', ),
            'readXML': ('read', 'XML'),
            'XMLRead': ('XML', 'Read'),
            'firstMIDDLELast': ('first', 'MIDDLE', 'Last'),
            'CFile': ('C', 'File'),
            'Word2Word34': ('Word', '2', 'Word', '34'),
            'WORD123Word': ('WORD', '123', 'Word'),
            'c_amelCase': ('c', '_', 'amel', 'Case'),
            'CamelC_ase': ('Camel', 'C', '_', 'ase'),
            'camel2_case': ('camel', '2', '_', 'case'),
            'camel_2Case': ('camel', '_', '2', 'Case'),
            'word': ('word', ),
            'HTML': ('HTML', ),
            'read_XML': ('read', '_', 'XML'),
            'XML_Read': ('XML', '_', 'Read'),
            'firstM_IDDL_ELast': ('first', 'M', '_', 'IDDL', '_', 'E', 'Last'),
            'the_CFile': ('the', '_', 'C', 'File'),
            'Word_2_Word3_4': ('Word', '_', '2', '_', 'Word', '3', '_', '4'),
            'WO_RD123W_or_d': ('WO', '_', 'RD', '123', 'W', '_', 'or', '_', 'd'),
            'hypen-ation': ('hypen', '-', 'ation'),
            'email@address.com': ('email', '@', 'address', '.', 'com'),
            '/*comment*/': ('/', '*', 'comment', '*', '/'),
            'word1': ('word', '1'),
            'Word1': ('Word', '1'),
            'f1': ('f', '1'),
            '1ms': ('1', 'ms'),
            'F1': ('F', '1'),
            'WORD_THING': ('WORD', '_', 'THING'),
            '@': ('@',),
            'WORD_THING_ONE': ('WORD', '_', 'THING', '_', 'ONE'),
            'wordThing_one': ('word', 'Thing', '_', 'one'),
            '_w': ('_', 'w'),
            '_wt': ('_', 'wt'),
            '_wT': ('_', 'w', 'T'),
            '_WT': ('_', 'WT'),
            '_Wt': ('_', 'Wt'),
            'wt_': ('wt', '_'),
            '<5>': ('<', '5', '>'),
            '==': ('=', '='),
            'x=5;': ('x', '=', '5', ';'),
            '2.0': ('2', '.', '0'),
            '2,0': ('2', ',', '0'),
            '//test': ('/', '/', 'test'),
            'Boolean.FALSE': ('Boolean', '.', 'FALSE'),
            'word': ('word', ),
            'word.': ('word', '.'),
            '.word.': ('.', 'word', '.'),
            '.word': ('.', 'word'),
            'WordThing.': ('Word', 'Thing', '.'),
            'WordThing.FLAG': ('Word', 'Thing', '.', 'FLAG'),
            'WordThing.cmd': ('Word', 'Thing', '.', 'cmd'),
            'WordThing.cmdDo': ('Word', 'Thing', '.', 'cmd', 'Do'),
            'System.out.println': ('System', '.', 'out', '.', 'println'),
            'System.out.println();': ('System', '.', 'out', '.', 'println', '(', ')', ';'),
            'x++': ('x', '+', '+'),
            '++x': ('+', '+', 'x'),
            "n't": ('n', "'", 't'),
            u"test💩word": ('test', u'💩', 'word'),
            u'Erwin_Schrödinger': ('Erwin', '_', u'Schrödinger')
            })

        for term, expected in cases.items():
            result = split([term])
            self.assertEqual(tuple(result), expected)

        terms = cases.keys()
        expected = sum(list(map(list, cases.values())), [])
        result = split(terms)
        self.assertEqual(list(result), expected)

    def test_split_random_punct(self):
        for i in range(1, 100):
            r = random.randint(1, i)
            word = u''
            for j in range(1, r):
                p = random.randint(0, len(string.punctuation) - 1)
                word += string.punctuation[p]

            result = split([word])
            self.assertEqual(list(result), list(word))

    def test_split_creates_generator(self):
        """ Split tokens creates a generator """
        result = split('butts')
        self.assertIsInstance(result, type(x for x in list()))

    def test_stops(self):
        inputs = ['test', 'the', '123']
        inputs.extend(string.punctuation)
        expected = ['test']
        stops = ['the']
        result = remove_stops(inputs, stops)
        self.assertEqual(list(result), expected)

    def test_stops_creates_generator(self):
        """ Remove stops creates a generator """
        inputs = ['test', 'the']
        expected = ['test']
        stops = ['the']
        result = remove_stops(inputs, stops)
        self.assertIsInstance(result, type(x for x in list()))
