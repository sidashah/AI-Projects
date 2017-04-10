import numpy as np
import csv, sys
from scipy.interpolate import griddata
from sklearn import svm
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV,train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


if len(sys.argv) == 3:
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    final_output = []

    # Reading input csv file
    with open(inputfilename, 'rb') as csvfile:
        csv_data = list(csv.reader(csvfile, delimiter=','))
    data = np.array(csv_data[1:], dtype=np.float64)

    ones = data[data[:,2] == 1]
    zeros = data[data[:,2] == 0]

    X = data[:,[0,1]]
    Y = data[:,2]
    # Spliting training and test data
    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, train_size=0.6, test_size=0.4, random_state=3)

    # Running SVM for linear kernel
    parameters = {'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(SVC(kernel='linear'), parameters, cv=5)
    clf.fit(train_X, train_Y)
    final_output.append(['svm_linear',clf.best_score_,clf.score(test_X,test_Y)]) 

    # Running SVM for poly kernel
    parameters = {'gamma':[0.1, 1], 'degree':[4, 5, 6], 'C':[0.1, 1, 3]}
    clf = GridSearchCV(SVC(kernel='poly'), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['svm_polynomial',clf.best_score_,clf.score(test_X,test_Y)])

    # Running SVM for RBF kernel
    parameters = {'gamma':[0.1, 0.5, 1, 3, 6, 10], 'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(SVC(kernel='rbf'), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['svm_rbf',clf.best_score_,clf.score(test_X,test_Y)])

    # Running Logistic Regression
    parameters = {'C':[0.1, 0.5, 1, 5, 10, 50, 100]}
    clf = GridSearchCV(LogisticRegression(), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['logistic',clf.best_score_,clf.score(test_X,test_Y)])

    # Running KNN
    parameters = {'n_neighbors' : range(1,51), 'leaf_size' : range(5,61,5)}
    clf = GridSearchCV(KNeighborsClassifier(), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['knn',clf.best_score_,clf.score(test_X,test_Y)])

    # Running  Decision Tree Classifier
    parameters = {'max_depth' : range(1,51), 'min_samples_split' : range(2,11)}
    clf = GridSearchCV(DecisionTreeClassifier(), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['decision_tree',clf.best_score_,clf.score(test_X,test_Y)])

    # Running Random Forest Classifier
    parameters = {'max_depth' : range(1,51), 'min_samples_split' : range(2,11)}
    clf = GridSearchCV(RandomForestClassifier(), param_grid=parameters, cv=5, n_jobs = 8)
    clf.fit(train_X, train_Y)
    final_output.append(['random_forest',clf.best_score_,clf.score(test_X,test_Y)])

    # Writing output to csv file
    with open(outputfilename, 'wb') as outputcsvfile:
        csvwriter = csv.writer(outputcsvfile, delimiter=',')
        for output in final_output:
            csvwriter.writerow(output)
else:
    print "Invalid Command"
    print "Use: python problem3.py <inputfilename> <outputfilename>"
