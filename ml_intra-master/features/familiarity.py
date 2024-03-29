# -*- coding: utf-8 -*-
"""familiarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eGV8w_EFS2l8iJbTn6fCwTJXMMEJHtV9

# Measuring familiarity from Google Trends Data

Takes in a sentence, parses relevant words or phrases, and then calculates a score that reflects the probability that a random US resident would be familiar with what the sentence was talking about.

Familiarity will be defined as the likelihood that a given person or audience has enough background knowledge to understand a joke
"""

# Import data

# from google.colab import files
# uploaded = files.upload()


from os.path import isfile
import threading
import subprocess
import time
import numpy as np

# Histogram
def histogram(table, array):
    for i in array:

        try:
            table[i] += 1
        except KeyError:
            table[i] = 1
        ####
    ####

    # for i in table:
    #     print("%d\t%d" % (i, table[i]))



def printHistogram(table):

    for i in range(101):
        try:
            print("%d\t| %s" % (i, "#" * table[i]))

        except KeyError:
            print("%d\t|" % i)


def histgramToFile(table, label, fileName):

    fh = open(fileName, "a")

    for i in range(101):
        try:
            print("%d\t%s\t%s\n" % (i, table[i], label))
            fh.write("%d\t%s\t%s\n" % (i, table[i], label))

        except KeyError:
            print("%d\t0\t%s\n" % (i, label))
            fh.write("%d\t0\t%s\n" % (i, label))
        ####
    ####
    fh.close()
    print("finished writing")

# """# Parsing CSV File"""

fh = open("test.shortjokes.csv", "r")

jokes = {}

for line in fh:
  id_num, joke = line.split(",", 1)
  jokes[id_num] = joke
#####

# Clean sentences
import nltk
nltk.download('punkt')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')


jokes_words = {}

for i in jokes:

    tokens = tokenizer.tokenize(jokes[i])
    jokes_words[i] = [w.lower() for w in tokens if w not in stop_words]
    jokes_words[i] = set(jokes_words[i])
#####



# Call API to retrieve Familiarity information for each word


def run_google_trends(word):

    # print("Retrieving words %s" % word)
    cmd = 'node google_trends_test.js %s' % word
    # print(cmd)
    numbers = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
    # print (word)
    # print (numbers.stdout.readlines()[0])

    return numbers.stdout.readlines()[0]
#####

def familiarity_score(data_arr):

    # Just variance for now
    # print(data_arr)
    return (np.var(data_arr), np.mean(data_arr))

#####


jokes_data = {}
histograms = {}

for i in jokes_words:
    # threads = list()
    count = 0
    jokes_data[i] = {}
    table = {}
    fileName = "joke_%s.histo" % i

    if isfile(fileName):
        print("%s already exists" % fileName)
        assert False
    for word in jokes_words[i]:
        # Get data
        str_data = run_google_trends(word)

        # Parse data
        jokes_data[i][word] = [int(num) for num in str_data.strip().split(",")]

        wordHistogram = {}
        histogram(wordHistogram, jokes_data[i][word])
        histgramToFile(wordHistogram, word, fileName)

        histogram(table, jokes_data[i][word])

        # Track API calls
        count += 1
        if count > 10:
            time.sleep(10)
            count = 0
    #####

    printHistogram(table)
    # assert False



    histograms[i] = table
    time.sleep(10)
#####



# take the variance of the frequencies
# Return the mean of the the scores

for i in jokes_data:
    # Score * frequency
    combined_freq = []

    for j in jokes_data[i]:
        combined_freq += jokes_data[i][j]
    #####
    # print(combined_freq)
    score = familiarity_score(combined_freq)
    print("%s,%d" % (i, score))


# jokes_scores = {}

# # Median
# jokes_median = {}

# # Unfamiliarity score = probability that a random person knows the topic
# # Sum the variances across all the words? Make a base line "normal" as the initial amount
# # But more words would skew longer jokes
# # Average variance for each sentence?

# # Merged frequencies
# jokes_score_freq = {}


# # Calculating variance
# for i in jokes_data:
#     jokes_scores = []
#     jokes_score_freq[i] = []
#     for w in jokes_data[i]:
#         jokes_score_freq[i].append(jokes_data[i][w]) # merging all the data from each word from a single joke
#         score = familiarity_score(jokes_data[i][w])
#         jokes_scores.append(score)
#     #####
#     jokes_median[i] = jokes_scores[len(jokes_data[i]) / 2]
#     jokes_score_freq[i].sort()


# #####

# for i in jokes_median:
#     print(i, jokes_median[i])





# for i in jokes_score_freq:
#     histo = histogram(jokes_score_freq)
#     values = histo.values().sort()
#     for v in values:
#         print("%s\t%s" % (v, histo[v]))




