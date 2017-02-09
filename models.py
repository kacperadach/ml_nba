import uuid
from datetime import datetime

from cassandra.cqlengine.columns import UUID, Text, DateTime, Float, Date, Integer, Boolean, Set
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

# PLAYER TEAM DATE MATCHUP W/L MIN PTS FGM FGA FG% 3PM 3PA 3P% FTM FTA FT% OREB DREB REB AST STL BLK TOV PF +/-

class PlayerGameLog(Model):
	name = Text(primary_key=True, required=True)
	team = Text(required=True)
	date = Date(primary_key=True, clustering_order="ASC")
	home = Boolean(required=True)
	opp = Text(required=True)
	win = Boolean(required=True)
	season = Text(required=True)
	season_type = Text(required=True)
	minutes = Integer()
	points = Integer()
	fgm = Integer()
	fga = Integer()
	fgp = Float()
	tm = Integer() # 3's made
	ta = Integer() # 3's attempted
	tp = Float()  # 3 percentage
	ftm = Integer()
	fta = Integer()
	ftp = Float()
	oreb = Integer()
	dreb = Integer()
	reb = Integer()
	ast = Integer()
	stl = Integer()
	blk = Integer()
	tov = Integer()
	pf = Integer()
	pm = Integer()

	@staticmethod
	def get_model_string():
		return 'player_game_log'

	def validate(self):
		super(PlayerGameLog, self).validate()


class Game(Model):
	home_team = Text(primary_key=True, required=True)
	away_team = Text(primary_key=True, required=True)
	date = Date(primary_key=True, clustering_order="ASC")
	home_win = Boolean(required=True)
	playoffs = Boolean(required=True)
	season = Text(required=True)

	home_players = Set(value_type=Integer)
	away_players = Set(value_type=Integer)
	# cassandra.cqlengine.columns.Set

	# home_rest = Integer()	# number of games past X days
	# away_rest = Integer()

	# home_success = Integer()	# recent record past X games
	# away_success = Integer()

	home_wins = Integer()
	home_losses = Integer()

	away_wins = Integer()
	away_losses = Integer()

	# rest for each team
	# recent success for each team
	# records for each team

	@staticmethod
	def get_model_string():
		return 'game'

	def validate(self):
		super(Game, self).validate()
		# if game_exists(home=self.home_team, away=self.away_team, date=self.date):
		# 	raise ValidationError('Game: {} vs {} on {} already exists'.format(self.home_team, self.away_team, self.date))



#class Player(Model):
