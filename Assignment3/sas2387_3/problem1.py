import csv
import numpy as np
import sys

"""
Calculates dot product of weights and features
"""
def calc_func(weights, features):
    return np.dot(weights, features)

if len(sys.argv) == 3:
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]

    # Reading from CSV file
    with open(inputfilename, 'rb') as csvfile:
        csv = list(csv.reader(csvfile, delimiter=','))
    
    csv_data = np.array(csv, dtype=np.double)
    y = csv_data[:,2]

    ones = np.ones((csv_data.shape[0],1), dtype=np.double)
    features = np.append(csv_data[:,[0,1]], ones, axis=1)

    weights = np.zeros(features.shape[1],dtype=np.double)
    newweights = np.zeros(features.shape[1],dtype=np.double)

    # First iteration to get initial weights
    for i in range(0, csv_data.shape[0]):
        if y[i] * calc_func(weights, features[i,:]) <= 0:
            weights = weights + y[i] * features[i,]

    final_weights = np.array([weights], copy=True)

    # Iterate till you don't have same weights
    while not np.array_equal(newweights, weights):
        newweights = weights
        for i in range(0, csv_data.shape[0]):
            if y[i] * calc_func(weights, features[i,:]) <= 0:
                weights = np.array(weights + y[i] * features[i,], copy=True)
        final_weights = np.concatenate((final_weights, np.array([weights])), axis=0)
    
    # Write to CSV file (using integer format string)
    np.savetxt(outputfilename, final_weights, delimiter=",", fmt="%d")
else:
    print "Invalid Command"
    print "Use: python problem1.py <inputcsvfile> <outputcsvfile>"


