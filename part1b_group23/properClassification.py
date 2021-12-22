import pandas as pd
import sklearn.model_selection as md
from sklearn.neighbors import KNeighborsClassifier as KN
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn import metrics
import pickle

"""On the file trainTestTxt we created 2 txt files, 
one for training and one for testing, so we use the same files for our results"""
train = pd.read_csv('train.txt', header = None)
test = pd.read_csv('test.txt', header = None)
train_X = train[1]
train_Y = train[0]
test_X =  test[1]
test_Y = test[0]

""" countvectorizer -> tf transformer -> classifier -> prediction -> metrics
"""

vec = CountVectorizer()
train_x_counts = vec.fit_transform(train_X)
tf_transformer = TfidfTransformer()
train_X_tf = tf_transformer.fit_transform(train_x_counts)
clf = RF(n_estimators=100 ).fit(train_X_tf, train_Y)

test_X_counts = vec.transform(test_X)
test_x_trans = tf_transformer.transform(test_X_counts)
predicted = clf.predict(test_x_trans)
print(metrics.classification_report(test_Y, predicted))
filename1, filename2, filename3 = 'vectorizer.sav', 'transformer.sav', 'model.sav'
#pickle.dump(vec, open(filename1, 'wb'))
#pickle.dump(tf_transformer, open(filename2, 'wb'))
#pickle.dump(clf, open(filename3, 'wb'))

"""Prompt user for sentence and sentence interpretation code. """
while True:
    phrase = input('Give me a sentence! || Type: "EXIT" to exit (case-sensitive) .\nSentence: ')
    if phrase == 'EXIT':
        break
    phrase_count = vec.transform([phrase])
    phrase_tf = tf_transformer.transform(phrase_count)
    phrase_pred = clf.predict(phrase_tf)
    print("predicted dialog act: " + phrase_pred)
