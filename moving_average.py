import matplotlib.pyplot as plt
import numpy as np

from IPython.core.debugger import Tracer

from data_access import get_season_games_for_team

# plt.plot([1,2,3,4])
# plt.show()

def assert_ordered_games(games):
	previous = None
	for g in games:
		if previous is None:
			previous = g
			continue
		else:
			assert g.date > previous.date
		previous = g



def update_wins(win, team, gl):
	if gl.home_team == team:
		if gl.home_win:
			return win+1
		else:
			return win
	else:
		if gl.home_win:
			return win
		else:
			return win+1


def main():
	
	team = 'BOS'
	games = get_season_games_for_team(season='2015-16', team=team)
	games = sorted(games, key=lambda x: x.date)
	assert_ordered_games(games)
	win_points = [0]
	wins = 0
	for g in games:
		wins = update_wins(wins, team, g)
		win_points.append(wins)

	plt.scatter(x=[i for i in range(0,len(win_points))], y=win_points)
	plt.show()
	Tracer()()



main()