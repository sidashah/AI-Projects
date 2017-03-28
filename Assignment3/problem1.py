import csv
import numpy as np
import sys

def calc_func(weights, features):
    return np.dot(weights, features)

if len(sys.argv) == 3:
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    with open('input1.csv', 'rb') as csvfile:
        csv = list(csv.reader(csvfile, delimiter=','))
    
    csv_data = np.array(csv, dtype=np.integer)
    ones = np.ones((csv_data.shape[0],1), dtype=np.integer)
    csv_data = np.append(ones, csv_data, axis=1)
    y = csv_data[:,3]
    features = csv_data[:,[0,1,2]]
    weights = np.zeros(features.shape[1],dtype=np.integer)

    newweights = np.zeros(features.shape[1],dtype=np.integer)

    for i in range(0, csv_data.shape[0]):
        if y[i] * calc_func(weights, features[i,:]) <= 0:
            weights = weights + y[i] * features[i,]
    print "W",weights
    # TODO : Write to CSV

    while not np.array_equal(newweights, weights):
        newweights = weights
        for i in range(0, csv_data.shape[0]):
            if y[i] * calc_func(weights, features[i,:]) <= 0:
                weights = weights + y[i] * features[i,]
        print "W",weights
        # TODO : Write to CSV

