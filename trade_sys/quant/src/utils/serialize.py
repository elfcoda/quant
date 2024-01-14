#!/usr/bin/env python
# encoding: utf-8

import pickle

def dump(li, fileName):
    with open(fileName + '.pkl', 'wb') as file:
        pickle.dump(li, file)

def load(fileName):
    with open(fileName + '.pkl', 'rb') as file:
        li = pickle.load(file)
        return li


