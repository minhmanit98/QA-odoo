import numpy as np
from random import randint
import os
import json
import settings
import pickle as pickle
from fileProcess import FileReader, FileStore
from preProcessData import FeatureExtraction ,NLP
from pyvi import ViTokenizer
from sklearn.svm import LinearSVC
from gensim import corpora, matutils
from sklearn.metrics import classification_report
from argparse import ArgumentParser
import os.path
import argparse

parser = argparse.ArgumentParser("classification.py")
text = parser.add_argument_group("The following arguments are mandatory for text option")
text.add_argument("--text", metavar="TEXT", help="text to predict", nargs="?")
args = parser.parse_args()

if not args.text:
    parser.print_help()
if args.text:
    data = args.text
    data=data.lower()
    print(data)
    classifier = pickle.load(open(settings.LINEARSVC_TFIDF_MODEL,'rb'))
    
    # bow
    # dense = FeatureExtraction(None).get_dense(text=data.decode('utf-16le'))
    # features = [] 
    # features.append(dense)
    
    # tf-idf
    vectorizer = pickle.load(open(settings.VECTOR_EMBEDDING,'rb'))
    data_features = []
    data_features.append(' '.join(NLP(text=data).get_words_feature()))
    features = vectorizer.transform(data_features)
    
    # predict result 
    print(classifier.predict(features))