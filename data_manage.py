import os

from IPython.core.debugger import Tracer

from options import TEAMS, SEASON_TYPES

DIRPATH = dirpath='/home/kacper/apps/ml_nba/pickles'



def get_info_from_filename(file_name):
	split = file_name.split('-')
	season = split[0].replace('_', '-')
	season_type = split[1].replace('_', ' ')
	team = split[2].replace('_', ' ')[:-2]
	return season, season_type, team

def get_data_file_names():
	return os.listdir(DIRPATH)

def main():
	file_names = get_data_file_names()
	# for f in file_names:
	# 	season, season_type, team = get_info_from_filename(f)
	# 	print '{}  {}  {}'.format(season, season_type, team)
	with open('pickles/{}'.format(file_names[0]), 'rb') as f:
		print(get_info_from_filename(file_names[0]))
		lines = f.readlines()
		#Tracer()()

if __name__ == '__main__':
	main()