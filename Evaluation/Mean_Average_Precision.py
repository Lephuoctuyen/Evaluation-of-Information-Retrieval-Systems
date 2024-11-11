'''
The following script calculates the Mean Average Precision
of Retrieval Model. It takes the average precision for each
query and then using those values, it interpolates to calculate
the mean average precision.
'''

import json

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


def mean_average_precision(baseline, relevance_file):
    # variables
    results = dict()
    relevance = dict()
    avg_precision = []

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

    # traverse each query and get their resultant documents
    for query in results:
        precision_values = []
        retrieved_docs = 0
        relevant_docs = 0

        result_docs = results[query]

        # traverse the resultant docs and check for
        # their existence in the relevance files.
        # If exists, calculate precision at rank k, and
        # add them to a list for further processing

        for doc in result_docs:
            try:
                if doc in relevance[query]:
                    relevant_docs += 1
                    retrieved_docs += 1
                    p = relevant_docs / retrieved_docs
                    precision_values.append(p)
                else:
                    retrieved_docs += 1
            except KeyError:
                # Excluding queries which are not present
                # in the relevance file
                continue

        # Calculate the average precision for a query and
        # store them in a list.
        try:
            avg = sum(precision_values) / len(precision_values)
        except ZeroDivisionError:
            avg = 0

        avg_precision.append(avg)

    # Take an average of all the average precision values
    # to find the Mean Average Precision.
    MAP = sum(avg_precision) / len(avg_precision)

    return MAP
