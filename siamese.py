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
import os


def reshaper(matrix):
    '''
    Alternative to np.reshape
    '''
    dim = matrix.shape[0]
    h = matrix.shape[1]
    w = matrix.shape[2]
    ans = np.ones((h, dim, w))
    for i in range(h):
        for j in range(dim):
            ans[i][j] = matrix[j][i]
    return (ans)


def data_processing_for_siamese(name):
    os.chdir('Pickles')
    fp = open(name + "_embeddings_ANP.pkl", "rb")
    embeddings_ANP = pickle.load(fp)
    os.chdir('..')

    embeddings_ANP[name + '_citation_embeddings'] = np.asarray(embeddings_ANP[name + '_citation_embeddings'])
    embeddings_ANP[name + '_reference_embeddings'] = np.asarray(embeddings_ANP[name + '_reference_embeddings'])
    embeddings_ANP[name + '_random_reference_embeddings'] = np.asarray(embeddings_ANP[name + '_random_reference_embeddings'])

    h, w = embeddings_ANP[name + '_citation_embeddings'].shape[0], embeddings_ANP[name + '_citation_embeddings'].shape[1]

    true_pairs = np.asarray([embeddings_ANP[name + '_citation_embeddings'], embeddings_ANP[name + '_reference_embeddings']])
    false_pairs = np.asarray([embeddings_ANP[name + '_citation_embeddings'], embeddings_ANP[name + '_random_reference_embeddings']])

    data11 = np.concatenate((true_pairs, false_pairs), axis=1)
    targets = np.concatenate((np.zeros((h)), np.ones((h)))).reshape((2 * h, 1))
    data11 = reshaper(data11)

    return (data11, targets)

# --------------------------Siamese Model Training-----------------------------


def model_definition():
    left_input = Input((w,))
    right_input = Input((w,))

    densenet = Sequential([
        Dense(400, activation='relu', input_shape=(w,)),
        # Dense(100, activation='relu'),
        Dense(75, activation='relu'),
        # Dense(35, activation='relu'),
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
name = 'human'
data11, targets = data_processing_for_siamese(name)

#data11, targets = shuffle(data11, targets)


w = data11.shape[2]
# Training of the model
siamese_net = model_definition()
siamese_net.fit([data11[:, 0], data11[:, 1]], targets, epochs=15)

# Testing
test_data11, test_targets = data_processing_for_siamese('test_17')
siamese_net.evaluate([test_data11[:, 0], test_data11[:, 1]], test_targets)


#------------------------------------------------------------------


'''

# Check zeros
# Check indexes
# Run on other datasets



from scipy.spatial import distance
import matplotlib.pyplot as plt


l2=np.ones((1328))*5
cos=np.ones((1328))*5
corr=np.ones((1328))*5

for i in range(1328):
    l2[i] = distance.euclidean(data11[i][0], data11[i][1])
    cos[i] = distance.cosine(data11[i][0], data11[i][1])
    corr[i] = distance.correlation(data11[i][0], data11[i][1])
#    l2[i+664] = distance.euclidean(false_pairs[0][i], false_pairs[1][i])
#    cos[i+664] = distance.cosine(false_pairs[0][i], false_pairs[1][i])
#    corr[i+664] = distance.correlation(false_pairs[0][i], false_pairs[1][i])


#for i in range(664):
#    l2[i] = distance.euclidean(distance.euclidean(true_pairs[1][i], false_pairs[0][i]),distance.euclidean(true_pairs[1][i], true_pairs[0][i]))
#    cos[i] = distance.cosine(true_pairs[1][i], false_pairs[0][i])
#    corr[i] = distance.correlation(true_pairs[1][i], false_pairs[0][i])




plt.plot(l2/max(l2),label='Euclidean Distance')
plt.plot(cos,label='Cosine Distance')

plt.plot(corr,label='Correlation')
plt.plot(targets,label='True values')


'''
