from bs4 import BeautifulSoup as bs
import requests
import re
import unicodecsv

cl_site = "http://www.craigslist.org/about/sites"

def main():

	main_index = requests.get(cl_site)
	index_soup = bs(main_index.text)
	index_links = index_soup.find_all('a', href=True)

	# Ignore links to country sections and footer links
	for link in index_links[7:-7]:
	
		city = link.string.title()
	
		mis_url = link.get('href')
		mis_index = requests.get(mis_url + "/search/mis")
	
		# Get state and country from JavaScript: var areaCountry and areaRegion
		re_pattern = r'"([A-Z]*)"'
		region_start = mis_index.text.find("areaRegion =")
		region_end = mis_index.text.find(";", region_start)
		region_code = mis_index.text[region_start:region_end]
		region = re.search(re_pattern, region_code).group(1)
	
		country_start = mis_index.text.find("areaCountry =")
		country_end = mis_index.text.find(";", country_start)
		country_code = mis_index.text[country_start:country_end]
		country = re.search(re_pattern, country_code).group(1)
	
		# Get links to local missed connection ads.
		# Local entries have format "/mis/4903457924.html".
		# Get only links that follow this pattern.
	
		mis_soup = bs(mis_index.text)	
		links_div = mis_soup.find('div', class_ = 'content')
		mis_links = links_div.find_all('a', class_ = 'hdrlnk')
		for mis_link in mis_links:
			if mis_link.get('href').startswith("/mis/"):
				mis_url = mis_link.get('href')
				post_title = mis_link.string
				try:
					cat_pattern = r'([mwt]+4[mwt]+)$'
					post_cat = re.search(cat_pattern, post_title).group()
				except:
					continue
				location = parse_text(link + mis_url)
			else:
				continue
			# Write to CSV the country, region, city, title, category, and post location of each post			
	
def parse_location(mis_url):
	mis_article = requests.get(mis_url)
	post_soup = bs(mis_article.text)
	post_text = post_soup.find(id="postingbody").string
	
	# If post language is not English, use Google Translate API
	

	return post_location


def translate_post():


def write_csv():


if __name__ == "__main__": 
   main()
