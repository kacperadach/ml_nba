from sklearn.cluster import KMeans
import numpy as np

from IPython.core.debugger import Tracer

from data_access import get_logs_for_clustering

# def cluster_logs():
# 	logs = get_logs_for_clustering()
# 	kmeans = KMeans(n_clusters=100, random_state=0).fit(logs)
# 	centers = kmeans.cluster_centers_
# 	print kmeans.cluster_centers_
# 	Tracer()()


def get_kmeans_player_logs(n_clusters=100):
	logs = get_logs_for_clustering()
	kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(logs)
	centers = kmeans.cluster_centers_
	print kmeans.cluster_centers_
	Tracer()()

get_kmeans_player_logs()