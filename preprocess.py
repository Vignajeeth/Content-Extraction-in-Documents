# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:42:11 2019

@author: vignajeeth
"""

import os
import pickle
import re
import xml.etree.ElementTree as ET
import random

#---------------------------------Lvl 3---------------------------------------


def annotation_file_to_ref_cit_text(file_name):
    dataset = []
    with open(file_name) as fp:
        lines = fp.readlines()
        for text in lines:
            if len(text) > 5:
                text = text.replace("</S>", "")
                text = text.replace("|", "")
                try:
                    citation_text = re.search('Citation Text:(.+?)Reference Offset:', text).group(1)
                except AttributeError:
                    citation_text = ''
                citation_text = re.sub(r'<(.+?)>', '', citation_text)
                try:
                    reference_text = re.search('Reference Text:(.+?)Discourse Facet:', text).group(1)
                except AttributeError:
                    reference_text = ''
                reference_text = re.sub(r'<(.+?)>', '', reference_text)
                try:
                    reference_art = re.search('Reference Article:(.+?)Citing Article:', text).group(1)
                    reference_art = re.search('[A-Z]\d{2}-\d{4}', reference_art).group(0)
                except AttributeError:
                    reference_art = ''
                sample = [text[15:18].strip(), reference_art.strip(), citation_text.strip(), reference_text.strip()]
                if not (len(sample[2]) < 5 or len(sample[3]) < 5):
                    dataset.append(sample)
    return dataset


def xml_to_string(file_path, file_name, reference_paper_sentences):
    tree = ET.parse(file_path)
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='unicode', method='xml')
    # Removing Tags
    xmlstr = re.sub(r'<(.+?)>', '', xmlstr)
    # Removing tabs
    xmlstr = re.sub(r'\t', '', xmlstr)
    # Removing strings with less than 50 characters
    xmlstr = re.sub(r'\n.{1,50}\n', '', xmlstr)
    # Removing double lines
    xmlstr = re.sub(r'\n\n', r'\n', xmlstr)
    xmlstr = re.sub(r'\n\n', r'\n', xmlstr)
    document = xmlstr.split('\n')
    reference_paper_sentences[file_name] = document


def pick_sentence(file_name, reference_paper_sentences):
    '''
    temp=random.choice(reference_paper_sentences[file_name])
    if len(temp)>100:
        return temp
    temp=pick_sentence(file_name,reference_paper_sentences)
    return temp
    '''
    temp, i = '', 0
    while (len(temp) < 100) and (i < 50):
        temp = random.choice(reference_paper_sentences[file_name])
        i += 1
    return temp


#-----------------------------------------------------------------------------


#------------------------------Lvl 2------------------------------------------

def create_dataset(dataset_path):
    count = 0
    true_pairs = []
    reference_paper_sentences = {}
    for subdir, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.ann.txt') or file.endswith('.annv3.txt'):
                temp = annotation_file_to_ref_cit_text(subdir + '/' + file)
                true_pairs.extend(temp)

            if subdir.endswith('Reference_XML') and file.endswith('.xml'):
                '''
                Reference Xml random sentences
                '''
                try:
                    xml_to_string(subdir + '/' + file, file, reference_paper_sentences)
                except:
                    count += 1
                    print(file)

    citation_text = []
    reference_text = []
    random_reference_text = []
    for i in range(len(true_pairs)):
        if true_pairs[i][1] + '.xml' in reference_paper_sentences:
            citation_text.append(true_pairs[i][2])
            reference_text.append(true_pairs[i][3])
            random_reference_text.append(pick_sentence(true_pairs[i][1] + '.xml', reference_paper_sentences))
    return (citation_text, reference_text, random_reference_text)


def pickling_function(dataset_path, name):
    data = {}
    data[name + '_citation_text'], data[name + '_reference_text'], data[name + '_random_reference_text'] = create_dataset(dataset_path)
    try:
        os.mkdir('Pickles')
    except FileExistsError:
        pass
    os.chdir('Pickles')
    fp = open(name + "_ANP.pkl", "wb")
    pickle.dump(data, fp)
    os.chdir('..')


#-----------------------------------------------------------------------------


if __name__ == "__main__":
    '''
    Uncomment the dataset you need to parse
    '''
#    human_dataset_path = '/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018'
#    pickling_function(human_dataset_path, 'human')
#
#
#    auto_dataset_path = '/home/vignajeeth/python/Research/IP/Task1/From-ScisummNet-2019'
#    pickling_function(auto_dataset_path, 'auto')
#
#
    test_17_path = '/media/vignajeeth/All Files/Dataset/BIRNDL/scisumm-corpus-master/data/Test-Set-2017'
    pickling_function(test_17_path, 'test_17')
#
#
#    test_16_path = '/media/vignajeeth/All Files/Dataset/BIRNDL/scisumm-corpus-master/data/Test-Set-2016'
#    pickling_function(test_16_path, 'test_16')

else:
    '''
    Stuff to add when called from a different main
    '''
    pass

# TODO
# Fix the bugs in the human dataset (9 files that isn't read)
