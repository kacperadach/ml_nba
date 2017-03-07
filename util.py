def get_seasons_from_str(season):
	try:
		sp = season.split('-')
		first = int(sp[0])
		if int(sp[1]) < 80:
			second = int('20' + sp[1])
		else:
			second = int('19' + sp[1])
		return first, second
	except Exception as e:
		print 'Invalid season provided: {}'.format(season)
		raise e
