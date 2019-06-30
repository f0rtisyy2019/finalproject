from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape():
	base_url = 'https://finance.yahoo.com'

	stocks = ['gainers', 'losers']

	# stock range
	stk_rng = 3

	# initialize empty list and dictionary
	stk_list = []
	stk_dict = {}
	    
	for l in stocks:
	    url = f'{base_url}/{l}'

	    r = requests.get(url)
	    
	    soup = BeautifulSoup(r.text, 'html.parser')
	    
	    table_head = soup.find_all('table')[0].find_all('thead')[0].find_all('tr')[0].find_all('th')
	    
	    # list of columns from yahoo finance table
	    columns = [head.text for head in table_head]

	    for i in range(0,stk_rng):
	        stk_row = soup.find_all('table')[0].find_all('tbody')[0].find_all('tr')[i]

	        stk_data = stk_row.find_all('td')

	        for data in range(0, len(stk_data)):
	            stk_dict[columns[data]] = stk_data[data].text

	        stk_list.append(dict(stk_dict))

	return stk_list

if __name__ == "__main__":
    print(scrape())