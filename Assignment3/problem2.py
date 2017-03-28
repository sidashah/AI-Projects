import numpy as np
import csv, sys

with open('input2.csv', 'rb') as csvfile:
    data = list(csv.reader(csvfile, delimiter=','))
csv_data = np.array(data, dtype=np.double)
features = csv_data[:,[0,1]]
values = csv_data[:,2]

stddev = np.std(features, axis=0)
stddev_tiles = np.tile(stddev, (features.shape[0],1))
mean = np.mean(features, axis=0)
mean_tiles = np.tile(mean, (features.shape[0],1))

features = np.divide(np.add(features, -mean_tiles), stddev_tiles)
float_formatter = lambda x: "%.2f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

beta = np.zeros((features.shape[0], features.shape[1]+1))

R = 0.5 * np.sum(np.square(beta[:,0] + np.sum(beta[:,[1,2]] * features, axis=1) - values)) / csv_data.shape[0]