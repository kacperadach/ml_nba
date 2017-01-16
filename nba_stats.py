import requests
import pickle
from bs4 import BeautifulSoup as BS
from selenium import webdriver

NBA_DEFENSIVE_STATS_URL = 'http://stats.nba.com/league/team/defense/#!/'
NBA_PLAYER_STATS_URL = 'http://stats.nba.com/league/player/#!/'
PLAYER_PAGES = 9







def get_page_source(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    return driver.page_source

def get_page_rows(soup):
    return soup.find_all('tr')[17:]

def get_team_defensive_stats():
    page_source = get_page_source(NBA_DEFENSIVE_STATS_URL)
    soup = BS(page_source, 'html.parser')
    rows = get_page_rows(soup)
    TeamDefenses = []
    for r in rows:
        tds = r.find_all('td')
        TeamDefenses.append(TeamDefense(
            tds[0].text,
            int(tds[1].text),
            float(tds[4].text),
            float(tds[5].text),
            float(tds[6].text),
            float(tds[7].text),
            float(tds[8].text)))
    with open('team_defenses.p', 'wb') as f:
        pickle.dump(TeamDefenses, f)
    return TeamDefenses

def get_player_stats():
    players = []
    driver = webdriver.PhantomJS()
    driver.get(NBA_PLAYER_STATS_URL)
    for _ in range(PLAYER_PAGES):
        page_source = driver.page_source
        soup = BS(page_source, 'html.parser')
        rows = get_page_rows(soup)
        for r in rows:
            tds = r.find_all('td')
            players.append(Player(
                tds[0].text,
                tds[1].text.split()[0],
                tds[3].text.split()[0],
                tds[6].text.split()[0],
                tds[7].text.split()[0],
                tds[8].text.split()[0],
                tds[9].text.split()[0],
                tds[10].text.split()[0],
                tds[11].text.split()[0],
                tds[12].text.split()[0],
                tds[18].text.split()[0],
                tds[19].text.split()[0],
                tds[20].text.split()[0],
                tds[21].text.split()[0],
                tds[22].text.split()[0],
                tds[26].text.split()[0],
                tds[27].text.split()[0]))
        nav_button = driver.find_element_by_class_name('right')
        nav_button.click()
    with open('players.p', 'wb') as f:
        pickle.dump(players, f)
    return players


if __name__ == "__main__":
    defenses = get_player_stats()
    for d in defenses:
        print d