'''
The following script calculates the Mean Reciprocal Rank
of Retrieval Model. It takes the Reciprocal Rank for each
query and then using those values, it interpolates to calculate
the mean reciprocal rank.
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


def mean_reciprocal_rank(baseline, relevance_file):
    # Variables
    results =  dict()
    relevance = dict()
    rr_list = []

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

        rank_position = 0
        result_docs = results[query]

        try:
            first_rel_doc = relevance[query][0]
        except KeyError:
            # Excluding queries which are not present
            # in the relevance file
            continue

        # traverse the resultant docs and check for
        # check if the doc exists in the relevance files
        # list. If it does, check if it is equivalent to
        # the first relevant doc. If it is, calculate the
        # RR @ p

        for doc in result_docs:
            if doc == first_rel_doc:
                rank_position += 1
                rr_list.append(1 / rank_position)
            else:
                rank_position += 1

    # calculate the mean reciprocal rank (MRR)
    # which is the average of the reciprocal ranks
    # over a set of queries
    MRR = sum(rr_list) / len(rr_list)

    return MRR