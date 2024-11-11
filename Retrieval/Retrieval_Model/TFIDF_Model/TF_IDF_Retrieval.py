from math import log
import json
import codecs
from collections import OrderedDict
import operator
from utilities.query_parser import parse_query
from os import path

# global variables
query_counter = 0
term_count_in_doc = {}
document_freq = {}
uni_index = {}
total_docs = 0
cosine_val = {}
queries = []
query_vector = {}
documentVector = {}
IDF = {}
magnitude_query_vector = 0
magnitude_doc = {}

# Dictionary to store the values in
# key: QueryID
# values: [docID, scores]
results = dict()


# query_file_name = path.join(path.pardir, path.pardir,
#                             "Stemming_and_Stopping", "Stopping", "stopped_queries.txt")
query_file_name = path.join(path.pardir, path.pardir,
                            path.pardir, "utilities", "queries.txt")
try:
    print(path.abspath(query_file_name))
    for line in codecs.open(query_file_name, 'r', encoding="utf-8"):
        ln = line.strip('\r\n')

        ln = ln.lower()
        if ln:
            queries.append(ln)
except Exception as e:
    print(e.args)
    exit(-2)


def load_files():
    global term_count_in_doc
    global document_freq
    global uni_index
    # doc name - number of terms in that document
    try:
        # p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
        #                   "Stopped_Inverted_Index", "docs_term_freq.json")
        p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
                          "Digit_Stemmed_Inverted_Index", "docs_term_freq.json")
        with open(p, 'r') as doc_dict:
            term_count_in_doc = json.load(doc_dict)
    except FileNotFoundError:
        print("File containing document length and average document length "
              "information not found.")

    # term - number of docs in which the term occurs
    try:
        # p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
        #                   "Stopped_Inverted_Index", "uni_gram_df.json")
        p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
                          "Digit_Stemmed_Inverted_Index", "uni_gram_df.json")
        with open(p, 'r') as uniDf:
            document_freq = json.load(uniDf)
    except FileNotFoundError:
        print("File containing document frequency not found .")

    # term - document in which it appears along with the count -unigram index
    try:
        # p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
        #                   "Stopped_Inverted_Index", "uni_dict.json")
        p = p = path.join(path.pardir, path.pardir, path.pardir, "Indexes",
                          "Digit_Stemmed_Inverted_Index", "uni_dict.json")
        with open(p, 'r') as unidict:
            uni_index = json.load(unidict)
    except FileNotFoundError:
        print("File containing unigram index not found.")


# get frequency of particular term in particular doc
def get_term_freq_in_doc(term, doc):
    global uni_index
    found = 0
    freq_in_doc = 0

    if doc != '':
        for x in uni_index[term]:
            if x[0] == doc:
                freq_in_doc = x[1]

                found = 1
                break
        if found == 0:
            freq_in_doc = 0
        term_freq = freq_in_doc / term_count_in_doc[doc]
        return term_freq
    else:
        return 0


# calculates tf.idf for every term of the corpus in a particular doc - doc vector
def generate_doc_vector(doc):
    global uni_index
    global documentVector
    global magnitude_doc
    v_sum = 0
    documentVector[doc] = {}
    for term in uni_index:
        s = get_term_freq_in_doc(term, doc) * IDF[term]
        documentVector[doc][term] = s

    # calculate the magnitude of document vector soon after generating the vector
    for term in documentVector[doc]:
        v_sum = v_sum + (documentVector[doc][term] ** 2)

    # magnitude is square root of sum of squares
    magnitude_doc[doc] = (v_sum ** 0.5)


# for every doc in the corpus, generates the document vector
def generate_document_vectors():
    global term_count_in_doc
    counter = 0
    l = len(term_count_in_doc)
    for doc in term_count_in_doc:
        if doc != '00_avdl_00' and doc != '':
            counter = counter + 1
            if counter == l * 0.1:
                print("Processed 10% of the indexer.")
            elif counter == l * 0.3:
                print("Processed 30% of the indexer.")
            elif counter == l * 0.5:
                print("Processed 50% of the indexer.")
            elif counter == l * 0.7:
                print("Processed 70% of the indexer.")
            elif counter == l * 0.9:
                print("Processed 90% of the indexer.")
            elif counter == l-1:
                print("Processing complete.")
            generate_doc_vector(doc)


