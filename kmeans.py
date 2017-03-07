from collections import Counter
import operator
import pickle
import math

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np

from IPython.core.debugger import Tracer

from data_access import get_logs_for_clustering, get_player_logs_for_clustering, get_stat_labels


def optimize_kmeans():
	logs = get_logs_for_clustering()
	st_devs = []
	cluster_range = range(8000, 10000, 50)
	try:
		for x in cluster_range:
			print x
			kmeans = get_kmeans_player_logs(logs, x)
			analysis = analyze_kmeans(kmeans, logs)
			print analysis
			st_devs.append((analysis, x))
	except KeyboardInterrupt:
		pickle.dump(st_devs, open('kmeans_{}_{}.p'.format(st_devs[0][1], st_devs[len(st_devs)-1][1]), 'wb'))
	plt.plot(cluster_range[0:len(st_devs)], map(lambda x: x[0], st_devs))
	plt.ylabel('Average StDev from Center / num clusters')
	plt.xlabel('num clusters')
	plt.show()
	Tracer()()


def analyze_kmeans(kmeans, logs):
	print 'Analyzing KMeans'
	st_dev_all = []

	for i, l in enumerate(logs):
		label_num = kmeans.labels_[i]
		center = kmeans.cluster_centers_[label_num]
		st_dev = np.zeros(17)
		for j, val in enumerate(l):
			st_dev[j] = pow((val - center[j]), 2)
		st_dev_total = math.sqrt(sum(st_dev) / len(st_dev))
		st_dev_all.append(st_dev_total)

	print 'Finished Analyzing KMeans'
	return sum(st_dev_all) / len(st_dev_all)


def get_kmeans_player_logs(logs=None, n_clusters=100):
	if not logs:
		logs = get_logs_for_clustering()
	print 'Calculating KMeans Clusters (this may take a while)...'
	kmeans = MiniBatchKMeans(init_size =3*n_clusters, n_clusters=n_clusters, batch_size= 10, random_state=0).fit(logs)
	print 'Finished Calculating KMeans'
	return kmeans


def strip_player_log_for_kmeans(log):
	stat_labels = get_stat_labels().replace(',', '').split()
	stripped_log = np.zeros(len(stat_labels))
	for i, stat in enumerate(stat_labels):
		val = getattr(log, stat)
		stripped_log[i] = val
	return stripped_log

def get_kmeans_for_neural_network():
	file_name = 'kmeans.p'
	logs = get_logs_for_clustering()
	kmeans = get_kmeans_player_logs(n_clusters=100)
	analysis = analyze_kmeans(kmeans, logs)
	pickle.dump(kmeans, open(file_name, 'wb'))
	print 'KMeans saved as pickle: {}'.format(file_name)

if __name__ == '__main__':
	get_kmeans_for_neural_network()