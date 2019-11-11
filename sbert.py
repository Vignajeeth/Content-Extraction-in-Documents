# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:07:48 2019

@author: vignajeeth
"""

import pickle
import sentence_transformers


fp = open("human_true_pairs.pkl","rb")
human_true_pairs = pickle.load(fp)

fp = open("human_sentences.pkl","rb")
human_sentences = pickle.load(fp)

fp = open("auto_true_pairs.pkl","rb")
auto_true_pairs = pickle.load(fp)

fp = open("auto_sentences.pkl","rb")
auto_sentences = pickle.load(fp)



model = SentenceTransformer('bert-base-nli-mean-tokens')






