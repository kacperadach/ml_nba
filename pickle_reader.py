import os
from datetime import datetime

from IPython.core.debugger import Tracer

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import ValidationError

from models import PlayerGameLog
from options import TEAMS, SEASON_TYPES, TEAM_ABBR
from cluster import CassandraConnector, connect_to_cluster

NOT_TEAM_ABBR = [
	'Jr.',
	'III',
	'II',
	'IV',
	'a'
]

DIRPATH = dirpath='/home/kacper/apps/ml_nba/pickles'

NULL_VALUE_SWAP = -9999999


def get_info_from_filename(file_name):
	split = file_name.split('-')
	season = split[0].replace('_', '-')
	season_type = split[1].replace('_', ' ')
	team = split[2].replace('_', ' ')[:-2]
	return season, season_type, team

def get_data_file_names():
	return os.listdir(DIRPATH)


def create_gamelog(row, season_type):

	try:
		name = row[0][2:] + ' ' + row[1] if len(row[2]) <= 3 else row[0][2:] + ' ' + row[1] + ' ' + row[2]

		if len(row[2]) > 3:
			del row[2]

		team = row[2]
		date = datetime.strptime(row[3], '%m/%d/%Y')
		home = True if row[5] == 'vs.' else False
		opp = row[6]
		win = True if row[7] == 'W' else False

		def strip_value(value):
			if value == '-':
				return NULL_VALUE_SWAP
			if '.' in value:
				return float(value)
			return int(value)
	
		PlayerGameLog.create(
			name = name,
			team = team,
			date = date,
			home = home,
			opp = opp,
			win = win,
			season_type = season_type,
			minutes = strip_value(row[8]),
			points = strip_value(row[9]),
			fgm = strip_value(row[10]),
			fga = strip_value(row[11]),
			fgp = strip_value(row[12]),
			tm = strip_value(row[13]),
			ta = strip_value(row[14]),
			tp = strip_value(row[15]),
			ftm = strip_value(row[16]),
			fta = strip_value(row[17]),
			ftp = strip_value(row[18]),
			oreb = strip_value(row[19]),
			dreb = strip_value(row[20]),
			reb = strip_value(row[21]),
			ast = strip_value(row[22]),
			stl = strip_value(row[23]),
			blk = strip_value(row[24]),
			tov = strip_value(row[25]),
			pf = strip_value(row[26]),
			pm = strip_value(row[27])
		)
	except:
		Tracer()()


def main():
	file_names = get_data_file_names()

	cc = CassandraConnector(ip_addr_list=['127.0.0.1'], keyspace='nba', tables=[PlayerGameLog])
	#cc.sync_tables()
	sync_table(PlayerGameLog)
	#connect_to_cluster(keyspace='nba', tables=[PlayerGameLog])
	for fname in file_names:
		with open('pickles/{}'.format(fname), 'rb') as f:
			_, season_type, _ = get_info_from_filename(fname)

			lines = map(lambda x: x.split(), filter(lambda x: len(x) > 10, f.readlines()))

			for gl in lines[1:]:
				create_gamelog(gl, season_type)
			print fname + ': '+ str(len(lines[1:]))
	cc.stop()

if __name__ == '__main__':
	main()