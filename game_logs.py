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

CHROMEDRIVER = '/home/kacper/apps/chromedriver/chromedriver'

BASE_URL = 'http://stats.nba.com/search/player-game'

stat_table_label = '.nba-stat-table'
run_button_label = '.run-it'
close_stat_filter_label = '.close'
stat_filter_label = '.inner'
season_button_label = '.multiselect-info'
season_options_label = '.multiselect-box__option'
pagination_button_label = '.querytool-pagination__more'

def read_game_logs(season):
    driver = get_page_driver(BASE_URL)
    #soup = BS(driver.page_source, 'html.parser')
    close_stat_filter(driver)
    select_season(driver, season)
    press_run_button(driver)
    open_all_logs(driver)
    rows = get_table_rows(driver)
    if rows and len(rows) > 1:
    	pickle.dump(rows, open('{}.p'.format(season), 'wb'))

def get_table_rows(driver):
	table = driver.find_element_by_css_selector(stat_table_label)
	rows = table.find_elements_by_tag_name('tr')
	rows = filter(lambda x: x.text != '', rows)
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
	#driver = webdriver.Chrome()
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
		print 'Season {}'.format(season)
		#read_game_logs('2016-17')
		try:
			read_game_logs(season)
		except TimeoutException:
			pass
		first = first + timedelta(366)
		second = second + timedelta(366)
