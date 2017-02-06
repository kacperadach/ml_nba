from sklearn.cluster import KMeans
import numpy as np

from IPython.core.debugger import Tracer

from data_access import get_logs_for_clustering

def cluster_logs():
	logs = get_logs_for_clustering(name='LeBron James')
	kmeans = KMeans(n_clusters=5, random_state=0).fit(logs)
	centers = kmeans.cluster_centers_
	print kmeans.cluster_centers_
	Tracer()()


cluster_logs()