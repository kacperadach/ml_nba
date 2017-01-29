import os
from datetime import datetime

from IPython.core.debugger import Tracer

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import ValidationError

from models import PlayerGameLog
from options import TEAMS, SEASON_TYPES, TEAM_ABBR, NOT_TEAM_ABBR
from cluster import CassandraConnector, connect_to_cluster


def start_connection():
	connection.setup(['127.0.0.1'], 'nba', protocol_version=3)
	sync_table(PlayerGameLog)

DIRPATH = dirpath='/home/kacper/apps/ml_nba/pickles'

NULL_VALUE_SWAP = -9999999


def get_info_from_filename(file_name):
	split = file_name.split('-')
	season = split[0].replace('_', '-')
	season_type = split[1].replace('_', ' ')
	team = split[2].replace('_', ' ')[:-2]
	return season, season_type, team

def get_data_file_names():
	return sorted(os.listdir(DIRPATH), key = lambda x: int(x[0:4]))

def hm_names(row):

	def isAllUpper(name):
		for letter in name:
			if str.islower(letter):
				return False
		return True

	def isInvalidName(name):
		return isAllUpper(name) and name not in NOT_TEAM_ABBR

	if isInvalidName(row[0]) and len(row[0]) <= 3:
		return 0, None
	elif isInvalidName(row[1]) and len(row[1]) <= 3:
		return 1, row[0]
	elif isInvalidName(row[2]) and len(row[2]) <= 3:
		return 2, row[0] + ' ' + row[1]
	elif isInvalidName(row[3]):
		return 3, row[0] + ' ' + row[1] + ' ' + row[2]
	else:
		return 4, row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3]


def create_gamelog(row, season, season_type, team):
	try:
		num_names, name = hm_names(row)

		# if row[0] == 'aVLAC':
		# 	Tracer()()

		# 1990-91 SUNS - Kurt Rambis 26 minutes
		
		if num_names == 0:
			if season == '1995-96' and team == TEAM_ABBR['BKN'] and season_type == 'Regular Season':
				name = 'Robert Werdann'
				row = ['Robert', 'Werdann'] + row
				print 'Replaced Name with Robert Werdann'
			elif season == '1990-91' and team == TEAM_ABBR['LAC'] and season_type == 'Regular Season':
				name = 'Loy Vaught'
				row = ['Loy', 'Vaught'] + row
				print 'Replaced Name with Loy Vaught'
			else:
				Tracer()()
		elif num_names == 1:
			row = [0] + row
		elif num_names == 3:
			del row[0]
		elif num_names == 4:
			del row[0]
			del row[0]

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
	except Exception as e:
		Tracer()()

def main():
	file_names = get_data_file_names()

	#cc = CassandraConnector(ip_addr_list=['127.0.0.1'], keyspace='nba', tables=[PlayerGameLog])
	#cc.sync_tables()
	#sync_table(PlayerGameLog)
	#connect_to_cluster(keyspace='nba', tables=[PlayerGameLog])
	game_logs_created = 0
	start_connection()
	index = 236
	for fname in file_names[236:]:
		with open('pickles/{}'.format(fname), 'rb') as f:
			season, season_type, team = get_info_from_filename(fname)

			lines = map(lambda x: x.split(), filter(lambda x: len(x) > 10, f.readlines()))

			for gl in lines[1:]:
				gl[0] = gl[0][2:]
				create_gamelog(gl, season, season_type, team)

			print fname + ': '+ str(len(lines[1:])) + ' - ' + str(index)
			game_logs_created += len(lines[1:])
			index += 1

	print game_logs_created + ' game logs created.'

if __name__ == '__main__':
	main()