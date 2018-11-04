'''This program scrapes data from the Washington Trails Association (WTA) site. For each hike listed 
on the site, it finds the name of the hike and basic statistics on the hike, then saves this 
data to a CSV file.'''

from lxml import html
import pandas as pd
import requests
import sqlite3

page_url = 'https://www.wta.org/go-outside/hikes?b_start:int=0'

def main():
	main_html = url_parse(page_url)[2]

	#Connect to database
	print('Connecting to database...')
	db = sqlite3.connect('db/hikes.db')
	c = db.cursor()

	#Generates list of links for all pages with hikes on them
	print('Collecting links...')
	link_elem = main_html.xpath('//nav[@class="pagination"]')
	last_num = int(link_elem[0].xpath('.//li[@class="last"]')[0].xpath('.//a/text()')[0])

	links = []
	for i in range(last_num):
		links.append('https://www.wta.org/go-outside/hikes?b_start:int=' + str(30*i))

	#Data structure initialization
	names = []
	areas = []
	lengths = []
	gains = []
	highs = []
	count = 1
	print('Running...')

	#Data collection
	for link in links:
		main_html = url_parse(link)[2]
		hike_elem = main_html.xpath('//div[@class="search-result-item"]')
		for elem in hike_elem:
			name_elem = elem.xpath('.//a[@class="listitem-title"]')
			names.extend(name_elem[0].xpath('.//span/text()'))

			area = elem.xpath('.//h3[@class="region"]/text()')
			if len(area) > 0:
				area = area[0].replace('-','').split('  ')
				if len(area) < 3:
					for i in range(3 - len(area)):
						area.append(None)
			else:
				area = (None, None, None)
			areas.append(area)

			stat_elem = elem.xpath('.//div[@class="hike-stats alpha"]')
			length = stat_elem[0].xpath('.//div[@class="hike-length hike-stat"]')
			if len(length) == 0:
				lengths.append(None)
			else:
				lengths.append(length[0].xpath('.//span/text()')[0].split(' ')[0])

			gain = stat_elem[0].xpath('.//div[@class="hike-gain hike-stat"]')
			if len(gain) == 0:
				gains.append(None)
			else:
				gains.append(gain[0].xpath('.//span/text()')[0].split(' ')[0])

			high = stat_elem[0].xpath('.//div[@class="hike-highpoint hike-stat"]')
			if len(high) == 0:
				highs.append(None)
			else:
				highs.append(high[0].xpath('.//span/text()')[0].split(' ')[0])
		print('Page ' + str(count) + '/' + str(len(links)) + ' done.', end='\r')
		count = count + 1

	#Data consolidation
	d = list(zip(names, [i[0] for i in areas], [i[1] for i in areas], [i[2] for i in areas], lengths, gains, highs))
	df = pd.DataFrame(data=d, columns=['Name', 'Region', 'Area', 'Sub-area', 'Length', 'Gain', 'Max Elevation'])

	#Data output
	for row in d:
		write_sql(db, row)
	db.commit()
	db.close()
	print('Data saved to db/hikes.db')

	df.to_csv('data.csv')
	print('Data saved to \'data.csv\'')

#Generates html for xpathing
def url_parse(url):
	response = requests.get(url, timeout=30) #Timeout after 30s
	source = response.text
	html_list = html.fromstring(source)

	return response, source, html_list

#Takes data and inputs it into database
def write_sql(conn, datachunk):
	c = conn.cursor()
	hike = ''' INSERT INTO hikes(name, region, area, subarea, length, gain, max_elevation) 
	VALUES (?, ?, ?, ?, ?, ?, ?) '''
	c.execute(hike, datachunk[0:7])

if __name__ == '__main__':
	main()