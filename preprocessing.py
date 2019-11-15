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

human_dataset_path='/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018'
auto_dataset_path='/home/vignajeeth/python/Research/IP/Task1/From-ScisummNet-2019'


def create_human_dataset():    
    human_count=0
    human_true_pairs=[]
    human_reference_paper_sentences={}
    for subdir, dirs, files in os.walk(human_dataset_path):
        for file in files:
            if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
                temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
                human_true_pairs.extend(temp)
                
            if subdir.endswith('Reference_XML') and file.endswith('.xml'):
                '''
                Reference Xml random sentences
                '''
                try:
                    xml_to_string(subdir+'/'+file,file,human_reference_paper_sentences)
                except:
                    human_count+=1
    #                print(file)
    
    
    human_citation_text=[]
    human_reference_text=[]
    human_random_reference_text=[]
    for i in range(len(human_true_pairs)):
        if human_true_pairs[i][1]+'.xml' in human_reference_paper_sentences:
            human_citation_text.append(human_true_pairs[i][2])
            human_reference_text.append(human_true_pairs[i][3])
            human_random_reference_text.append(pick_sentence(human_true_pairs[i][1]+'.xml',human_reference_paper_sentences))
    return (human_citation_text,human_reference_text,human_random_reference_text)




def create_auto_dataset():
    auto_count=0
    auto_true_pairs=[]
    auto_reference_paper_sentences={}
    for subdir, dirs, files in os.walk(auto_dataset_path):
        for file in files:
            if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
                temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
                auto_true_pairs.extend(temp)
                
            if subdir.endswith('Reference_XML') and file.endswith('.xml'):
                '''
                Reference Xml random sentences
                '''
                try:
                    xml_to_string(subdir+'/'+file,file,auto_reference_paper_sentences)
                except:
                    auto_count+=1
                    print(file)
    
    auto_citation_text=[]
    auto_reference_text=[]
    auto_random_reference_text=[]
    for i in range(len(auto_true_pairs)):
        if auto_true_pairs[i][1]+'.xml' in auto_reference_paper_sentences:
            auto_citation_text.append(auto_true_pairs[i][2])
            auto_reference_text.append(auto_true_pairs[i][3])
            auto_random_reference_text.append(pick_sentence(auto_true_pairs[i][1]+'.xml',auto_reference_paper_sentences))
    return (auto_citation_text,auto_reference_text,auto_random_reference_text)



#
#def return_human(human_citation_text,human_reference_text,human_random_reference_text):
#    return (human_citation_text,human_reference_text,human_random_reference_text)
#
#def return_auto(auto_citation_text,auto_reference_text,auto_random_reference_text):
#    return (auto_citation_text,auto_reference_text,auto_random_reference_text)
#



'''
#To dump it into pickle if need be
#
#fp = open("auto_citation_text.pkl","wb")
#pickle.dump(auto_citation_text, fp)
#
#fp = open("auto_reference_text.pkl","wb")
#pickle.dump(auto_reference_text, fp)
#
#fp = open("auto_random_reference_text.pkl","wb")
#pickle.dump(auto_random_reference_text, fp)
##
'''




human_citation_text,human_reference_text,human_random_reference_text=create_human_dataset()
#auto_citation_text,auto_reference_text,auto_random_reference_text=create_auto_dataset()



#To dump it into pickle if need be

fp = open("human_citation_text.pkl","wb")
pickle.dump(human_citation_text, fp)

fp = open("human_reference_text.pkl","wb")
pickle.dump(human_reference_text, fp)

fp = open("human_random_reference_text.pkl","wb")
pickle.dump(human_random_reference_text, fp)






































#Fix the bugs in the human dataset
#USe the lists to generate sentence embeddings and then pass to siamese


'''
import pickle


fp = open("human_true_pairs.pkl","wb")
pickle.dump(human_true_pairs, fp)

fp = open("human_sentences.pkl","wb")
pickle.dump(human_reference_paper_sentences, fp)

fp = open("auto_true_pairs.pkl","wb")
pickle.dump(auto_dataset, fp)

fp = open("auto_sentences.pkl","wb")
pickle.dump(auto_reference_paper_sentences, fp)

'''







