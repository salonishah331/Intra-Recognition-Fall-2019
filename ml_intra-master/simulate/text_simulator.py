# Text simulator
# Takes in a series of files and recombines them into a random
# text.


# Parameters:
#   -J: A file of jokes
#   -K: A file of non-jokes
#   -n: The number of sentences used in the the final text
#   -p: The percentage of jokes
#   -o: Output file name


import sys
import random
import re
from optparse import OptionParser

def setParser():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-J", "--jokes",
                      default=None,
                      help="File of jokes, one joke on each line")
    parser.add_option("-K", "--nonjokes",
                      default=None,
                      help="File of non-jokes, one non-joke on each line",)

    parser.add_option("-s", "--size",
                      type="int",
                      default=100,
                      help="Number of lines in new text")

    parser.add_option("-p", "--percent",
                      type="float",
                      default=0.5,
                      help="Proportion of the text to be made up of jokes (ex. 0.5 = 50% of the text will be made up of jokes")

    parser.add_option("-o", "--output",
                      default="output.txt",
                      help="Output filename of simulated text")

    parser.add_option("-l", "--labels",
                      default="labels.txt",
                      help="Output filename of labels of jokes and non-jokes. Index i refers to the ith sentence")
    return parser
#####

def sentencePrep(sentence):

    if len(sentence) < 1:
        return None, None

    iD, sentence = sentence.split(",", 1) # csv format
    sentence = sentence.strip('" ') # disadvantage is that you can't use punctuation to get semantic meaning...
    # Add punctuation
    if sentence[-1] not in ["!", ".", "?"]:
        sentence += "."
    #####

    return iD, sentence
#####



def main():

    parser = setParser()
    (options, args) = parser.parse_args()

    print(options)

    jokes_file = options.jokes
    nonjokes_file = options.nonjokes
    size = options.size
    percent = options.percent

    print(jokes_file)


    # Get all the sentences

    jokes_list = [line.strip() for line in open(jokes_file, "r")]
    nonjokes_list = [line.strip() for line in open(nonjokes_file, "r")]

    # Check that there are enough sentences to make desired length/proportioned text
    # TO-DO: Should I just reuse sentences?

    if len(jokes_list) < size * percent:
        sys.stderr.write("Not enough jokes to make a new file with %d lines with %0.2f proportion of jokes.\n" % (size, percent))
        assert False

    if len(nonjokes_list) < size * (1 - percent):
        sys.stderr.write("Not enough nonjokes to make a new file with %d lines with %0.2f proportion of nonjokes.\n" % (size, 1 - percent))
        assert False



    # Shuffle lists
    random.shuffle(jokes_list)
    random.shuffle(nonjokes_list)



    # Label which sentences are added in
    indices = {}
    true_proportion = 0

    delimiters = '!', '.', '?'
    regexPattern = '|'.join(map(re.escape, delimiters))

    with open(options.output, "w") as fh:

        i = 0
        while i < size:

            # Pick a random number from 0 - 1
            x = random.uniform(0,1)

            if x <= percent:
                # If it falls under percent, add a random joke
                iD,joke = sentencePrep(jokes_list.pop())

                # Parse the joke or sentences into individual sentences
                if joke != None:
                    fh.write(joke + " ")
                    s = 0
                    indices[i] = ("J", iD)
                    numSentences = len(re.split(regexPattern, joke))
                    i += numSentences
                    true_proportion += numSentences
                #####


            else:
                # If it falls above percent, add a random non-jokes
                iD, nonjoke = sentencePrep(nonjokes_list.pop())

                # Parse the joke or sentences into individual sentences
                if nonjoke != None:
                    s = 0
                    fh.write(nonjoke + " ")
                    indices[i] = ("N", iD)
                    numSentences = len(re.split(regexPattern, nonjoke))
                    i += numSentences
                #####
            #####
        #####
    #####

    # print(indices)

    with open(options.labels, "w") as gh:

        for iD in indices:
            label = indices[iD]
            gh.write("%d\t%s\t%s\n" % (iD, label[0], label[1]))
        print("%0.5f" % (true_proportion / float(size)))



















if __name__ == '__main__':
    main()