# -*- coding: utf-8 -*-
import os
import json
import settings
from datetime import datetime
from fileProcess import FileReader, FileStore 
from preProcessData import FeatureExtraction
import numpy as np
import itertools

import matplotlib.pyplot as plt
import pickle as pickle
from gensim import corpora, matutils
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
import logging
from numpy.core.umath_tests import inner1d

class Classifier(object):
    def __init__(self, features_train = None, labels_train = None, features_test = None, labels_test = None, estimator=None):
        self.features_train = features_train
        self.features_test = features_test  
        self.labels_train = labels_train
        self.labels_test = labels_test
        self.estimator = estimator

    def training(self):
        print(( 'Tranning... ',  str(datetime.now())))
        self.estimator.fit(self.features_train, self.labels_train)
        self.__training_result()
        print('Tranning Done! ',  str(datetime.now()))

    def save_model(self, filePath):
        print('Saving Model... ',  str(datetime.now()))
        FileStore(filePath=filePath).save_pickle(obj=self.estimator)
        print('Save Model Done! ',  str(datetime.now()))

    def __training_result(self):
        y_true, y_pred = self.labels_test, self.estimator.predict(self.features_test)
        cnf_matrix = confusion_matrix(y_true, y_pred)
        plot_confusion_matrix(cnf_matrix,normalize=False, title='Confusion matrix from LinearSVC')
        print(( 'Accurancy: ',self.estimator.score(self.features_test,self.labels_test)))
        print((classification_report(y_true, y_pred)))
        logging.info(('Accurancy: ',self.estimator.score(self.features_test,self.labels_test)))
        logging.info((classification_report(y_true, y_pred)))

def plot_confusion_matrix(cm, 
                          normalize=False,
                          title='Confusion matrix'):
    classes= ["admin","ban công tác chính trị và sinh viên","ban khảo thí & đảm bảo chất lượng","ban quản lý ký túc xá","ban thiết bị quản trị","ban thông tin thư viện","ban tổ chức hành chính","ban đào tạo","cố vấn","giảng viên","khác","null2"," trung tâm đào tạo thực hành","đoàn và hội"]
    plt.figure()
    # if normalize:
    #     cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #     print("Normalized confusion matrix")
    # else:
    #     print('Confusion matrix, without normalization')

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1, keepdims = True)

    plt.imshow(cm, interpolation='nearest',cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(list(range(cm.shape[0])), list(range(cm.shape[1]))):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('./log/unnormalized_Confusion_Matrix_SVC.png')
    plt.show()  
if __name__ == '__main__':
    # Read feature extraction 
    print(('Reading Feature Extraction... ',  str(datetime.now())))
    features_test_loader = pickle.load(open(settings.FEATURES_TEST,'rb'))
    features_train_loader = pickle.load(open(settings.FEATURES_TRAIN,'rb'))
    features_train, labels_train = FeatureExtraction(data=features_train_loader).read_feature()
    features_test, labels_test = FeatureExtraction(data=features_test_loader).read_feature()
    print(('Read Feature Extraction Done! ',  str(datetime.now())))

    logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)
    logging.info(('Training by SVM classification ... ',  str(datetime.now())))
    print('Training by SVM classification ...', str(datetime.now()))
    logging.info('\nModel: LinearSVC\nC = 10\nPenalty=\'l2\'\nMax_iter = 10')
    estSVC = Classifier(features_train=features_train, features_test=features_test, labels_train=labels_train, labels_test=labels_test, estimator = LinearSVC(random_state=0, C=10, max_iter=10))
    estSVC.training()
    estSVC.save_model(filePath=settings.LINEARSVC_TFIDF_MODEL) # save Model
    print('Training by SVC Classifier Done !', str(datetime.now()))
    logging.info(('Training by SVM Done! ',  str(datetime.now())))
    