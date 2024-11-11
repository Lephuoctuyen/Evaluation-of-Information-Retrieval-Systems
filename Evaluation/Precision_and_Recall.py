'''
The following script calculates the Precision and Recall
of all queries of a Retrieval Model. It takes the average precision for each
query and then using those values, it interpolates to calculate
the mean average precision.
'''

import json
from os import path
from collections import OrderedDict

''' 
The method generates the mean average precision for
given input baseline run and relevance values.

Input: 
@baseline:param         Results of the retrieval model for all the
                        queries. Should be in json format where
                        the structure should be
                        key: QueryID
                        values: [docID, scores]

@relevance_file:param   File location containing the relevance
                        information.

@Returns:   It returns the Mean Average Precision Value for the given
            retrieval model
'''


def precision_recall_calculator(baseline, relevance_file, system_name):
    # Variables
    results = OrderedDict()
    relevance = OrderedDict()

    # key: Query_ID
    # values: [Precision_Value@p=1, .....]
    precision = OrderedDict()

    # key: Query_ID
    # values: [Recall@p=1, .....]
    recall = OrderedDict()

    # key: Query_ID
    # values: [R/NR, ....]
    relevance_info = OrderedDict()

    results, relevance = load_modules(baseline, relevance_file)

    # iterate through each query results
    for query in results:

        result_docs = results[query]
        try:
            relevant_docs = relevance[query]
        except KeyError:
            # Excluding queries which are not present
            # in the relevance file
            continue

        num_relevant_docs = len(relevant_docs)

        retrieved_docs = 0
        relevant_docs_counter = 0

        for doc in result_docs:
            if doc == '':
                continue

            retrieved_docs += 1
            if doc in relevant_docs:
                relevant_docs_counter += 1
                info = 'R'
            else:
                info = 'NR'

            # Recall calculation
            if query not in recall:
                recall[query] = [relevant_docs_counter / num_relevant_docs]
            else:
                values = recall[query]
                values.append(relevant_docs_counter / num_relevant_docs)
                recall[query] = values

            # Precision calculation
            if query not in precision:
                precision[query] = [relevant_docs_counter / retrieved_docs]
            else:
                values = precision[query]
                values.append(relevant_docs_counter / retrieved_docs)
                precision[query] = values

            # Relevance Calculation
            if query not in relevance_info:
                relevance_info[query] = [info]
            else:
                values = relevance_info[query]
                values.append(info)
                relevance_info[query] = values

    generate_result(precision, recall, relevance_info, results, system_name)


def load_modules(baseline, relevance_file):
    results = OrderedDict()
    relevance = OrderedDict()

    # Load baseline and relevance file.
    try:
        with open(baseline, 'r', encoding='utf-8') as file:
            results = json.load(file)
    except FileNotFoundError as e:
        print("Baseline file not found." + str(e.args) + "\nCould not calculate MAP values. "
                                                         "Exiting the program.")
        exit(-2)

    try:
        with open(relevance_file, 'r', encoding='utf-8') as file:
            relevance = json.load(file)
    except FileNotFoundError:
        print("Relevance information file not found. Exiting the"
              "program...")
        exit(-2)

    return results, relevance


def generate_result(precision, recall, relevance_info, results, system_name):
    file_name = "precision_recall_values_" + system_name

    # Save to disk the precision and recall values generated
    # for the retrieval model.
    p = path.join(path.dirname(path.abspath(__file__)),
                  "Files", "precision_values_" + system_name + ".json")
    with open(p, 'w+', encoding='utf-8') as file:
        json.dump(precision, file)

    p = path.join(path.dirname(path.abspath(__file__)),
                  "Files", "recall_values_" + system_name + ".json")
    with open(p, 'w+', encoding='utf-8') as file:
        json.dump(recall, file)

    with open(path.join(path.dirname(path.abspath(__file__)),
                        "Output", file_name + ".txt"),
              'w+', encoding='utf-8') as file:
        file.write("Precision and Recall Values for "
                   "every query in the " + system_name + ":\n\n")

        # iterate through each query
        file.write("{0:10} {1:10} {2:10} {3:5} {4:10} {5:10}\n".format(
            "Query_ID", "DOC_ID", "Relevance", "Rank", "Precision", "Recall"))

        for query in results:

            try:
                p_result_list = precision[query]
                r_result__list = recall[query]
                rel_result_list = relevance_info[query]
                result_docs = list(results[query])

                for i in range(0, len(result_docs)):
                    file.write("{0:10} {1:<10} {2:<10} {3: <5} {4:<10} {5:<10}\n".format(
                        query, result_docs[i], rel_result_list[i], i+1,
                        round(p_result_list[i], 2), round(r_result__list[i], 2)))

                file.write("\n")
            except KeyError:
                continue
