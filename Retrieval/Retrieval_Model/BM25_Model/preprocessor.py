# Pre-processes the information for the retrieval model to use
# term: [[doc_id, pre-bm25_score]...]
import json
import math
from os import path

# Model constants
num_term_docs = 0
num_total_docs = 0
param_k1 = 1.2
param_b = 0.75
param_K = 0
processed_score = dict()

# Structure which stores the document lengths
try:
    p = path.abspath(path.join(path.pardir, path.pardir, path.pardir, "Indexes",
                               "Stopped_Inverted_index", "docs_term_freq.json"))
    # p = path.abspath(path.join(path.pardir, path.pardir, path.pardir, "Indexes",
    #                            "Digit_Stemmed_Inverted_index", "docs_term_freq.json"))
    with open(p, 'r') as doc_dict:
        docs_term_freq = json.load(doc_dict)
except FileNotFoundError:
    print("File containing document length and average document length "
          "information not found.")
    exit(-2)

# Structure which stores the uni-gram indexer
try:
    with open(path.join(path.pardir, path.pardir, path.pardir, "Indexes",
                        "Stopped_Inverted_index", "uni_dict.json"), 'r') as dict_file:
    # with open(path.join(path.pardir, path.pardir, path.pardir, "Indexes",
    #                     "Digit_Stemmed_Inverted_index", "uni_dict.json"), 'r') as dict_file:
        uni_dict = json.load(dict_file)
except FileNotFoundError:
    print("Uni-gram indexer not found.")
    exit(-2)

# Structure to store the pre-processed information for the
# retrieval model
try:
    y = str(path.join("stopped_processed_score.json"))
    # y = str(path.join("digit_stemmed_processed_score.json"))
    with open(y, 'r') as dict_file:
        uni_score_values = json.load(dict_file)
except FileNotFoundError:
    uni_score_values = dict()


def preprocessor():
    global num_term_docs
    global num_total_docs
    global param_K
    global param_k1
    global param_b
    global processed_score

    counter = 0

    num_total_docs = len(docs_term_freq) - 1
    avg_doc_len = docs_term_freq['00_avdl_00']
    print("Calculating the pre BM25 scores.")
    l = len(uni_dict)
    for term in uni_dict:
        counter += 1
        if counter == l * 0.1:
            print("Processed 10% of the indexer.")
        elif counter == l * 0.3:
            print("Processed 30% of the indexer.")
        elif counter == l * 0.5:
            print("Processed 50% of the indexer.")
        elif counter == l * 0.7:
            print("Processed 70% of the indexer.")
        elif counter == l * 0.9:
            print("Processed 30% of the indexer.")

        processed_score[term] = value = []
        num_term_docs = len(uni_dict[term])

        # calculate the binary-model score for the term
        bm_score = math.log(1 / ((num_term_docs + 0.5) / (num_total_docs - num_term_docs + 0.5)))

        for doc in uni_dict[term]:
            param_K = param_k1 * ((1 - param_b) + (param_b * (docs_term_freq[doc[0]] / avg_doc_len)))
            pre_bm25_score = bm_score * (((param_k1 + 1) * doc[1]) / (param_K + doc[1]))
            value.append([doc[0], pre_bm25_score])
            processed_score[term] = value

    print("Processing the indexer is completed. Writing the information to"
          " a file.")

    # write the pre-processed scores to a file
    j = path.join("stopped_processed_score.json")
    # j = path.join("digit_stemmed_processed_score.json")
    with open(j, "w+") as file:
        json.dump(processed_score, file)


if __name__ == '__main__':
    preprocessor()
