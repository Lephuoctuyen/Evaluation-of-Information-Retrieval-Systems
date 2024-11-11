# Script which parses any input string
# and process it into forming a tokens
# in the format imbibed in the indexer
# of this retrieval system
import nltk
import string
import re
from os import path
import codecs

stopwords = []


def getStopWords():
    global stopwords
    p = path.join(path.join(path.pardir, "Material"), "common_words.txt")
    with open(p, "r") as ins:
        for line in ins:
            line = line.strip('\n')
            stopwords.append(line)


def parse_query_rem_stopwords(query):
    global stopwords
    print("in parse query ", query)
    print(stopwords)
    result_query = []
    # Step-1: Convert it into ascii format
    query = query.encode('ascii', 'ignore')

    # Step-2: Decode it using the utf-8 format
    query = query.decode('utf-8', 'ignore')

    # Step-3: Tokenize the words using nltk
    # library
    tokens = nltk.word_tokenize(query)

    # Iterate through the tokens to remove
    # any unrequired punctuation
    for element in tokens:
        element = element.strip(string.punctuation)
        filter_output = re.match(
            '(\w+(\.\w+)+)|(\w+(-\w+)+)+|(\w+(_\w+)+)+|[A-z]+|(\d(-\d+)+)+|(\d(\.\d+)+)+'
            '|(\d(\,\d+)+)+|(\d+:\d+\w+)|\d+|[^_\-,⋅.?:’\')({}\]\[]',
            element)

        if filter_output is not None:
            if (str(filter_output.group().lower()) not in stopwords):
                result_query.append(filter_output.group().lower())

    # return the parsed tokens
    result_query = ' '.join(result_query)
    return result_query


queries = []


def main():
    global queries, stopwords
    getStopWords()
    try:
        p = str(path.join(path.pardir, "queries.txt"))
        for line in codecs.open(p, 'r', encoding="utf-8"):
            ln = line.strip('\r\n')

            ln = ln.lower()
            if ln:
                new_q = parse_query_rem_stopwords(ln)
                print(new_q)
                queries.append(new_q)
        print(queries)
        with open('stopped_queries.txt', 'w+', encoding='utf-8') as stoppedqueryfile:
            for q in queries:
                stoppedqueryfile.write(str(q) + "\n")
    except FileNotFoundError:
        print("Query file not found.")


main()
