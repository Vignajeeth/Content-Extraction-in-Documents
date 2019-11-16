# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:55:58 2019

@author: vignajeeth
"""

import os
import glob
import pandas as pd
import re
from preprocessing_functions import *
import pickle


def create_dataset(dataset_path):
    count=0
    true_pairs=[]
    reference_paper_sentences={}
    for subdir, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
                temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
                true_pairs.extend(temp)
                
            if subdir.endswith('Reference_XML') and file.endswith('.xml'):
                '''
                Reference Xml random sentences
                '''
                try:
                    xml_to_string(subdir+'/'+file,file,reference_paper_sentences)
                except:
                    count+=1
                    print(file)
    
    citation_text=[]
    reference_text=[]
    random_reference_text=[]
    for i in range(len(true_pairs)):
        if true_pairs[i][1]+'.xml' in reference_paper_sentences:
            citation_text.append(true_pairs[i][2])
            reference_text.append(true_pairs[i][3])
            random_reference_text.append(pick_sentence(true_pairs[i][1]+'.xml',reference_paper_sentences))
    return (citation_text,reference_text,random_reference_text)


def general(dataset_path,name):
    data={}
    data[name+'_citation_text'],data[name+'_reference_text'],data[name+'_random_reference_text']=create_dataset(dataset_path)    
    fp = open(name+"_ANP.pkl","wb")
    pickle.dump(data, fp)

