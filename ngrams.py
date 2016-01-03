import csv
import string
from collections import Counter


def clean_text(raw, field):
    return raw[field].lower().translate(string.maketrans("",""), string.punctuation).replace("\n", " ")
    
# Returns the top 3 words that follow a given word for each city.
def ngrams(word, n=1, top=3):
    with open("cl_mis_ca.csv", "rb") as f:
        f = open("cl_mis_ca.csv", "rb")
        infile = csv.DictReader(f)
        craigs = []
        for line in infile:
            craigs.append(line)
            
        for item in craigs:
            # Make everything lowercase, remove punctuation and line breaks
            text_field = clean_text(item, 'text')
            post_title = clean_text(item, 'title')
            all_fields = text_field + " " + post_title
            tokens = []
    
            if word in all_fields:
                before, keyword, after = all_fields.partition(word)
                after = after.strip()
                after_words = after.split(" ")[:n]
                after_phrase = " ".join(after_words)
                tokens.append(after_phrase) 
            
            item['tokens'] = list(set(tokens))
    
        city_tokens = {}

        # Add possible locations as a list for each city in a dictionary
        for item in craigs:
            if item['city'] in city_tokens:
                city_tokens[item['city']].extend(item['tokens'])
            else:
                city_tokens[item['city']] = item['tokens']
 
        # Print to stdout the 10 most common words for every city
        for city, words in city_tokens.iteritems():
            top_results = Counter(words).most_common(top)
            for i in top_results:
                if i[1] < 2:
                    continue
                print city+"\t" + i[0]+ "\t" + str(i[1])
