import os
from datetime import datetime
import pickle

from IPython.core.debugger import Tracer

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import ValidationError

from models import PlayerGameLog
from options import TEAMS, SEASON_TYPES, TEAM_ABBR, NOT_TEAM_ABBR
from cluster import CassandraConnector, connect_to_cluster


DIRPATH = dirpath='/home/kacper/apps/ml_nba/pickles'

NULL_VALUE_SWAP = -9999999

def start_connection():
	connection.setup(['127.0.0.1'], 'nba', protocol_version=3)
	sync_table(PlayerGameLog)


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
		return isAllUpper(name) and name not in NOT_TEAM_ABBR and '.' not in name

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
	num_names, name = hm_names(row)
	
	if num_names == 0:
		# ignoring missing names for now
		name = 'noname'
		row = [0, 1] + row
		
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
		season = season,
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


def main():
	file_names = get_data_file_names()

	game_logs_created = 0
	start_connection()
	for fname in file_names:
		with open('pickles/{}'.format(fname), 'rb') as f:
			season, season_type, team = get_info_from_filename(fname)

			lines = map(lambda x: x.split(), filter(lambda x: len(x) > 10, f.readlines()))

			for gl in lines[1:]:
				gl[0] = gl[0][2:] # removes 'aV' from first element of each row
				try:
					create_gamelog(gl, season, season_type, team)
					game_logs_created += 1 
				except:
					Tracer()()
					pass

			print fname + ': ' + str(len(lines[1:]))

	print str(game_logs_created) + ' game logs created.'

if __name__ == '__main__':
	main()