from os import listdir
from os.path import join
import numpy as np
import string
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score

"""
Reference:
For HTML Stripper
http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
For SGD Classifier
http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
For CountVectorizer
http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
"""

# Changed path according to 
# https://piazza.com/class/ixovke53an7n1?cid=686

train_path = "../aclImdb/train/" # source data
test_path = "../imdb_te.csv" # test data for grade evaluation. 

from HTMLParser import HTMLParser

# Implementation of ML Stripper that removes HTML tags from the text using HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
    and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have three 
    columns, "row_number", "text" and label'''
    stopwords_filename = "stopwords.en.txt"
    stopwords = []
    reviews = []

    with open(stopwords_filename,'rb+') as stopwords_file:
        stopwords = stopwords_file.read().split('\n')

    positive_file_path = join(inpath,"pos")
    negative_file_path = join(inpath,"neg")
    row_num = 0

    positive_review_files = listdir(positive_file_path)
    for file_path in positive_review_files:
        review_file = join(positive_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()

            review = strip_tags(review) # removes HTML tags
            review = re.sub(r'[^\x00-\x7F]+',' ', review) # remove all characters other than ASCII with space

            for p in string.punctuation + string.digits: # replace punctuations and numbers with space
                review = review.replace(p, ' ')

            reviewwords  = [word.strip().lower() for word in review.split(' ') if word.lower() not in stopwords]
            review = ' '.join(reviewwords)

            reviews.append([row_num, review, 1])
            row_num += 1

    negative_review_files = listdir(negative_file_path)
    for file_path in negative_review_files:
        review_file = join(negative_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()

            review = strip_tags(review) #removes HTML tags
            review = re.sub(r'[^\x00-\x7F]+',' ', review) # remove all characters other than ASCII with space

            for p in string.punctuation + string.digits: # replace punctuations and numbers with space
                review = review.replace(p, ' ')
            
            reviewwords  = [word.strip().lower() for word in review.split(' ') if word.lower() not in stopwords]
            review = ' '.join(reviewwords)
            reviews.append([row_num, review, 0])
            row_num += 1

    reviews_np = np.array(reviews)
    np.savetxt(fname=name, X=reviews_np, fmt=['%s','%s','%s'], delimiter=',', header='row_number,text,polarity', comments='')
    return name
  

def get_processed_test_data():
    """
    Get processed test data from the CSV test data file and 
    remove punctuations and stopwords from it.
    """
    df = pd.read_csv(test_path)
    test_data = df['text'].tolist()
    stopwords_filename = "../stopwords.en.txt"
    stopwords = []
    processed_test_data = []

    with open(stopwords_filename,'rb+') as stopwords_file:
        stopwords = stopwords_file.read().split('\n')

    for review in test_data:

        review = strip_tags(review) # removes HTML tags
        review = re.sub(r'[^\x00-\x7F]+',' ', review) # remove all characters other than ASCII with space
        
        for p in string.punctuation + string.digits: # replace punctuations with space
            review = review.replace(p, ' ')
        
        reviewwords  = [word.lower().strip() for word in review.split(' ') if word.lower() not in stopwords]
        review = ' '.join(reviewwords)
        processed_test_data.append(review)
    
    return processed_test_data


if __name__ == "__main__":
    train_data_file = imdb_data_preprocess(train_path)
    train_data_file = 'imdb_tr.csv'
    df = pd.read_csv(train_data_file)
    text = df['text']

    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    
    vectorizer = CountVectorizer(ngram_range=(1,1))
    train_X = vectorizer.fit_transform(text)
    Y = np.array(df['polarity'])
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(train_X, Y)
    test_data = get_processed_test_data()
    test_X = vectorizer.transform(test_data)
    answer = clf.predict(test_X)
    np.savetxt(fname='unigram.output.txt', X=answer, fmt='%d')

    ''' Checking accuracy'''
    print cross_val_score(clf, X=train_X,y=Y,cv=5)

    inpath = '../aclImdb/test'
    review_X = []
    review_Y = []

    positive_file_path = join(inpath,"pos")
    negative_file_path = join(inpath,"neg")
    stopwords_filename = "../stopwords.en.txt"
    stopwords = []

    with open(stopwords_filename,'rb+') as stopwords_file:
        stopwords = stopwords_file.read().split('\n')

    positive_review_files = listdir(positive_file_path)
    for file_path in positive_review_files:
        review_file = join(positive_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()

            review = re.sub(r'[^\x00-\x7F]+',' ', review) # remove all characters other than ASCII with space

            for p in string.punctuation:
                review = review.replace(p, ' ')
            reviewwords  = [word.strip().lower() for word in review.split(' ') if word.lower() not in stopwords and not word.isdigit()]
            review = ' '.join(reviewwords)

            review_X.append(review)
            review_Y.append(1)

    negative_review_files = listdir(negative_file_path)
    for file_path in negative_review_files:
        review_file = join(negative_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()

            review = re.sub(r'[^\x00-\x7F]+',' ', review) # remove all characters other than ASCII with space

            for p in string.punctuation:
                review = review.replace(p, ' ')
            reviewwords  = [word.strip().lower() for word in review.split(' ') if word.lower() not in stopwords and not word.isdigit()]
            review = ' '.join(reviewwords)

            review_X.append(review)
            review_Y.append(0)

    vector_X = vectorizer.transform(review_X)
    Y = np.array(review_Y)
    print "Unigram"
    print clf.score(vector_X, Y)

    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    vectorizer = CountVectorizer(ngram_range=(2,2))
    train_X = vectorizer.fit_transform(text)
    Y = np.array(df['polarity'])
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(train_X, Y)
    test_data = get_processed_test_data()
    test_X = vectorizer.transform(test_data)
    answer = clf.predict(test_X)
    np.savetxt(fname='bigram.output.txt', X=answer, fmt='%d')

    ''' Checking accuracy'''
    print cross_val_score(clf, X=train_X,y=Y,cv=5)
    vector_X = vectorizer.transform(review_X)
    Y = np.array(review_Y)
    print "Bigram"
    print clf.score(vector_X, Y)
    

    '''train a SGD classifier using unigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to unigramtfidf.output.txt'''
    vectorizer = TfidfVectorizer(ngram_range=(1,1))
    train_X = vectorizer.fit_transform(text)
    Y = np.array(df['polarity'])
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(train_X, Y)
    test_X = vectorizer.transform(test_data)
    answer = clf.predict(test_X)
    np.savetxt(fname='unigramtfidf.output.txt', X=answer, fmt='%d')

    ''' Checking accuracy'''
    print cross_val_score(clf, X=train_X,y=Y,cv=5)
    vector_X = vectorizer.transform(review_X)
    Y = np.array(review_Y)
    print "Tfidf-Unigram"
    print clf.score(vector_X, Y)

    '''train a SGD classifier using bigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to bigramtfdif.output.txt'''

    vectorizer = TfidfVectorizer(ngram_range=(2,2))
    train_X = vectorizer.fit_transform(text)
    Y = np.array(df['polarity'])
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(train_X, Y)
    test_X = vectorizer.transform(test_data)
    answer = clf.predict(test_X)
    np.savetxt(fname='bigramtfidf.output.txt', X=answer, fmt='%d')

    ''' Checking performance'''
    print cross_val_score(clf, X=train_X,y=Y,cv=5)
    vector_X = vectorizer.transform(review_X)
    Y = np.array(review_Y)
    print "Tfidf- Bigram"
    print clf.score(vector_X, Y)