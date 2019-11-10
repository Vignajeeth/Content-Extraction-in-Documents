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


human_dataset_path='/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018'
auto_dataset_path='/home/vignajeeth/python/Research/IP/Task1/From-ScisummNet-2019'

human_count=0
human_dataset_true_pairs=[]
human_reference_paper_sentences={}
for subdir, dirs, files in os.walk(human_dataset_path):
    for file in files:
        if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
            temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
            human_dataset_true_pairs.extend(temp)
            
        if subdir.endswith('Reference_XML') and file.endswith('.xml'):
            '''
            Reference Xml random sentences
            '''
            try:
                xml_to_string(subdir+'/'+file,file,human_reference_paper_sentences)
            except:
                human_count+=1
                print(file)


auto_count=0
auto_dataset=[]
auto_reference_paper_sentences={}
for subdir, dirs, files in os.walk(auto_dataset_path):
    for file in files:
        if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
            temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
            auto_dataset.extend(temp)
            
        if subdir.endswith('Reference_XML') and file.endswith('.xml'):
            '''
            Reference Xml random sentences
            '''
            try:
                xml_to_string(subdir+'/'+file,file,auto_reference_paper_sentences)
            except:
                auto_count+=1
                print(file)

#Fix the bugs in the human dataset














