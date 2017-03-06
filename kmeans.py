from collections import Counter
import operator
import pickle
import math

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np

from IPython.core.debugger import Tracer

from data_access import get_logs_for_clustering, get_player_logs_for_clustering

# def cluster_logs():
# 	logs = get_logs_for_clustering()
# 	kmeans = KMeans(n_clusters=100, random_state=0).fit(logs)
# 	centers = kmeans.cluster_centers_
# 	print kmeans.cluster_centers_
# 	Tracer()()

def optimize_kmeans(start=1000):
	logs = get_logs_for_clustering()
	n_clusters = start
	st_devs = []
	cluster_range = [1000, 10000, 20000]
	for x in cluster_range:
		print x
		kmeans = get_kmeans_player_logs(logs, x)
		st_devs.append(analyze_kmeans(kmeans, logs)/x)
	plt.plot(cluster_range, st_devs)
	plt.show()



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


def get_kmeans_player_logs(logs, n_clusters=100):
	print 'Calculating KMeans Clusters (this may take a while)...'
	kmeans = MiniBatchKMeans(init_size =3*n_clusters, n_clusters=n_clusters, batch_size= 10, random_state=0).fit(logs)
	print 'Finished Calculating KMeans'
	return kmeans
	# centers = kmeans.cluster_centers_
	# center_count = Counter(kmeans.labels_)
	# #center_count = sorted(center_count, key=operator.itemgetter(1))
	
	# print kmeans.cluster_centers_
	# pickle.dump(kmeans, open('kmeans.p', 'wb'))

optimize_kmeans()