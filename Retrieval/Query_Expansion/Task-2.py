# This file implements the psuedo-relevance feedback
# for the Query Stemming.
# Create an reference of this class to access the stemmer.
from Retrieval.Retrieval_Model.BM25_Model.search import Search
from utilities.stopwords_parser import stop_word_parser
from os import path, remove
import json
from operator import itemgetter
from collections import OrderedDict


class QueryExpansion:

    # Variables
    stem_query = ""
    obj = None
    tf_dict = dict()
    top_words = list()
    tf_per_doc_dict = dict()

    # Constructor
    def __init__(self):

        try:
            remove("stemmed_baseline_results.txt")
        except Exception as e:
            "do nothing."

        self.obj = Search()

        try:
            p = path.join(path.pardir, path.pardir, "Indexes", "Digit_Stemmed_Inverted_Index", "uni_dict.json")
            # print(k)
            # print(p)
            with open(p, 'r', encoding='utf-8') as file:
                self.tf_dict = json.load(file)
        except FileNotFoundError:
            print("Term frequencies file not found. Processing incomplete. Exiting the program...")
            exit(-1)

        try:
            p = path.join(path.pardir, path.pardir, "Indexes", "Digit_Stemmed_Inverted_Index", "term_freq_per_doc.json")
            with open(p, 'r', encoding='utf-8') as file:
                self.tf_per_doc_dict = json.load(file)
        except FileNotFoundError:
            print("Term frequencies per document file not found. Processing incomplete. Exiting the program...")
            exit(-1)

        p = path.join(path.pardir, path.pardir, "utilities", "stop_words.json")
        try:
            with open(p, 'r', encoding='utf-8') as file:
                self.s_word_dict = json.load(file)
        except FileNotFoundError:
            stop_word_parser()
            with open(p, 'r', encoding='utf-8') as file:
                self.s_word_dict = json.load(file)
            exit(-1)

    # Method which invokes BM25
    def invoke_BM25(self, query):
        return self.obj.search(query)

    # Method which takes the plain query and
    # extends it using stem words based on
    # psuedo-relevance feedback
    def query_expansion(self, query):
        words = []
        # Step-1: Generate the results for the Query
        result_set = self.invoke_BM25(query)

        # Step-2: Select the top 10 documents from the
        # result set and add those to the query.
        for i in range(0, 10):
            # get the top words of the file.
            words.append(self.tf_per_doc_dict[result_set[i][0]])

        # remove stop words from the file.
        words = sorted(words, key=itemgetter(1), reverse=True)
        words = self.remove_stop_words(words)

        self.stem_query = query

        for item in words:
            if item not in self.stem_query:
                self.stem_query += " " + item

        return self.stem_query

    # Method which removes stop-words from the given
    # list of ["word", freq] lists
    def remove_stop_words(self, words):
        return_list = []
        counter = 0
        for i in range(0, len(words)):
            for j in range(0, len(words[i])):
                if words[i][j][0] in self.s_word_dict:
                    continue
                else:
                    # remove duplicates and words which are smaller than 2 characters
                    if words[i][j][0] not in return_list and len(words[i][j][0]) > 2:
                        return_list.append(words[i][j][0])
                        counter += 1

                if counter > 10:
                    break
            if counter > 10:
                break

        return return_list


# Driver Program
if __name__ == '__main__':
    obj = QueryExpansion()
    query_counter = 1

    # Dictionary to store the values in
    # key: QueryID
    # values: [docID, scores]
    results = dict()

    try:
        with open(path.join(path.pardir, path.pardir, "utilities", "queries.txt"), 'r', encoding='utf-8') as file:
            for line in file:
                stemmed_query = obj.query_expansion(line)
                result_set = obj.invoke_BM25(stemmed_query)

                filename = "stemmed_baseline_results.txt"

                top_result_set = OrderedDict(result_set[:100])

                with open(filename, 'a', encoding='utf-8') as file:
                    file.write("\nResults for Query: " + stemmed_query + "\n\n")
                    file.write("{0:5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                        "Query", "Q0", "Doc_ID", "Rank", "Score", "System Name"))

                    rank_counter = 1
                    for item in top_result_set.items():
                        file.write("{0:>5} {1:<3} {2:<10} {3:<5} {4:<10} {5}\n".format(
                            query_counter, "Q0", item[0], rank_counter,
                            round(item[1], 3),
                            "Query_Expansion_using_Psuedo_Relevance_Feedback"))
                        # file.write('{0:40} {1}\n'.format(item[0], item[1]))
                        rank_counter += 1

                print("Output generated for Query-" + str(query_counter))
                results[query_counter] = top_result_set
                query_counter += 1

        with open("stemmed_baseline_results.json", "w+", encoding='utf-8') as file:
            json.dump(results, file)

    except Exception as e:
        print("Exception Raised during Stemmed Query results calculation: " + e.args[1])