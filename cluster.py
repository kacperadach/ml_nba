from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table

# cluster = Cluster(['127.0.0.1'])

def connect_to_cluster(keyspace):
	cluster = Cluster(['127.0.0.1'])
	session = cluster.connect(keyspace)
	return cluster, session

def disconnect_from_cluster(cluster):
	Cluster.shutdown(cluster)

class CassandraConnector(object):

	def __init__(self, ip_addr_list, keyspace, tables):
		self.keyspace = keyspace
		self.tables = tables
		self.cluster = Cluster(ip_addr_list)
		self.start()
	
	def sync_tables(self):
		for t in self.tables:
			sync_table(t)

	def start(self):
		self.cluster.connect(self.keyspace)
	
	def stop(cluster):
		Cluster.shutdown(self.cluster)

