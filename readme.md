# An analyzer of Canadian missed connection ads

These files scrape Craiglist missed connection ads for Canadian cities, find the most common location for each city, and the most common words that follow a given phrase, also for each city.


### craiglist_mis_CA.py
The scraper file. Cities with fewer than 20 ads are ignored. Results are saved to a CSV.

### get_locations.py

Reads the CSV saved by the scraper and finds the most common locations (most frequent words followed by location prepositions like "in", "at", "on" and "behind").

### ngrams.py

`ngrams( word, n=1, top=3 )`

Function that takes as arguments a word or phrase, a number n of words that follow the inputted phrase (default is 1), and the top results (default is top 3). It also work from the CSV saved by the scraper.