#!/usr/bin/env python3

#######################################
## Sources:
## https://www.geeksforgeeks.org/python-program-crawl-web-page-get-frequent-words/
##
## https://albertauyeung.github.io/2018/06/03/generating-ngrams.html
##
##


import requests
from bs4 import BeautifulSoup
# import selenium
import operator
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def crawl(url):
    ngram_lenght = 3
    wordlist = []
    source_code = requests.get(url).text

    soup = BeautifulSoup(source_code, 'html.parser')
    for each_text in soup.findAll('p'):  # this will just take things between <p> and </p>
        content = each_text.text
        content = clean_text(content)
        content = remove_common_phrases(content)
        print(content)
        tmp_ngrams = generate_ngrams(content, ngram_lenght)
        for ngram in tmp_ngrams:
            ngram = ngram.replace("\n", "")
            ngram = ngram.replace("\t", "")
            #            ngram = remove_common_phrases(ngram)
            #            print(len(ngram))
            if len(ngram) > ngram_lenght:
                wordlist.append(ngram)
    print(wordlist)
    ngram_counts(wordlist)
    find_links(soup)


def remove_common_phrases(text):
    common_phrases = ['for more information', 'see']
    for phrase in common_phrases:
        text = text.replace(phrase, "")
    return text


def find_links(html_soup):
    for a in html_soup.find_all('a', href=True):
        if a['href'][:28] == 'https://docs.aws.amazon.com/':
            print(a['href'])

        #### Notes:


#### The same meaning 'amazon elastic container service', 'amazon ECS', 'ECS'
#### 'ec2', 'amazon ec2'


# remove unwanted symobols and makes everything lowercase
def clean_text(s):
    # Convert to lowercases
    s = s.lower()

    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    #    for i in ['\n','\t']:
    #        s = s.replace(i,' ')

    return s


import re


def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()

    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


# remove unwanted symobols, stop words and lemmatinazed the words (plurals to singulars etc.)
def clean_words(wordlist):
    clean_list = []
    stoplist = stopwords.words('english')
    print(stoplist)
    for word in wordlist:
        if word not in stoplist:
            clean_list.append(lemmatizer.lemmatize(word))
    return clean_list


def ngram_counts(ngram_list):
    ngram_count = {}

    for ngram in ngram_list:
        if ngram in ngram_count:
            ngram_count[ngram] += 1
        else:
            ngram_count[ngram] = 1

    c = Counter(ngram_count)

    # returns the most occurring elements
    top = c.most_common(10)
    print(top)


# Driver code
if __name__ == '__main__':
    #    url = "https://www.geeksforgeeks.org/programming-language-choose/"
    #    url = "https://docs.aws.amazon.com"
    url = "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"
    # starts crawling and prints output
    crawl(url)