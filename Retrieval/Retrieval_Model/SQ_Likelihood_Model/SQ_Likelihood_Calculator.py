# Class, whose instance can be used to calculate
# the SQ_Likelihood_Model scores for the uni-gram
# index of the corpus.
import json
import math
from os import path, remove
from operator import itemgetter
from utilities.query_parser import parse_query
from collections import OrderedDict


class SQLikelihoodCalculator:
    # Class Variables
    term_freq_dict = dict()
    term_indexer = dict()
    doc_freq = dict()
    likelihood_parameter = 0.35
    result_docs = dict()

    def __init__(self):
        # opening data structures to read data
        try:
            # remove("Results.txt")
            remove("stopped_likelihood_results.txt")
        except Exception as e:
            "do nothing"

        print("Loading Modules...")
        try:
            with open(path.join(path.pardir, path.pardir, path.pardir,
                                "Indexes", "Stopped_Inverted_Index", "uni_gram_tf.json"),
                      'r', encoding='utf-8') as file:
            # with open(path.join(path.pardir, path.pardir, path.pardir,
            #                     "Indexes", "Digit_Stemmed_Inverted_Index", "uni_gram_tf.json"),
            #           'r', encoding='utf-8') as file:
                self.term_freq_dict = json.load(file)
        except FileNotFoundError as e:
            print("Term Frequencies File not found. Encountered following error: " + str(e.errno))

        try:
            with open(path.join(path.pardir, path.pardir, path.pardir,
                                "Indexes", "Stopped_Inverted_Index", "uni_dict.json"),
                      'r', encoding='utf-8') as file:
            # with open(path.join(path.pardir, path.pardir, path.pardir,
            #                     "Indexes", "Digit_Stemmed_Inverted_Index", "uni_dict.json"),
            #           'r', encoding='utf-8') as file:
                self.term_indexer = json.load(file)
        except FileNotFoundError as e:
            print("Indexer File not found. Encountered following error: " + str(e.errno))

        try:
            with open(path.join(path.pardir, path.pardir, path.pardir,
                                "Indexes", "Stopped_Inverted_Index", "docs_term_freq.json"),
                      'r', encoding='utf-8') as file:
            # with open(path.join(path.pardir, path.pardir, path.pardir,
            #                     "Indexes", "Digit_Stemmed_Inverted_Index", "docs_term_freq.json"),
            #           'r', encoding='utf-8') as file:
                self.doc_freq = json.load(file)
        except FileNotFoundError as e:
            print("Document Frequency File not found. Encountered following error: " + str(e.errno))

        # for key in self.doc_freq:
        #     self.result_docs[key] = 0

        print("Modules Loaded.\n")

    # Function which calculates the likelihood score
    # for each document
    def calculate(self, query):
        # # Tokenize the Query
        # query_list = query.split()

        # Reiterate through the documents and
        # for each token, find likelihood scores.

        # for |C| calculation
        total_terms_in_corpus = sum(self.doc_freq.values())

        try:
            for doc in self.doc_freq.keys():
                if doc == '':
                    continue
                doc_score = 0
                for term in query:
                    term_freq_per_doc = 0
                    # |D| calculation
                    total_term_per_doc = self.doc_freq[doc]

                    # C(q, i) calculation
                    try:
                        total_term_collection_freq = self.term_freq_dict[term]

                        # f(q, i) calculation
                        doc_list = self.term_indexer[term]
                        for item in doc_list:
                            if item[0] == doc:
                                term_freq_per_doc += item[1]

                        score = (((1 - self.likelihood_parameter) * (term_freq_per_doc / total_term_per_doc))
                                 + self.likelihood_parameter * (total_term_collection_freq / total_terms_in_corpus))

                        doc_score += math.log(score)
                    except KeyError:
                        doc_score += 0

                # add the document score value to the resultant list
                self.result_docs[doc] = doc_score
        except KeyError as e:
            print("\nEither term or document key not found: " + str(e.args[0]).capitalize())

    # function which reads the query and prints the top 100
    # results to a text file.
    def reader(self, query_file_name):
        query = ""
        query_counter = 1

        # Dictionary to store the values in
        # key: QueryID
        # values: [docID, scores]
        results = dict()

        with open(query_file_name, 'r', encoding='utf-8') as q_file:
            for line in q_file:
                query = line
                s = query
                # parse the input
                query = parse_query(query)
                # send it to the searcher
                self.calculate(query)

                l = len(self.result_docs)
                result_set = sorted(self.result_docs.items(), key=itemgetter(1), reverse=True)

                g = path.join(path.dirname(path.abspath(__file__)), "stopped_likelihood_results.txt")
                # g = path.join("Results.txt")

                top_result_set = OrderedDict(result_set[:100])

                with open(g, 'a', encoding='utf-8') as file:
                    file.write("\nResults for Query: " + s + "\n\n")
                    file.write("{0:5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                        "Query", "Q0", "Doc_ID", "Rank", "Score", "System Name"))

                    rank_counter = 1
                    for item in top_result_set.items():
                        file.write("{0:>5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                            query_counter, "Q0", item[0], rank_counter,
                            round(item[1], 3),
                            "Smoothed_Query_Likelihood_Model_Stopped_with_1Grams"))
                        # file.write('{0:40} {1}\n'.format(item[0], item[1]))
                        rank_counter += 1

                self.result_docs.clear()
                print("Output generated for Query-" + str(query_counter))
                # results[query_counter] = result_set
                results[query_counter] = top_result_set
                query_counter += 1

        with open("sq_likelihood_stopped_baseline_results.json", "w+", encoding='utf-8') as file:
        # with open("sq_likelihood_baseline_results.json",
        #           "w+", encoding='utf-8') as file:
            json.dump(results, file)


# Driver Program
if __name__ == '__main__':
    obj = SQLikelihoodCalculator()
    query_f_name = path.join(path.pardir, path.pardir, "Stemming_and_Stopping", "Stopping", "stopped_queries.txt")
    # query_f_name = path.join(path.pardir, path.pardir, path.pardir,
    #                          "utilities", "queries.txt")
    obj.reader(query_f_name)
