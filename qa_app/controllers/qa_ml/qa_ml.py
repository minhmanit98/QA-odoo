import pandas as pd
import os
import json
import nltk
from underthesea import word_tokenize
from underthesea import pos_tag
import numpy as np
import pickle
import string
import random
import timeit

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 

import warnings
warnings.simplefilter('ignore')
import os


path = os.path.dirname(os.path.realpath(__file__))
convdata = pd.read_csv(path+'/legal_help_clean.csv')

#show header of the dataset
convdata.head()

#covert dataframes to json
convdata_json = json.loads(convdata.to_json(orient='records'))
convdata_json[0:2]

#export as data as JSON
with open(path+'/conversation_json.json', 'w', encoding="utf8") as outfile:
    json.dump(convdata_json, outfile, ensure_ascii=False)

#greeting function
GREETING_INPUTS = ("hello", "hi", "greetings", "hello i need help", "good day","hey","i need help", "greetings")
GREETING_RESPONSES = ["Good day, How may i of help?", "Hello, How can i help?", "hello", "I am glad! You are talking to me."]
           
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

#Wordnet Lemmatization 

lemmer = nltk.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

# Remove punctuation
def RemovePunction(tokens):
    return[t for t in tokens if t not in string.punctuation]

def read_stopwords(file):
    with open(file, 'r', encoding="utf8") as f:
        stopwords = set([w.strip() for w in f.readlines()])
    return stopwords

# Create a stopword list from the standard list of stopwords available in nltk
# stop_words = set(stopwords.words('english'))
stop_words = set(read_stopwords(path+'/stopwords.txt'))

def QA_ML(test_set_sentence):
    json_file_path = path+"/conversation_json.json"
    tfidf_vectorizer_pickle_path = path + "/tfidf_vectorizer.pkl"
    tfidf_matrix_pickle_path = path+ "/tfidf_matrix_train.pkl"
    
    i = 0
    sentences = []
    
    # ---------------Tokenisation of user input -----------------------------#
    
    tokens = RemovePunction(word_tokenize(test_set_sentence))
    tokens = (" ").join(tokens)
    pos_tokens = [word for word,pos in pos_tag(tokens)]
    
    word_tokens = LemTokens(pos_tokens)
    
    filtered_sentence = []
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)  
    
    filtered_sentence =" ".join(filtered_sentence).lower()
            
    test_set = (filtered_sentence, "")
    
    #For Tracing, comment to remove from print.
    #print('USER INPUT:'+filtered_sentence)
    
    # -----------------------------------------------------------------------#
        
    try: 
        # ---------------Use Pre-Train Model------------------#
        f = open(tfidf_vectorizer_pickle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()
        
        f = open(tfidf_matrix_pickle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        # ---------------------------------------------------#
    except: 
        # ---------------To Train------------------#
        
        start = timeit.default_timer()
        
        with open(json_file_path, encoding="utf8") as sentences_file:
            reader = json.load(sentences_file)
            
            # ---------------Tokenisation of training input -----------------------------#    
            
            for row in reader:
                db_tokens = RemovePunction(word_tokenize(row['MESSAGE']))
                db_tokens = (" ").join(db_tokens)
                pos_db_tokens = [word for word,pos in pos_tag(db_tokens)]
                db_word_tokens = LemTokens(pos_db_tokens)
                
                db_filtered_sentence = [] 
                for dbw in db_word_tokens: 
                    if dbw not in stop_words: 
                        db_filtered_sentence.append(dbw)  
                
                db_filtered_sentence =" ".join(db_filtered_sentence).lower()
                
                #Debugging Checkpoint
                print('TRAINING INPUT: '+db_filtered_sentence)
                
                sentences.append(db_filtered_sentence)
                i +=1                
            # ---------------------------------------------------------------------------#
                
        tfidf_vectorizer = TfidfVectorizer() 
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)
        
        #train timing
        stop = timeit.default_timer()
        print ("Training Time : ")
        print (stop - start) 
    
        f = open(tfidf_vectorizer_pickle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f) 
        f.close()
    
        f = open(tfidf_matrix_pickle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f) 
        f.close 
        # ------------------------------------------#
        
    #use the learnt dimension space to run TF-IDF on the query
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    #then run cosine similarity between the 2 tf-idfs
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    
    #if not in the topic trained.no similarity 
    idx= cosine.argsort()[0][-2]
    flat =  cosine.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if (req_tfidf==0): #Threshold A
        
        not_understood = "Apology, I do not understand. Can you rephrase?"
        
        return not_understood, not_understood, 2
        
    else:
        
        cosine = np.delete(cosine, 0)

        #get the max score
        max = cosine.max()
        response_index = 0

        #if max score is lower than < 0.34 > (we see can ask if need to rephrase.)
        if (max <= 0.34): #Threshold B
            
            not_understood = "Apology, I do not understand. Can you rephrase?"
            
            return not_understood,not_understood, 2
        else:

                #if score is more than 0.91 list the multi response and get a random reply
                if (max > 0.95):
                    new_max = max - 0.05 
                    # load them to a list
                    list = np.where(cosine > new_max) 
                   
                    # choose a random one to return to the user 
                    response_index = random.choice(list[0])
                    response_index=response_index+2
                elif (max > 0.91): #Threshold C
                    
                    new_max = max - 0.05 
                    # load them to a list
                    list = np.where(cosine > new_max) 
                   
                    # choose a random one to return to the user 
                    response_index = random.choice(list[0])
                else:
                    # else we would simply return the highest score
                    response_index = np.where(cosine == max)[0][0] + 2 

                j = 0 

                with open(json_file_path, "r",encoding="utf8") as sentences_file:
                    reader = json.load(sentences_file)
                    for row in reader:
                        j += 1 
                        if j == response_index: 
                            return row["RESPONSE"], row["MESSAGE"], max
                            break

