import uuid
from datetime import datetime

from cassandra.cqlengine.columns import UUID, Text, DateTime, Float
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError


# PLAYER TEAM DATE MATCHUP W/L MIN PTS FGM FGA FG% 3PM 3PA 3P% FTM FTA FT% OREB DREB REB AST STL BLK TOV PF +/-

class PlayerGameLog(Model):
	id = UUID(primary_key=True, default=uuid.uuid4)
	player = Text(required=True)
	date = Date(primary_key=True, clustering_order="DSC")
	matchup = Text(required=True)
	wl = Text(required=True)
	minutes = Integer()
	points = Integer()
	fgm = Integer()
	fga = Integer()
	fgp = Float()
	tm = Integer() # three's made
	ta = Integer() # three's attempted
	tp = Float()  # three percentage
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






class CurrencyPair(Model):
    id = UUID(primary_key=True, default=uuid.uuid4)
    base = Text(required=True)
    counter = Text(required=True)

    def validate(self):
        super(CurrencyPair, self).validate()
        if self.base not in CURRENCIES or self.counter not in CURRENCIES:
            raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))


class CurrencyPairValue(Model):
	base = Text(primary_key=True, required=True)
	counter = Text(primary_key=True, required=True)
	date = DateTime(primary_key=True, clustering_order="ASC")
	open = Float()
	close = Float()
	high = Float()
	low = Float()
	volume = Float()

	def validate(self):
		super(CurrencyPairValue, self).validate()
		if self.base not in CURRENCIES or self.counter not in CURRENCIES:
		    raise ValidationError('Invalid Currency Pair: {}/{}'.format(self.base, self.counter))
