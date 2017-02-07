import os
from datetime import datetime

from cluster import connect_to_cluster, disconnect_from_cluster
from models import PlayerGameLog, Game

PM_START_DATE = '1997-11-01'

def game_exists(home, away, date):
	filter_dict = {
		'=': ('home_team', home),
		'=': ('away_team', away),
		'=': ('date', date)
	}
	count = make_query(make_query_string(count=True, model=Game, filter_dict=filter_dict))
	return count == 1

def make_query(query_string):
	cluster, session = connect_to_cluster(keyspace='nba')
	rows = map(lambda x: x, session.execute(query_string))
	disconnect_from_cluster(cluster)
	return rows


def make_query_string(model, columns=None, count=False, filter_dict={}, limit=None):
	if not columns and not count:
		seleted_columns = '*'
	elif count:
		seleted_columns = 'count(*)'
	else:
		seleted_columns = columns
	cql_query = "SELECT {} FROM {}".format(seleted_columns, model.get_model_string())
	if filter_dict:
		cql_query += " WHERE"
		for key, value in filter_dict.items():
			cql_query += " {} {} '{}'".format(value[0], key, value[1])
	if limit:
		cql_query += " LIMIT {}".format(limit)
	if filter_dict:
		cql_query += " ALLOW FILTERING"
	return cql_query


def get_seasonal_player_logs(season):
	filter_dict = {
		'=': ('season', season)
	}
	return make_query(make_query_string(model=PlayerGameLog, filter_dict=filter_dict))


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


