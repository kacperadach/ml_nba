from options import TEAM_ABBR


MISSING_NAMES = {
	'Loy Vaught': ['1995-96', TEAM_ABBR['BKN'], 'Regular Season'],
	'Robert Werdann': ['1990-91', TEAM_ABBR['LAC'], 'Regular Season']
}


def get_missing_name(season, season_type, team):
	for key, value in MISSING_NAMES.items():
		if value[0] == season and value[1] == team and value[2] == season_type:
			print 'Replaced Name with {}'.format(key)
			return key
	print 'No replacement name found for {} - {} - {}'.format(season, season_type, team)
	return None



# if season == '1995-96' and team == TEAM_ABBR['BKN'] and season_type == 'Regular Season':
			# 	name = 'Robert Werdann'
			# 	row = ['Robert', 'Werdann'] + row
			# 	print 'Replaced Name with Robert Werdann'
			# elif season == '1990-91' and team == TEAM_ABBR['LAC'] and season_type == 'Regular Season':
			# 	name = 'Loy Vaught'
			# 	row = ['Loy', 'Vaught'] + row
			# 	print 'Replaced Name with Loy Vaught'
			# else:
			# 	Tracer()()


# 1990-91 SUNS - Kurt Rambis 26 minutes