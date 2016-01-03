from bs4 import BeautifulSoup as bs
import requests
import re
import unicodecsv
import time


# Initiate the CSV

cl_site = "http://www.craigslist.org/about/sites"
f = open("cl_mis_ca.csv", "w+")
writer = unicodecsv.writer(f)
writer.writerow(["city","category","title","text"])


def main():

    main_index = requests.get(cl_site)
    index_txt = main_index.text
    
    # Get only Canadian cities
    start = '<h1><a name="CA">'
    end = '<h1><a name="EU">'
    index_ca = index_txt[index_txt.find(start):index_txt.find(end)]
    index_soup = bs(index_ca, "lxml")
    index_links = index_soup.find_all('a', href=True)
    time.sleep(8)

    for link in index_links:   
        city = link.string.strip().title()   
        city_url = link.get('href')
        mis_index = requests.get(city_url + "/search/mis")
        
        print " "
        print "GETTING DATA FOR " + city
        
        mis_soup = bs(mis_index.content, "lxml")       
        try: 
            total_items = int(mis_soup.find('span', class_='totalcount').string)
        except:
            continue
        
        # Skip cities with fewer than 20 ads
        if total_items < 20:
            continue        
        print "Total ads found: %s" % total_items
        
        scrape_page(mis_soup, city, city_url)
        
        # Paginate if more than one page of results
        if total_items <= 100:
            continue
        else:   
            time.sleep(5)
            page = 100
            while page <= round(total_items, -2):
                mis_index = requests.get(city_url + "/search/mis?s=" + str(page))
                mis_soup = bs(mis_index.content, "lxml")
                scrape_page(mis_soup, city, city_url)
                page = page + 100
       
 
def scrape_page(mis_soup, city, city_url):
    # Get links to local missed connection ads.    
    mis_links = mis_soup.find_all('a', class_ = 'hdrlnk')
    for mis_link in mis_links:
        
        # Toronto and Vancouver have neighbourhood sub-domains
        if city == "Toronto" or city == "Vancouver":
            mis_url = mis_link.get('href')
            post_title = mis_link.string
        else:
            if mis_link.get('href').startswith('/mis/'):          
                mis_url = mis_link.get('href')
                post_title = mis_link.string           
        try:
            cat_pattern = r'([mwt]+4[mwt]+)$'
            post_cat = re.search(cat_pattern, post_title).group()
        except:
            continue
        print "   " + post_title[:25] + "..."
        post_text = get_post_text(city_url + mis_url)
        
        # Write to CSV the city, title, category, and post location of each post        
        writer.writerow([city, post_cat, post_title, post_text])
    time.sleep(8)
    
def get_post_text(mis_url):
    # Goes to each entry and gets the text content
    time.sleep(5)
    mis_article = requests.get(mis_url)
    post_soup = bs(mis_article.content, "lxml")
    post_text = post_soup.find(id="postingbody").get_text().strip()    
    return post_text

if __name__ == "__main__": 
   main()
   
f.close()
   