# creates the query vector for a given query
def generate_query_vector(query):
    global query_vector
    global magnitude_query_vector
    query_vector = {}
    q_terms = parse_query(query)
    num_terms = len(q_terms)
    q_terms_count = {}

    # get the count of every term in a query
    for term in q_terms:

        if term in q_terms_count:
            q_terms_count[term] = q_terms_count[term] + 1
        else:
            q_terms_count[term] = 1

    # for every unique term in the query
    for term in q_terms_count:
        if term in uni_index:
            query_vector[term] = (q_terms_count[term] / num_terms) * (IDF[term])
        else:
            query_vector[term] = 0
    v_sum = 0
    for term in query_vector:
        v_sum = v_sum + ((query_vector[term]) ** 2)

    magnitude_query_vector = v_sum ** 0.5


def generate_cosine_value(doc):
    global query_vector
    global documentVector
    global cosine_val
    numerator = 0

    for term in query_vector:
        if term in documentVector[doc]:
            numerator = numerator + (query_vector[term] * documentVector[doc][term])

    denominator = (magnitude_doc[doc] * magnitude_query_vector)

    cosine_val[doc] = numerator / denominator


# writes the top 100 documents for every query in separate result file
def get_top_docs():
    global query_counter
    global results

    sorted_docs = sorted(cosine_val.items(), key=operator.itemgetter(1), reverse=True)

    sorted_top100 = OrderedDict(sorted_docs[:100])

    # results[query_counter] = sorted_docs[:100]
    results[query_counter] = sorted_top100

    # rank = 1

    # n = path.join(path.dirname(path.abspath(__file__)), "Stopped_Results.txt")
    n = path.join(path.dirname(path.abspath(__file__)), "Results.txt")
    with open(n, 'a', encoding='utf-8') as file:
        file.write("\nQuery Number " + str(query_counter) + "\n\n")
        # file.write("{0:40} {1:30} {2}\n".format("DOC_ID", "Rank", "Score"))
        # for doc in sorted_top100:
        #     file.write('{0:40} {1:30} {2}\n'.format(str(doc), str(rank), str(cosine_val[doc])))
        #     rank += 1
        file.write("{0:5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
            "Query", "Q0", "Doc_ID", "Rank", "Score", "System Name"))

        rank_counter = 1
        for item in sorted_top100.items():
            file.write("{0:>5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                query_counter, "Q0", item[0], rank_counter,
                round(item[1], 3),
                "TFIDF_1Grams"))
            # file.write('{0:40} {1}\n'.format(item[0], item[1]))
            rank_counter += 1


# computing the idf of all terms in the index beforehand
def get_term_idf():
    global IDF
    global total_docs
    global document_freq
    total_docs = len(term_count_in_doc)
    for term in uni_index:
        IDF[term] = log(total_docs / document_freq[term][1])


# reads every query from the file and gets result for it
def get_all_queries():
    # global file_top100
    global magnitude_query_vector
    global query_counter
    global query_file_name
    global query_vector
    global cosine_val
    global queries
    global results

    try:
        for query in queries:
            query_counter += 1
            query_vector = {}
            magnitude_query_vector = 0
            cosine_val = {}
            generate_query_vector(query)
            for doc in term_count_in_doc:
                if doc != '00_avdl_00' and doc != '':
                    generate_cosine_value(doc)
            get_top_docs()

        # with open("Stopped_TFIDF_results.json", 'w+') as f:
        with open("TFIDF_results.json", 'w+') as f:
            json.dump(results, f)
        print("Result generated for all the 64 queries.")

    except FileNotFoundError:
        print("Query file not found.")


# Driver Function Calls
print("Loading Modules...")
load_files()
get_term_idf()
generate_document_vectors()
print("Processing Queries.")
get_all_queries()
