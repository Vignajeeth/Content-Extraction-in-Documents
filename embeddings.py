# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:07:48 2019

@author: vignajeeth
"""


from sentence_transformers import SentenceTransformer
import pickle


def encoding_text_to_float(name):
    fp = open(name + "_ANP.pkl", "rb")
    data_ANP = pickle.load(fp)

    embedder = SentenceTransformer('bert-base-nli-max-tokens')

    embeddings_ANP = {}

    embeddings_ANP[name + "_citation_embeddings"] = embedder.encode(data_ANP[name + "_citation_text"])
    embeddings_ANP[name + "_reference_embeddings"] = embedder.encode(data_ANP[name + "_reference_text"])
    embeddings_ANP[name + "_random_reference_embeddings"] = embedder.encode(data_ANP[name + "_random_reference_text"])

    # To dump it into pickle if need be

    fp = open(name + "_embeddings_ANP.pkl", "wb")
    pickle.dump(embeddings_ANP, fp)


name = 'human'
encoding_text_to_float(name)
