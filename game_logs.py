import pickle
from datetime import date, timedelta
import math

from bs4 import BeautifulSoup as BS
from IPython.core.debugger import Tracer

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from options import TEAMS, SEASON_TYPES

CHROMEDRIVER = '/home/kacper/apps/chromedriver/chromedriver'

BASE_URL = 'http://stats.nba.com/search/player-game'

stat_table_label = '.nba-stat-table'
run_button_label = '.run-it'
close_stat_filter_label = '.close'
stat_filter_label = '.inner'
season_button_label = '.multiselect-info'
options_label = '.multiselect-box__option'
pagination_button_label = '.querytool-pagination__more'

def read_game_logs(season, season_type, team):
    driver = get_page_driver(BASE_URL)
    #soup = BS(driver.page_source, 'html.parser')
    close_stat_filter(driver)
    select_options(driver, season, season_type, team)
    press_run_button(driver)
    open_all_logs(driver)
    rows = get_table_rows(driver)
    if rows and len(rows) > 1:
    	pickle.dump(rows, open('{}.p'.format(season), 'wb'))

def get_table_rows(driver):
	table = driver.find_element_by_css_selector(stat_table_label)
	rows = filter(lambda x: x.text != '', table.find_elements_by_tag_name('tr'))
	Tracer()()
	return rows
	
def open_all_logs(driver):
	results_str = driver.find_element_by_css_selector('.querytool-pagination__text').text
	results = int(results_str.split()[3])
	pagination_clicks = int(math.ceil(float(int(results) - 50) / 50))
	for x in range(pagination_clicks):
		print "Pagination Click: {} of {}".format(x+1, pagination_clicks)
		press_pagination_button(driver)

def press_pagination_button(driver):
	pagination_button = driver.find_element_by_css_selector(pagination_button_label)
	pagination_button.click()

def close_stat_filter(driver):
	close_button = driver.find_element_by_css_selector(close_stat_filter_label).find_elements_by_css_selector("*")[0]
	close_button.click()

def select_options(driver, season, season_type, team):
	# season should be a string in the format "2016-17"
	# season_type should be: "Preseason", "Regular Season", "Playoffs", "All Star"
	buttons = driver.find_elements_by_css_selector(season_button_label)
	season_button = buttons[0]
	season_type_button = buttons[1]
	team_button = buttons[2]

	def select(button, val):
		button.click()
		buttons = driver.find_elements_by_css_selector(options_label)
		for b in buttons:
			if b.text == val:
				option = b
				break
		if option:
			option.click()
		button.click()

	select(season_button, season)
	select(season_type_button, season_type)
	select(team_button, team)

def wait_for_load(driver, delay=15):
	try:
		WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, stat_table_label)))
		print 'Data Table Loaded'
	except TimeoutException:
		print '{} second timeout'.format(delay)
		raise TimeoutException

def press_run_button(driver):
	run_button = driver.find_element_by_css_selector(run_button_label)
	run_button.click()
	wait_for_load(driver)

def take_screenshot(driver):
	driver.save_screenshot('out.png')

def get_page_driver(url):
	driver = webdriver.Chrome()
	driver.get(url)
	return driver

def create_year_str(first, second):
	return '{}-{}'.format(first.year, str(second.year)[-2:])

if __name__ == "__main__":

	#1984-85 - 2016-17

	first = date(year=1985, month=1, day=1)
	second = date(year=1986, month=1, day=1)
	while first.year < 2017:
		season = create_year_str(first, second)
		for season_type in SEASON_TYPES:
			for team in TEAMS:
				#read_game_logs('2016-17')
				print "{} - {} - {}".format(season, season_type, team)
				try:
					read_game_logs(season, season_type, team)
				except TimeoutException:
					pass
		first = first + timedelta(366)
		second = second + timedelta(366)
