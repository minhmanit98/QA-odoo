import os
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_TRAIN_PATH = os.path.join(DIR_PATH, 'data/train/')
DATA_TEST_PATH = os.path.join(DIR_PATH, 'data/test/')
DATA_TRAIN_JSON = os.path.join(DIR_PATH, 'processed_data/data_train.json')
DATA_TEST_JSON = os.path.join(DIR_PATH, 'processed_data/data_test.json')
FEATURES_TEST = os.path.join(DIR_PATH, 'feature_extraction/feature_test_full.pkl')
FEATURES_TRAIN = os.path.join(DIR_PATH, 'feature_extraction/feature_train_full.pkl')
VECTOR_EMBEDDING = os.path.join(DIR_PATH, 'vector_embedding/vector_embedding_full.pkl')
STOP_WORDS = os.path.join(DIR_PATH, 'stopwords-nlp-vi.txt')
SPECIAL_CHARACTER = '0123456789%@$.,=+-!;/()*"&^:#|\n\t\''
DICTIONARY_PATH = './dictionary.txt'
LOG_FILE = os.path.join(DIR_PATH, 'log/app.log')
LINEARSVC_TFIDF_MODEL = os.path.join(DIR_PATH, 'trained_model/linearSVC_tf_idf_model.pk')