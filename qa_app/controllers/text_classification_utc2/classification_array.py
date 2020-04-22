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

# parser = argparse.ArgumentParser("classification.py")
# text = parser.add_argument_group("The following arguments are mandatory for text option")
# text.add_argument("--text", metavar="TEXT", help="text to predict", nargs="?")
# args = parser.parse_args()

# if not args.text:
#     parser.print_help()
# if args.text:
#     data = args.text\
# line=[' ad cho e hoi bay giơ thi ktx co con phong nao trong khong a','ad cho em hoi bao gio hoan tra lai tien bao hiem y te vay a ?'
# ,'cho em hoi la dau nam nha truong vs ngan hang lam the mien phi cho hoc sinh. dau nam em co dien thong tin va ki vao giay lam the roi nhung bay gio nhan đuoc thong bao bo sung thong tin. va sau khi bo sung em dong 100k voi noi dung la lam lai the. Trong khi do em cung chua co the hay lam mat the gi ca. anh va giay cmnd em cung nop dau nam roi.',
# 'cho e hoi hom thu 7 e co thay thong bao mo lop tieng anh chuyen nghanh va vai dang ki thi full mat nhung gio len ban dao tao de xin dang ki bo sung thi lai bao khong mo lop vay gio e muon dang ki bo sung thi o dau a vi la k55 nen e dang rat gap a',
# 'em co thac mac xin duoc giai dap a lan thi anh van dau vao. em xep loai A, va hien gio truong co to chuc lop hoc phan anh van, em muon hoi la lop nay minh dang ki theo tung ca nhan hay bat buoc a? Vi hien gio em co lop hoc anh van o ngoai r a em hoc ben tu đong hoa. Em xin cam on',
# 'Truong minh con to chuc thi tu do tieng anh A2 k a']
line=['Tại sao lại có cái khái niệm vô lý vậy nhỉ, thẻ xe tháng trước tháng này làm lại thì kêu hết thẻ tháng, kh lẽ giữ xe lại có khái niệm giới hạn thẻ xe tháng ạ',
'Mong nhà trường cho người kiểm tra gắt gao hơn dãy nhà e4 ạ, chiều thứ 5 em phát hiện có 1 số bạn bài bạc trong lớp học vi phạm nội quy nhà trường, đồng thời kiểm tra thẻ sinh viên gắt gao 1 tí , chứ em bị ăn cắp trong khuôn viên giảng đường rồi ạ',
'Cho em hỏi tí. Học lại mà rớt môn cũng được xét học bổng phải không admin',
'Ad cho em hỏi. Đợt vừa rồi em đăng kí mở lớp kì 8 của k56, không biết khi nào mới duyệt xong vậy? Mong trường duyệt sớm để tụi em còn học để kịp cho đợt bảo vệ sắp tới.',
'Ad ơi cho em hỏi, bây giờ em ko học lớp học phần anh văn, mà em học ở ngoài. R lấy thi lấy bằng ở ngoài được ko. Và học anh văn chuyên ngành là năm mấy ạ',
'Cho em hỏi khi nào mới biết đậu hay rớt gdqp vậy ạ?',
' Ad cho em hỏi là kì vừa rồi em được xếp loại giỏi nhưng em có Học Lại 1 môn của Kì Trước nữa và bị rớt. Vậy em có được xét học bổng không ạ.',
'Em muốn bảo lưu điểm phải làm sao ạ, bảo lưu được bao nhiêu năm, rồi cần làm những vấn đề gì ạ']
for dat in line:
    data=dat.lower()
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