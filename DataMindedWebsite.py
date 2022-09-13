#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
# import selenium
import operator
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

lemmatizer = WordNetLemmatizer()

# Importing Libraries

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# Importing Dataset


def start(url_list):
    wordlist = []
    content = ""
    for url in url_list:
        source_code = requests.get(url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        for each_text in soup.findAll('p'):
            content = content + " " + each_text.text
    #   print("%%%%% content %%%%% \n", content)

    #    wordlist = generate_ngrams(content, 1)
    #    print("%%%%% wordlist %%%%%% \n ", wordlist)
    #    clean_words(wordlist)

    #    wordlist = generate_ngrams(content, 2)
    #    print("%%%%% wordlist %%%%%% \n ", wordlist)
    #    clean_words(wordlist)
    #    find_links(soup)
    return content


def find_links(html_soup):
    for a in html_soup.find_all('a', href=True):
        #         if a['href'][:28]=='https://docs.aws.amazon.com/':
        print(a['href'])


#        print(a)

# remove unwanted symobols, stop words and lemmatinazed the words (plurals to singulars etc.)


import re


def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()
    print("generate_ngrams: ")
    #    print(s)
    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


# import re
# from nltk.util import ngrams
#
# s = s.lower()
# s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
# tokens = [token for token in s.split(" ") if token != ""]
# output = list(ngrams(tokens, 5))


def clean_words(wordlist):
    clean_list = []
    stoplist = stopwords.words('english')
    common_noinfo_words = ["see"]
    print("%% stoplist %%", stoplist)
    for word in wordlist:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')

        if (len(word) > 0) and (word not in stoplist) and (word not in common_noinfo_words):
            clean_list.append(lemmatizer.lemmatize(word))

    #  clean_list = ' '.join([lemmatizer.lemmatize(w) for w in clean_list])
    create_dictionary(clean_list)


# remove unwanted symobols, stop words
def clean_words_old(wordlist):
    clean_list = []
    stoplist = stopwords.words('english')

    print(stoplist)

    for word in wordlist:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')

        if (len(word) > 0) and (word not in stoplist):
            clean_list.append(word)
    create_dictionary(clean_list)


# remove unwanted symobols
def clean_words_old_old(wordlist):
    clean_list = []

    for word in wordlist:
        symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "

        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')

        if len(word) > 0:
            clean_list.append(word)
    create_dictionary(clean_list)


# Creates a dictionary conatining each word's
# count and top_20 ocuuring words


def create_dictionary(clean_list):
    word_count = {}

    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    ''' To get the count of each word in
        the crawled page -->

    # operator.itemgetter() takes one
    # parameter either 1(denotes keys)
    # or 0 (denotes corresponding values)

    for key, value in sorted(word_count.items(),
                    key = operator.itemgetter(1)):
        print ("% s : % s " % (key, value))

    <-- '''

    c = Counter(word_count)

    # returns the most occurring elements
    top = c.most_common(20)
    print(top)


# def make_world_cloude(
#    word_cloud = WordCloud(collocations = False, background_color = 'white').generate(text)
# )


# Driver code


def get_all_content(start_url, url=None, all_url=[], content=""):
    if url == None:
        url = start_url
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    for each_text in soup.findAll('p'):
        content = content + " " + each_text.text
    #        print(each_text.text)
    for a in soup.find_all('a', href=True):
        link = a['href']
#        print('link', link, 'start_url', start_url)
        if link.startswith(start_url):
 #           print('check ', link, all_url)
            if link not in all_url:
                print('appoved link ', link)
                all_url.append(link)
                content, all_url = get_all_content(start_url, link, all_url, content)
    #               content = content + content1
    #               print('final_url_list1',final_url_list1)
    #          all_url.extend(final_url_list1)

#    print("all_url", all_url)
    return content, all_url


if __name__ == '__main__':
    #    url = "https://www.geeksforgeeks.org/programming-language-choose/"
    #    url = "https://docs.aws.amazon.com"
    #    url = "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"
    url_list = ["https://www.dataminded.com/",
                "https://www.dataminded.com/consulting",
                "https://www.dataminded.com/data-foundations",
                "https://www.dataminded.com/data-democratization",
                "https://www.dataminded.com/conveyor",
                "https://www.dataminded.com/conveyor-product-and-features",
                "https://www.dataminded.com/conveyor-vs-diy",
                "https://www.dataminded.com/conveyor-vs-databrics",
                "https://www.dataminded.com/conveyor-vs-emr",
                "https://www.dataminded.com/academy",
                "https://www.dataminded.com/data-engineering-manifesto",
                "https://www.dataminded.com/dmi",
                "https://www.dataminded.com/cases",
                "https://www.dataminded.com/webinars",
                "https://www.dataminded.com/team",
                "https://www.dataminded.com/join-us",
                "https://www.dataminded.com/cloud-partnerships"
                ]

    url_list1 = ['https://www.dataminded.com',
                 'https://www.dataminded.com/consulting',
                 'https://www.dataminded.com/conveyor',
                 'https://www.dataminded.com/conveyor-product-and-features',
                 'https://www.dataminded.com/conveyor-vs-diy',
                 'https://www.dataminded.com/conveyor-pricing',
                 'https://www.dataminded.com/conveyor-contact',
                 'https://www.dataminded.com/academy',
                 'https://www.dataminded.com/data-engineering-manifesto',
                 'https://www.dataminded.com/dmi',
                 'https://www.dataminded.com/cases',
                 'https://www.dataminded.com/webinars',
                 'https://www.dataminded.com/team',
                 'https://www.dataminded.com/join-us',
                 'https://www.dataminded.com/cloud-partnerships',
                 'https://www.dataminded.com/data-engineers',
                 'https://www.dataminded.com/cases/bics',
                 'https://www.dataminded.com/cases/',
                 'https://www.dataminded.com/cases/luminus',
                 'https://www.dataminded.com/cases/dpg',
                 'https://www.dataminded.com/cases/newpharma',
                 'https://www.dataminded.com/cases/kwarts',
                 'https://www.dataminded.com/conveyor-vs-databrics',
                 'https://www.dataminded.com/conveyor-vs-emr',
                 'https://www.dataminded.com/data-foundations',
                 'https://www.dataminded.com/data-democratization',
                 'https://www.dataminded.com/mlops',
                 'https://www.dataminded.com/cases/luminus-neo']

    # starts crawling and prints output
    # start(url_list)

    # text2 = " ".join(title for title in df.title)

    x = "begin"
    y = "beginend"
    print("test starts with: ", y.startswith(x))
    text1, all_url = get_all_content("https://www.dataminded.com")
    print(text1)
    print(all_url)
    word_cloud1 = WordCloud(collocations=False, background_color='white').generate(text1)
    plt.imshow(word_cloud1, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('DataMindedWordCloud1.png')

    text2 = start(url_list1)
    print("comarison: ", len(text1), len(text2))
    print("url list comparison", len(all_url), len(url_list1))
    print(text2)
#  word_cloud2 = WordCloud(collocations=False, background_color='white').generate(text2)
#  plt.imshow(word_cloud2, interpolation='bilinear')
#  plt.axis("off")
#  plt.savefig('DataMindedWordCloud2.png')
#  # plt.show()
