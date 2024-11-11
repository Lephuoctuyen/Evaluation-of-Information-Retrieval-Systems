'''
The following script calculates the Precision values
at ranks 5 and 20 of all queries of a Retrieval Model.
'''

import json
from os import path
from collections import OrderedDict

''' 
The method generates the mean average precision for
given input baseline run and relevance values.

Input: 
@precision_file:param        Precision Values of the retrieval model for all the
                             queries. Should be in json format where
                             the structure should be
                             key: QueryID
                             values: [precision@1,
                                     precision@2,
                                     ........]

@Returns:   It returns the Mean Average Precision Value for the given
            retrieval model
'''


def precision_at_rank_calculator(precision_file, system_name):

    # Variables
    precision_values = OrderedDict()

    # load the json into a dictionary
    # for traversal
    try:
        with open(precision_file, 'r', encoding='utf-8') as file:
            precision_values = json.load(file)
    except FileNotFoundError:
        print("Precision Values file not found. Exiting the"
              "precision at rank module.")
        return

    # if load is successful, for each query
    # in the precision_values file
    p = path.join(path.dirname(path.abspath(__file__)), "Output",
                  "precision_at_rank_5_20_" + system_name + ".txt")
    with open(p, 'w+', encoding="utf-8") as file:

        file.write("Precision at rank 5 and 20 for " + system_name + ":\n\n")
        file.write("{0:10} {1:<12} {2:<12}\n".format(
            "Query_ID", "Precision@05",  "Precision@20"
        ))

        for query in precision_values:
            precision_val_query = precision_values[query]

            p_at_5 = precision_val_query[4]
            p_at_20 = precision_val_query[19]

            file.write("{0:10} {1:<12} {2:<12}\n".format(
                query, round(p_at_5, 2), round(p_at_20, 2)
            ))