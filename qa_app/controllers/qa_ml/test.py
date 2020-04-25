# from underthesea import word_tokenize
from nltk.tokenize import word_tokenize
import nltk
from underthesea import pos_tag
from nltk.corpus import stopwords
from nltk import pos_tag
import string

def read_stopwords(file):
    with open(file, 'r', encoding="utf8") as f:
        stopwords = set([w.strip() for w in f.readlines()])
    return stopwords
# stop_words = set(read_stopwords('stopwords.txt'))
stop_words = set(stopwords.words('english'))
# text = " 2. cho e hỏi là thi quốc phòng hp1 có đc mang cuốn tài liều phô ở bên ngoài vô đc ko ạ hay chỉ đc mang vở mình viết bài ạ ??"
text = "Based on a non consummated marriage, what is the process to annul my marriage? "
# Remove punctuation
def RemovePunction(tokens):
    return[t for t in tokens if t not in string.punctuation]

lemmer = nltk.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

# tokens = RemovePunction(word_tokenize(text))
# tokens = (" ").join(tokens)
# pos_tokens = [word for word,pos in pos_tag(tokens)]
# word_tokens = LemTokens(pos_tokens)

tokens = RemovePunction(nltk.word_tokenize(text))
pos_tokens = [word for word,pos in pos_tag(tokens, tagset='universal')]
word_tokens = LemTokens(pos_tokens)

print(lemmer)
print(pos_tokens)
print(word_tokens)
