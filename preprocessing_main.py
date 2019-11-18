# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:44:25 2019

@author: vignajeeth
"""


from preprocessing import *


human_dataset_path = '/home/vignajeeth/python/Research/IP/Task1/From-Training-Set-2018'
general(human_dataset_path, 'human')


# auto_dataset_path = '/home/vignajeeth/python/Research/IP/Task1/From-ScisummNet-2019'
# general(auto_dataset_path, 'auto')


test_17_path = '/media/vignajeeth/All Files/Dataset/BIRNDL/scisumm-corpus-master/data/Test-Set-2017'
general(test_17_path, 'test_17')


# TODO
# Fix the bugs in the human dataset (9 files that isn't read)
