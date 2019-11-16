# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:07:48 2019

@author: vignajeeth
"""


from sentence_transformers import SentenceTransformer
import pickle

def encoding_text_to_float(name):
    fp = open(name+"_ANP.pkl","rb")
    data_ANP=pickle.load(fp)
    
    embedder = SentenceTransformer('bert-base-nli-max-tokens')
    
    embeddings_ANP={}
    
    embeddings_ANP[name+"_citation_embeddings"]=embedder.encode(data_ANP[name+"_citation_text"])
    embeddings_ANP[name+"_reference_embeddings"]=embedder.encode(data_ANP[name+"_reference_text"])
    embeddings_ANP[name+"_random_reference_embeddings"]=embedder.encode(data_ANP[name+"_random_reference_text"])
    
    #To dump it into pickle if need be
    
    fp=open(name+"_embeddings_ANP.pkl","wb")
    pickle.dump(embeddings_ANP,fp)



name = input ("Enter the name of the data : ")
encoding_text_to_float(name)





#
#fp = open("human_citation_embeddings.pkl","wb")
#pickle.dump(human_citation_embeddings, fp)
#
#fp = open("human_reference_embeddings.pkl","wb")
#pickle.dump(human_reference_embeddings, fp)
#
#fp = open("human_random_reference_embeddings.pkl","wb")
#pickle.dump(human_random_reference_embeddings, fp)




# # import pickle

# import scipy
# import scipy.cluster

# fp = open("human_true_pairs.pkl","rb")
# human_true_pairs = pickle.load(fp)

# fp = open("human_sentences.pkl","rb")
# human_sentences = pickle.load(fp)

# fp = open("auto_true_pairs.pkl","rb")
# auto_true_pairs = pickle.load(fp)

# fp = open("auto_sentences.pkl","rb")
# auto_sentences = pickle.load(fp)




'''
# word_embedding_model = models.BERT('bert-base-uncased')
# pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
#                                pooling_mode_mean_tokens=True,
#                                pooling_mode_cls_token=False,
#                                pooling_mode_max_tokens=False)

# model = SentenceTransformer(modules=[word_embedding_model, pooling_model])


# nli_reader = NLIDataReader('datasets/AllNLI')

# train_data = SentencesDataset(nli_reader.get_examples('train.gz'), model=model)
# train_dataloader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
# train_loss = losses.SoftmaxLoss(model=model, sentence_embedding_dimension=model.get_sentence_embedding_dimension(), num_labels=train_num_labels)

# sts_reader = STSDataReader('datasets/stsbenchmark')
# dev_data = SentencesDataset(examples=sts_reader.get_examples('sts-dev.csv'), model=model)
# dev_dataloader = DataLoader(dev_data, shuffle=False, batch_size=train_batch_size)
# evaluator = EmbeddingSimilarityEvaluator(dev_dataloader)

# model.fit(train_objectives=[(train_dataloader, train_loss)],
#          evaluator=evaluator,
#          epochs=num_epochs,
#          evaluation_steps=1000,
#          warmup_steps=warmup_steps,
#          output_path=model_save_path
#          )



# embedder = SentenceTransformer('bert-base-nli-max-tokens')

# # Corpus with example sentences
# corpus = ['     A man is eating a food.',
#           'A man    is eating a piece of bread.',
#           'A man is eating pasta.',
#           'The girl  is carrying a baby.',
#           'The baby is  carried by the woman',
#           'A man is riding  a horse.',
#           'A man is riding a   w hite horse on an enclosed ground.',
#           'A monkey is playing    drums.    ',
#           'Someone in a gorilla co stume is playing a set of drums.',
#           'A cheetah is running be hind its prey.  ',
#           '  A cheetah chases prey    on across a field.  ']

# corpus_embeddings = embedder.encode(corpus)

# num_clusters = 5
# whitened_corpus = scipy.cluster.vq.whiten(corpus_embeddings)
# code_book, _ = scipy.cluster.vq.kmeans(whitened_corpus, num_clusters)
# cluster_assignment, _ = scipy.cluster.vq.vq(whitened_corpus, code_book)

# print(cluster_assignment)







# model = SentenceTransformer('bert-base-nli-max-tokens')

# sentences=["The king cannot be killed","The monarch was immortal"]

# sentence_embeddings = model.encode(sentences)

# for sentence, embedding in zip(sentences, sentence_embeddings):
#     print("Sentence:", sentence)
#     print("Embedding:", embedding)
#     print("")



from torch.utils.data import DataLoader
import math
from sentence_transformers import models, losses
from sentence_transformers import SentencesDataset, LoggingHandler, SentenceTransformer
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import *
import logging
from datetime import datetime

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

# Read the dataset
batch_size = 16
nli_reader = NLIDataReader('datasets/AllNLI')
sts_reader = STSDataReader('datasets/stsbenchmark')
train_num_labels = nli_reader.get_num_labels()
model_save_path = 'output/training_nli_bert-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")



# Use BERT for mapping tokens to embeddings
word_embedding_model = models.BERT('bert-base-uncased')

# Apply mean pooling to get one fixed sized sentence vector
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])


# Convert the dataset to a DataLoader ready for training
logging.info("Read AllNLI train dataset")
train_data = SentencesDataset(nli_reader.get_examples('train.gz'), model=model)
train_dataloader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
train_loss = losses.SoftmaxLoss(model=model, sentence_embedding_dimension=model.get_sentence_embedding_dimension(), num_labels=train_num_labels)



logging.info("Read STSbenchmark dev dataset")
dev_data = SentencesDataset(examples=sts_reader.get_examples('sts-dev.csv'), model=model)
dev_dataloader = DataLoader(dev_data, shuffle=False, batch_size=batch_size)
evaluator = EmbeddingSimilarityEvaluator(dev_dataloader)

# Configure the training
num_epochs = 1

warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
logging.info("Warmup-steps: {}".format(warmup_steps))



# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=1000,
          warmup_steps=warmup_steps,
          output_path=model_save_path
          )




'''