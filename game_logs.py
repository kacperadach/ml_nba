import os
import requests
import pickle
from bs4 import BeautifulSoup as BS
from selenium import webdriver

from IPython.core.debugger import Tracer

CHROMEDRIVER = '/home/kacper/apps/chromedriver/chromedriver'
os.environ["webdriver.chrome.driver"] = CHROMEDRIVER


BASE_URL = 'http://stats.nba.com/search/player-game'

stat_table_label = 'nba-stat-table'
run_button_label = '.run-it'
close_stat_filter_label = '.close'
stat_filter_label = '.inner'
season_button_label = '.multiselect-info'
season_options_label = '.multiselect-box__option'
pagination_button_label = '.querytool-pagination__more'

SEASON = '2016-17'

def read_game_logs():
    driver = get_page_driver(BASE_URL)
    #soup = BS(driver.page_source, 'html.parser')
    close_stat_filter(driver)
    select_season(driver, SEASON)
    press_run_button(driver)
    open_all_logs(driver)

    Tracer()()
    
    #rows = soup.findChildren('table')[0].findChildren(['th', 'tr'])

def open_all_logs(driver):
	opened = False
	while not opened:
		try:
			press_pagination_button(driver)
			opened = True
		except:
			pass
	while opened:
		try:
			press_pagination_button(driver)
			opened = False
		except:
			pass


def press_pagination_button(driver):
	pagination_button = driver.find_element_by_css_selector(pagination_button_label)
	pagination_button.click()


def close_stat_filter(driver):
	close_button = driver.find_element_by_css_selector(close_stat_filter_label).find_elements_by_css_selector("*")[0]
	close_button.click()

def select_season(driver, season):
	# season should be a string in the format "2016-17"
	season_button = driver.find_element_by_css_selector(season_button_label)
	season_button.click()
	buttons = driver.find_elements_by_css_selector(season_options_label)
	option = None
	for b in buttons:
		if b.text == season:
			option = b
			break
	if option:
		option.click()

def press_run_button(driver):
	run_button = driver.find_element_by_css_selector(run_button_label)
	run_button.click()

def take_screenshot(driver):
	driver.save_screenshot('out.png')

def get_page_driver(url):
	#driver = webdriver.PhantomJS()
    driver = webdriver.Chrome(CHROMEDRIVER)
    driver.get(url)
    return driver

if __name__ == "__main__":
    read_game_logs()