import os
from datetime import datetime

from cluster import connect_to_cluster, disconnect_from_cluster
from models import PlayerGameLog

PM_START_DATE = '1997-11-01'

def get_player_logs(name, team=None, opp=None, date=None, limit=100):
	
	cluster, session = connect_to_cluster(keyspace='nba')
	cql_query = "SELECT * FROM player_game_log WHERE name = '{}'".format(name)
	# if name:
	# 	cql_query += " AND date >= '{}'".format(date_low)
	# if date_high:
	# 	cql_query += " AND date <= '{}'".format(date_high)
	cql_query += " LIMIT {} ALLOW FILTERING".format(limit)
	rows = map(lambda x: x, session.execute(cql_query))
	disconnect_from_cluster(cluster)
	return rows

def get_stat_labels():
	#return 'minutes, points, fgm, fga, fgp, tm, ta, tp, ftm, fta, ftp, oreb, dreb, reb, ast, stl, blk, tov, pf, pm'
	return 'minutes, points, fgm, fga, tm, ta, ftm, fta, oreb, dreb, reb, ast, stl, blk, tov, pf, pm'

def get_logs_for_clustering(limit=1000000):
	cluster, session = connect_to_cluster(keyspace='nba')
	cql_query = "SELECT {} FROM player_game_log WHERE date > '{}' LIMIT {} ALLOW FILTERING".format(get_stat_labels(), PM_START_DATE, limit)
	rows = map(lambda x: x, session.execute(cql_query))
	disconnect_from_cluster(cluster)
	return rows


# def get_num_of_data_points(base, counter):
# 	cluster, session = connect_to_cluster()
# 	cql_query = "SELECT count(*) FROM currency_pair_value WHERE base = '{}' AND counter = '{}'".format(base.upper(), counter.upper())
# 	count = session.execute(cql_query)
# 	disconnect_from_cluster(cluster)
# 	return count[0].count

if __name__ == "__main__":
	a = get_currency_data_from_cass(base="EUR", counter="USD")
	print(len(a))


