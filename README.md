# ml_nba
Neural Network for NBA games

##Files

**game_logs.py** - Selenium script to get Player Game Logs from http://stats.nba.com/search/player-game/ and save in Pickles dir

**pickle_reader.py** - reads pickles to create PlayerGameLog objects in Cass DB

**game.py** - creates Game objects from PlayerGameLogs and updates records for each game

**player.py** - updates Game objects with associated Players

##HyperParameters

**n_clusters** - in kmeans.py
