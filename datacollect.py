'''This program scrapes data from the Washington Trails Association (WTA) site. For each hike listed 
on the site, it finds the name of the hike and basic statistics on the hike, then saves this 
data to a CSV file.'''


import pandas as pd
import requests
from lxml import html

page_url = 'https://www.wta.org/go-outside/hikes?b_start:int=0'

def main():
	main_html = url_parse(page_url)[2]

	#Generates list of links for all pages with hikes on them
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
	print("Running...")
	for link in links:
		main_html = url_parse(link)[2]
		hike_elem = main_html.xpath('//div[@class="search-result-item"]')
		for elem in hike_elem:
			name_elem = elem.xpath('.//a[@class="listitem-title"]')
			names.extend(name_elem[0].xpath('.//span/text()'))

			area = elem.xpath('.//h3[@class="region"]/text()')[0]
			area = area.replace('-','').split('  ')
			if len(area) < 3:
				for i in range(3 - len(area)):
					area.append(None)
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
		print('Page ' + str(count) + ' done.', end='\r')
		count = count + 1
	d = zip(names, [i[0] for i in areas], [i[1] for i in areas], [i[2] for i in areas], lengths, gains, highs)
	df = pd.DataFrame(data=d, columns=['Name', 'Region', 'Area', 'Sub-area', 'Length', 'Gain', 'Max Elevation'])
	df.to_csv('data.csv')
	print('Data saved to \'data.csv\'')

#Generates html for xpathing
def url_parse(url):
	response = requests.get(url, timeout=30) #Timeout after 30s
	source = response.text
	html_list = html.fromstring(source)

	return response, source, html_list

if __name__ == '__main__':
	main()