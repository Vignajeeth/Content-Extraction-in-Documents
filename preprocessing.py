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

count=0
human_dataset=[]
for subdir, dirs, files in os.walk(human_dataset_path):
    for file in files:
        if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
            temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
            human_dataset.extend(temp)
            
        if subdir.endswith('Reference_XML') and file.endswith('.xml'):
            '''
            Reference Xml random sentences
            '''
            count+=1



auto_dataset=[]
for subdir, dirs, files in os.walk(auto_dataset_path):
    for file in files:
        if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
            temp=annotation_file_to_ref_cit_text(subdir+'/'+file)
            auto_dataset.extend(temp)
            
        if subdir.endswith('Reference_XML') and file.endswith('.xml'):
            '''
            Reference Xml random sentences
            '''




'''

myfile='/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018/J96-3004/Reference_XML/J96-3004.xml'

import xml.etree.ElementTree as ET
import xmltodict
import json
import re
import random

tree = ET.parse(myfile)
xml_data = tree.getroot()
xmlstr = ET.tostring(xml_data, encoding='unicode', method='xml')


#Removing Tags
xmlstr=re.sub(r'<(.+?)>','',xmlstr)
#Removing tabs
xmlstr=re.sub(r'\t','',xmlstr)
#Removing strings with less than 30 characters
xmlstr=re.sub(r'\n.{1,50}\n', '', xmlstr)
#Removing double lines
xmlstr=re.sub(r'\n\n',r'\n',xmlstr)
xmlstr=re.sub(r'\n\n',r'\n',xmlstr)

document=xmlstr.split('\n')
return (random.sample(document,4))


#
#for i in range(len(document)):
#    try:    
#        document[i] = document[i].replace('<(.+?)>',"")
#    except:
#        continue


#TODO
#Remove all whitespaces
#Each line must end with a period and should be a separate entry in the list



data_dict = dict(xmltodict.parse(xmlstr))
'''