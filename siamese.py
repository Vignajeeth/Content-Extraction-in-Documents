# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:10:28 2019

@author: vignajeeth
"""


from keras.layers import Input, Lambda, Dense
from keras.models import Model, Sequential
# from keras.regularizers import l2
from keras import backend as K
from keras.optimizers import Adam
import pickle
import numpy as np
from sklearn.utils import shuffle


def data_processing_for_siamese(name):
    fp = open(name + "_embeddings_ANP.pkl", "rb")
    embeddings_ANP = pickle.load(fp)

    embeddings_ANP[name + '_citation_embeddings'] = np.asarray(embeddings_ANP[name + '_citation_embeddings'])
    embeddings_ANP[name + '_reference_embeddings'] = np.asarray(embeddings_ANP[name + '_reference_embeddings'])
    embeddings_ANP[name + '_random_reference_embeddings'] = np.asarray(embeddings_ANP[name + '_random_reference_embeddings'])

    # human_citation_embeddings=np.asarray(human_citation_embeddings)#.reshape(len(human_citation_embeddings),1,len(human_citation_embeddings[0]))
    # human_reference_embeddings=np.asarray(human_reference_embeddings)#.reshape(len(human_reference_embeddings),1,len(human_reference_embeddings[0]))
    # human_random_reference_embeddings=np.asarray(human_random_reference_embeddings)#.reshape(len(human_random_reference_embeddings),1,len(human_random_reference_embeddings[0]))

    h, w = embeddings_ANP[name + '_citation_embeddings'].shape[0], embeddings_ANP[name + '_citation_embeddings'].shape[1]

    targets = [np.zeros((h)), np.ones((h))]
    #
    # true_pairs=np.concatenate((human_citation_embeddings,human_reference_embeddings),axis=1)
    # false_pairs=np.concatenate((human_citation_embeddings,human_random_reference_embeddings),axis=1)

    # dataset_1_to_1=np.concatenate((true_pairs,false_pairs),axis=)

    true_pairs = np.asarray([embeddings_ANP[name + '_citation_embeddings'], embeddings_ANP[name + '_reference_embeddings']])
    false_pairs = np.asarray([embeddings_ANP[name + '_citation_embeddings'], embeddings_ANP[name + '_random_reference_embeddings']])

    dataset_1to1 = np.concatenate((true_pairs, false_pairs), axis=1).reshape(2 * h, 2, w)
    targets = np.concatenate((np.zeros((h)), np.ones((h)))).reshape((2 * h, 1))

    dataset_1to1, targets = shuffle(dataset_1to1, targets)
    dataset_1to1 = dataset_1to1.reshape((2, 2 * h, w))
    return (dataset_1to1, targets)

# --------------------------Siamese Model Training-----------------------------


def model_definition():
    left_input = Input((w,))
    right_input = Input((w,))

    densenet = Sequential([
        Dense(400, activation='relu', input_shape=(w,)),
        Dense(100, activation='relu'),
        Dense(75, activation='relu'),
        Dense(35, activation='relu'),
    ])

    encoded_l = densenet(left_input)
    encoded_r = densenet(right_input)

    L1_layer = Lambda(lambda tensor: K.abs(tensor[0] - tensor[1]))

    L1_distance = L1_layer([encoded_l, encoded_r])

    prediction = Dense(1, activation='sigmoid')(L1_distance)
    siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)
    siamese_net.compile(loss="binary_crossentropy", optimizer='Nadam', metrics=['accuracy'])
    return (siamese_net)


# Training Data
name = input("Enter the name of the data : ")
dataset_1to1, targets = data_processing_for_siamese('human')
w = dataset_1to1.shape[2]

# Training of the model
siamese_net = model_definition()
siamese_net.fit([dataset_1to1[0], dataset_1to1[1]], targets, epochs=5)

# Testing
test_dataset_1to1, test_targets = data_processing_for_siamese('test_17')
siamese_net.evaluate([test_dataset_1to1[0], test_dataset_1to1[1]], test_targets)
