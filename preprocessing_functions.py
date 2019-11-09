# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:59:25 2019

@author: vignajeeth
"""



import os
import glob
import pandas as pd
import re
import xml.etree.ElementTree as ET
import random


def annotation_file_to_ref_cit_text(file_name):
    dataset=[]
    with open(file_name) as fp:
        lines = fp.readlines()
        for text in lines:
            if len(text)>5:
                text=text.replace("</S>", "")
                text=text.replace("|", "")
                try:
                    citation_text = re.search('Citation Text:(.+?)Reference Offset:', text).group(1)
                except AttributeError:
                    citation_text=''
                try:
                    reference_text = re.search('Reference Text:(.+?)Discourse Facet:', text).group(1)
                except AttributeError:
                    reference_text=''
                try:
                    reference_art = re.search('Reference Article:(.+?)Citing Article:', text).group(1)
                except AttributeError:
                    reference_art=''
                sample=[text[15:18],reference_art,citation_text,reference_text]
                dataset.append(sample)    
    return dataset



def xml_to_string(file_name):
    tree = ET.parse(file_name)
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






















'''

file_name='/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018/X96-1048/Reference_XML/X96-1048.xml'

#def annotation_file_to_ref_cit_text(file_name):
dataset={}
with open(file_name,'rb') as fp:
    lines = fp.readlines()


    for text in lines:


        if len(text)>5:
            text=text.replace("</S>", "")
            text=text.replace("|", "")
            try:
                citation_text = re.search('Citation Text:(.+?)Reference Offset:', text).group(1)
            except AttributeError:
                citation_text=''
            try:
                reference_text = re.search('Reference Text:(.+?)Discourse Facet:', text).group(1)
            except AttributeError:
                reference_text=''
            try:
                reference_art = re.search('Reference Article:(.+?)Citing Article:', text).group(1)
            except AttributeError:
                reference_art=''
            sample=[text[15:18],reference_art,citation_text,reference_text]
            dataset.append(sample)    
#    return dataset




'''










































'''
def annotation_v3_file_to_ref_cit_text(file_name):
    dataset=[]
    with open(file_name) as fp:
        lines = fp.readlines()
        for text in lines:
            if len(text)>5:
                text=text.replace("</S>", "")
                text=text.replace("|", "")
                try:
                    citation_text = re.search('Citation Text:(.+?)Reference Offset:', text).group(1)
                except AttributeError:
                    citation_text=''
                try:
                    reference_text = re.search('Reference Text:(.+?)Discourse Facet:', text).group(1)
                except AttributeError:
                    reference_text=''
                try:
                    reference_art = re.search('Reference Article:(.+?)Citing Article:', text).group(1)
                except AttributeError:
                    reference_art=''
                sample=[text[15:18],reference_art,citation_text,reference_text]
                dataset.append(sample)    
    return dataset
'''


