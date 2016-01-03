import csv
import string
import re
from collections import Counter

def clean_text(field):
    return item[field].lower().translate(string.maketrans("",""), string.punctuation).replace("\n", " ")


prepositions = [" at ", " in ", " on ", " by ", " near ", " across ", " around ", " behind ", " in front of "]

ignore_words = ["", "the", "you", "i", "and", "when", "on", "a", "me", "or", "for", "of", "your", "at", "my", "in", "we", "to", "with", "this", "that", "was", "were", "but", "see", "is", "front", "what", "from", "around", "here", "back", "front", "it", "if", "just", "would", "have", "some", "had", "today", "each", "other", "are", "as", "m4w", "w4m", "m4m", "w4w", "love", "so", "maybe", "night" ]

# Load data into a list of dictionaries for every entry
f = open("cl_mis_ca.csv", "rb")
infile = csv.DictReader(f)
craigs = []
for line in infile:
    craigs.append(line)
f.close()


for item in craigs:
    # Make everything lowercase, remove punctuation and line breaks
    text_field = clean_text('text')
    post_title = clean_text('title')
    all_fields = text_field + " " + post_title
    tokens = []
    
    # Get six words that come after every preposition in the entry
    for prep in prepositions:
        if prep in all_fields:
            before, keyword, after = all_fields.partition(prep)            
            locations = after.split(" ")[:6]
            
            # Check for variations of Tim Horton's and standardize
            for location in locations:
                if re.match(r"tim(mie)?(s)?", location):
                    locations[locations.index(location)] = "tim"
             
            # Remove the ignore words from the list   
            for word in ignore_words:
                if word in locations:
                    locations.remove(word)
            tokens.extend(locations) 
              
    # Remove all duplicate words from and add to list for each entry                
    item['tokens'] = list(set(tokens))

city_tokens = {}

# Add possible locations as a list for each city in a dictionary
for item in craigs:
    if item['city'] in city_tokens:
        city_tokens[item['city']].extend(item['tokens'])
    else:
        city_tokens[item['city']] = item['tokens']
 
# Print to stdout the 10 most common words for every city
with open("results2.txt", "w") as outfile:
    for city, words in city_tokens.iteritems():
        top_results = Counter(words).most_common(10)
        print city + "\t" + "\t".join([i[0]+"\t"+str(i[1]) for i in top_results if i[1] > 4])
        outfile.write(city + "\t" + "\t".join([i[0]+"\t"+str(i[1]) for i in top_results if i[1] > 4]) + "\n" )