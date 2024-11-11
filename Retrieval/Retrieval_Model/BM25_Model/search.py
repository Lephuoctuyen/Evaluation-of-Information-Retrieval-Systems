# A python program which acts as an interface to search and produce
# the results for the search engine

import json
import operator
from os import path, remove
from utilities.query_parser import parse_query
from collections import OrderedDict


# A Class which handles the operations of searching and displaying
# the results. Any other class can use the instance of this class
# to provide search capability using the underlying search engine.
class Search:
    query = ""
    terms = []
    results_dict = {}
    docs_score = []
    pre_processed_score = 0
    term_score_dict = {}
    param_k2 = 100

    def __init__(self):
        # print("Loading Modules...")
        try:
            # remove("results_of_stopped_corp.txt")
            remove("results.txt")
        except Exception as e:
            "do nothig."

        try:

            g = path.join(path.dirname(path.abspath(__file__)), "digit_stemmed_processed_score.json")
            # g = path.join(path.dirname(path.abspath(__file__)), "stopped_processed_score.json")
            with open(g, 'r') as file:
                self.term_score_dict = json.load(file)
            # print("Search Engine ready...")
        except FileNotFoundError:
            print("Pre-processed scores not available. "
                  "Execute preprocessor.py script to generate the "
                  "values.")
            exit(-1)

    # Function which receives the input and processes it.
    def search(self, query):
        # parse the input
        self.query = parse_query(query)

        self.terms = self.query

        self.results_dict = {}

        # Call function to process the scores
        self.process()

        r = sorted(self.results_dict.items(), key=operator.itemgetter(1), reverse=True)
        return r

    # A function which performs the BM25 score calculation
    # for each document
    def process(self):
        # Iterate through each item and find the BM25 score
        # of each document for the entire query.
        for item in self.terms:
            # If the key is in the corpus, find the score
            # Else ignore the score contributed by the key
            # towards the resultant score.
            try:
                self.docs_score = self.term_score_dict[item]
            except KeyError:
                continue

            qf = self.terms.count(item)
            t = (((self.param_k2 + 1) * qf) / (self.param_k2 + qf))

            # Calculating BM25 score for each document the
            # term(in the corpus) is present in.
            for doc in self.docs_score:
                doc_id = doc[0]
                doc_score = doc[1]

                bm25_score = float(doc_score) * t

                try:
                    self.results_dict[doc_id] += bm25_score
                except KeyError:
                    self.results_dict[doc_id] = bm25_score

    # Function which prints the top 100 results
    def print_top_results(self, query_file_name):
        # query_file_name = str(path.join(path.pardir, path.pardir, path.pardir, 'utilities/queries.txt'))
        query_counter = 1

        # Dictionary to store the values in
        # key: QueryID
        # values: [docID, scores]
        results = dict()
        snip_results = dict()

        with open(query_file_name, 'r', encoding='utf-8') as q_file:
            for line in q_file:
                # sort the docs based on the scores
                result_set = self.search(line)

                # print the top 100 results to a file
                filename = "results.txt"
                # filename = "results_of_stopped_corp.txt"

                top_result_set = OrderedDict(result_set[:100])

                with open(filename, 'a', encoding='utf-8') as file:
                    file.write("\nResults for Query: " + line + "\n\n")
                    file.write("{0:5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                        "Query", "Q0", "Doc_ID", "Rank", "Score", "System Name"))

                    rank_counter = 1
                    for item in top_result_set.items():
                        file.write("{0:>5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                            query_counter, "Q0", item[0], rank_counter,
                            round(item[1], 3),
                            "BM25_with_1Grams"))
                        # file.write('{0:40} {1}\n'.format(item[0], item[1]))
                        rank_counter += 1

                print("Output generated for Query-" + str(query_counter))
                results[query_counter] = top_result_set
                snip_results[query_counter] = list(top_result_set)
                query_counter += 1

        with open("bm25_baseline_results.json", "w+", encoding='utf-8') as file:
        # with open("bm25_stopped_baseline_results.json", "w+", encoding='utf-8') as file:
            json.dump(results, file)

        with open("snippet_generation_results.json", "w+", encoding='utf-8') as file:
            json.dump(snip_results, file)


# Driver Program
if __name__ == '__main__':
    obj = Search()
    # print(path.abspath(path.curdir))
    query_f_name = str(path.join(path.pardir, path.pardir, path.pardir, 'utilities', 'queries.txt'))
    # query_f_name = str(path.join(path.pardir, path.pardir,
    #                              "Stemming_and_Stopping", "Stopping",
    #                              "stopped_queries.txt"))

    obj.print_top_results(query_f_name)
