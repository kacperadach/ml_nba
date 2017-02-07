from datetime import date, timedelta

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from IPython.core.debugger import Tracer

from models import Game
from data_access import get_seasonal_player_logs

PM_START_DATE = '1997-11-01'

def start_connection():
	connection.setup(['127.0.0.1'], 'nba', protocol_version=3)
	sync_table(Game)

# takes all of the player game logs and filters out duplicates per game and sorts by team
def split_games_by_team(logs):
	game_logs = {}
	date_dict = {}
	for l in logs:
		if l.team not in game_logs.keys():
			game_logs[l.team] = [l]
			date_dict[l.team] = [l.date]
		elif l.date not in date_dict[l.team]:
			game_logs[l.team].append(l)
			date_dict[l.team].append(l.date)
	return game_logs

# create Game model objects 
def create_games():
	start_connection()
	first = date(year=1997, month=1, day=1)
	second = date(year=1998, month=1, day=1)
	while first.year < 2017:
		season = str(first.year) + '-' + str(second.year)[2:]
		logs = get_seasonal_player_logs(season)
		game_logs = split_games_by_team(logs)

		print 'Creating Game Objects for {} season'.format(season)
		for key, value in game_logs.items():
			for v in value:
				Game.create(
					home_team = v.team if v.home else v.opp,
					away_team = v.opp if v.home else v.team,
					date = v.date,
					home_win = v.win if v.home else not v.win,
					playoffs = False if v.season_type == 'Regular Season' else True,
					season = v.season
				)

		first = first + timedelta(366)
		second = second + timedelta(366)

if __name__ == '__main__':
	create_games()
