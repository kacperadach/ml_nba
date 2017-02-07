import uuid
from datetime import datetime

from cassandra.cqlengine.columns import UUID, Text, DateTime, Float, Date, Integer, Boolean
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError


# PLAYER TEAM DATE MATCHUP W/L MIN PTS FGM FGA FG% 3PM 3PA 3P% FTM FTA FT% OREB DREB REB AST STL BLK TOV PF +/-

class PlayerGameLog(Model):
	name = Text(required=True, primary_key=True)
	team = Text(required=True)
	date = Date(primary_key=True, clustering_order="DESC")
	home = Boolean(required=True)
	opp = Text(required=True)
	win = Boolean(required=True)
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

	def validate(self):
		super(PlayerGameLog, self).validate()


class Game(Model):
	id = UUID(primary_key=True)
	home_team = Text(required=True)
	away_team = Text(required=True)
	date = Date(primary_key=True, clustering_order="ASC")
	outcome = Text(required=True)
	season_type = Text(required=True)

	def validate(self):
		super(Game, self).validate()


#class Player(Model):






# class CurrencyPair(Model):
#     id = UUID(primary_key=True, default=uuid.uuid4)
#     base = Text(required=True)
#     counter = Text(required=True)

#     def validate(self):
#         super(CurrencyPair, self).validate()
#         if self.base not in CURRENCIES or self.counter not in CURRENCIES:
#             raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))


# class CurrencyPairValue(Model):
# 	base = Text(primary_key=True, required=True)
# 	counter = Text(primary_key=True, required=True)
# 	date = DateTime(primary_key=True, clustering_order="ASC")
# 	open = Float()
# 	close = Float()
# 	high = Float()
# 	low = Float()
# 	volume = Float()

# 	def validate(self):
# 		super(CurrencyPairValue, self).validate()
# 		if self.base not in CURRENCIES or self.counter not in CURRENCIES:
# 		    raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))
