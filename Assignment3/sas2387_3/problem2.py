import numpy as np
import csv, sys

if len(sys.argv) == 3:
    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    final_output = []

    # Reading input file
    with open(inputfilename, 'rb') as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
    csv_data = np.array(data, dtype=np.float)
    values = csv_data[:,2]
    features = csv_data[:,[0,1]]
    n = features.shape[0]

    # Calculating Standard Deviation and Mean
    stddev = np.std(features, axis=0,ddof=1)
    stddev_tiles = np.tile(stddev, (features.shape[0],1))
    mean = np.mean(features, axis=0)
    mean_tiles = np.tile(mean, (features.shape[0], 1))

    # Normalizing features using mean and std dev
    features = np.divide(np.add(features, -mean_tiles), stddev_tiles)
    ones = np.ones((features.shape[0], 1), dtype=np.float)

    # Appending one at front as intercept
    features = np.append(ones, features, axis=1)

    # Initializing beta
    beta = np.zeros((1, features.shape[1]),dtype=np.float)

    # Calculating beta for all the 9 alpha values
    alpha_values = [0.001, 0.005, 0.01, 0.05, 0.1, 0.4, 0.5, 1, 5, 10]
    
    iterations = 100
    for alpha in alpha_values:
        for i in range(1, iterations+1):
            beta = beta - (alpha * np.sum((features.T) * (np.sum(beta * features, axis=1) - values), axis=1).reshape(1,3) / n)
            # print 0.5 * np.sum(np.square(np.sum(beta * features, axis=1) - values)) / csv_data.shape[0])
        final_output.append([alpha, iterations] + beta.reshape(3).tolist())
        beta = np.zeros((1, features.shape[1]), dtype=np.float)

    """
    Custom last test case using alpha=0.99 and iterations=150
    """

    iterations = 10
    alpha = 0.99
    for i in range(1, iterations+1):
        beta = beta - (alpha * np.sum((features.T) * (np.sum(beta * features, axis=1) - values), axis=1).reshape(1,3) / n)
            # print 0.5 * np.sum(np.square(np.sum(beta * features, axis=1) - values)) / csv_data.shape[0])
    final_output.append([alpha, iterations] + beta.reshape(3).tolist())
    beta = np.zeros((1, features.shape[1]), dtype=np.float)

    # Writing output to CSV file
    with open(outputfilename, 'wb') as outputcsvfile:
            csvwriter = csv.writer(outputcsvfile, delimiter=',')
            for output in final_output:
                csvwriter.writerow(output)
else:
    print "Invalid Command"
    print "Use: python problem2.py <inputfilename> <outputfilename>"

