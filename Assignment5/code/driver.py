from os import listdir
from os.path import join
import numpy as np

train_path = "aclImdb/train/" # source data
test_path = "imdb_te.csv" # test data for grade evaluation. 


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
    and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have three 
    columns, "row_number", "text" and label'''
    positive_file_path = join(inpath,"pos")
    reviews = []
    negative_file_path = join(inpath,"neg")

    row_num = 0

    positive_review_files = listdir(positive_file_path)
    for file_path in positive_review_files:
        review_file = join(positive_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()
            review = review.replace("\"","\"\"")
            reviews.append([row_num, review, 1])
            row_num += 1

    negative_review_files = listdir(negative_file_path)
    for file_path in negative_review_files:
        review_file = join(negative_file_path, file_path)
        with open(review_file, 'rb+') as text_file:
            review = text_file.read()
            review = review.replace("\"","\"\"")
            reviews.append([row_num, text_file.read(),0])
            row_num += 1

    reviews_np = np.array(reviews)
    np.savetxt(fname=name, X=reviews_np, fmt=['%s','"%s"','%s'], delimiter=',', header='row_number,text,polarity', comments='')
  
if __name__ == "__main__":
    imdb_data_preprocess(train_path)
    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''

    
    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''

     
    '''train a SGD classifier using unigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to unigram.output.txt'''

    
    '''train a SGD classifier using bigram representation
     with tf-idf, predict sentiments on imdb_te.csv, and write 
     output to unigram.output.txt'''

    pass