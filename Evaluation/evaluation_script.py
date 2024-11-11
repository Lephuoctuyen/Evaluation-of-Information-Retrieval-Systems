'''
This script performs the evaluation of several retrieval
systems by calculating their
    1. MAP
    2. MRR
    3. Precision at Rank k
    4. Precision and Recall
'''
from Evaluation.Mean_Average_Precision import mean_average_precision
from Evaluation.Mean_Reciprocal_rank import mean_reciprocal_rank
from Evaluation.Precision_and_Recall import precision_recall_calculator
from Evaluation.Precision_at_Rank_5_20 import precision_at_rank_calculator
from os import path
from operator import itemgetter

# Variables
result_scores = dict()

"""
This method calculates the MAP for the baseline runs the
prints to a results file their MAP values along their system
names in sorted order.
"""


def calculate_map():

    # Required files
    relevance_file = path.join(path.pardir, "utilities",
                               "relevance_information.json")

    # effectiveness_noise_queries(relevance_file)
    #
    # effectiveness_noise_minimized_queries(relevance_file)

    # return

    effectiveness_query_expansion(relevance_file)

    effectiveness_bm25(relevance_file)

    effectiveness_sq_likelihood(relevance_file)

    effectiveness_tfidf(relevance_file)

    effectiveness_lucene(relevance_file)


def effectiveness_noise_queries(relevance_file):
    baseline_run = path.join(path.pardir, "Extra_Credit", "Noise_Generator",
                             "noise_induced_bm25_result.json")

    # MAP for BM25 on noise-induced queries baseline run
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR for BM25 on noise-induced queries baseline run
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "BM25 on noise-queries")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "BM25 on noise-queries" + ".json")
    precision_at_rank_calculator(precision_file, "BM25 on noise-induced queries")

    result_scores["Mean Average Precision"] = [["BM25 on noise-induced queries", v]]
    result_scores["Mean_Reciprocal_Rank"] = [["BM25 on noise-induced queries", mrr]]

    print("MAP, MRR and Precision and Recall generated for BM25 on noise-induced queries Model.\n")


def effectiveness_noise_minimized_queries(relevance_file):
    baseline_run = path.join(path.pardir, "Extra_Credit", "Noise_Minimizer",
                             "noise_minimized_bm25_result.json")

    # MAP for BM25 on noise-induced queries baseline run
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR for BM25 on noise-induced queries baseline run
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "BM25 on noise-minimized queries")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "BM25 on noise-minimized queries" + ".json")
    precision_at_rank_calculator(precision_file, "BM25 on noise-minimized queries")

    values = result_scores["Mean Average Precision"]
    values.append(["BM25 on noise-minimized queries", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["BM25 on noise-minimized queries", mrr])

    print("MAP, MRR and Precision and Recall generated for BM25 on noise-minimized queries Model.\n")


def effectiveness_query_expansion(relevance_file):
    baseline_run = path.join(path.pardir, "Retrieval", "Query_Expansion",
                             "stemmed_baseline_results.json")

    # MAP for Query_Expansion baseline run
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR for Query_Expansion baseline run
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "Query_Expansion")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "Query_Expansion" + ".json")
    precision_at_rank_calculator(precision_file, "Query_Expansion")

    result_scores["Mean Average Precision"] = [["Query_expansion", v]]
    result_scores["Mean_Reciprocal_Rank"] = [["Query_expansion", mrr]]

    print("MAP, MRR and Precision and Recall generated for Query Expansion Model.\n")


def effectiveness_bm25(relevance_file):

    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "BM25_Model", "bm25_baseline_results.json")

    # MAP for BM25 baseline run
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR for BM25 baseline run
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "BM25")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "BM25" + ".json")

    precision_at_rank_calculator(precision_file, "BM25")

    values = result_scores["Mean Average Precision"]
    values.append(["BM25", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["BM25", mrr])

    # BM25 Stopped baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "BM25_Model", "bm25_stopped_baseline_results.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "BM25_Stopped")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "BM25_Stopped" + ".json")

    precision_at_rank_calculator(precision_file, "BM25_Stopped")

    values = result_scores["Mean Average Precision"]
    values.append(["BM25 Stopped", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["BM25 Stopped", mrr])

    print("MAP, MRR and Precision and Recall generated for BM25 Model.\n")


def effectiveness_sq_likelihood(relevance_file):
    # Stopped SQ Likelihood Model baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "SQ_Likelihood_Model", "sq_likelihood_stopped_baseline_results.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "SQ_Likelihood_Stopped")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "SQ_Likelihood_Stopped" + ".json")

    precision_at_rank_calculator(precision_file, "SQ_Likelihood_Stopped")

    values = result_scores["Mean Average Precision"]
    values.append(["SQ_Likelihood_Stopped", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["SQ_Likelihood_Stopped", mrr])

    # SQ Likelihood Model baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "SQ_Likelihood_Model", "sq_likelihood_baseline_results.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "SQ_Likelihood")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "SQ_Likelihood" + ".json")

    precision_at_rank_calculator(precision_file, "SQ_Likelihood")

    values = result_scores["Mean Average Precision"]
    values.append(["SQ_Likelihood", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["SQ_Likelihood", mrr])

    print("MAP, MRR and Precision and Recall generated for SQLikelihood Model.\n")


def effectiveness_tfidf(relevance_file):
    # TFIDF baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "TFIDF_Model", "TFIDF_results.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "TF_IDF")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "TF_IDF" + ".json")

    precision_at_rank_calculator(precision_file, "TF_IDF")

    values = result_scores["Mean Average Precision"]
    values.append(["TFIDF", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["TFIDF", mrr])

    # Stopped TFIDF baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "TFIDF_Model", "Stopped_TFIDF_results.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "TF_IDF_Stopped")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "TF_IDF_Stopped" + ".json")

    precision_at_rank_calculator(precision_file, "TF_IDF_Stopped")

    values = result_scores["Mean Average Precision"]
    values.append(["Stopped_TFIDF", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["Stopped_TFIDF", mrr])

    print("MAP, MRR and Precision and Recall generated for TFIDF Model.\n")


def effectiveness_lucene(relevance_file):
    # Lucene baseline run
    baseline_run = path.join(path.pardir, "Retrieval", "Retrieval_Model",
                             "LuceneSearchEngine", "result_dict.json")

    # MAP
    v = mean_average_precision(baseline_run, relevance_file)

    # MRR
    mrr = mean_reciprocal_rank(baseline_run, relevance_file)

    # Precision and Recall
    precision_recall_calculator(baseline_run, relevance_file, "Lucene")

    # Precision at rank =5 and rank = 20
    precision_file = path.join(path.dirname(path.abspath(__file__)), "Files",
                               "precision_values_" + "Lucene" + ".json")
    precision_at_rank_calculator(precision_file, "Lucene")

    values = result_scores["Mean Average Precision"]
    values.append(["Lucene", v])

    values = result_scores["Mean_Reciprocal_Rank"]
    values.append(["Lucene", mrr])

    print("MAP, MRR and Precision and Recall generated for Lucene Model.\n")

"""
This method prints the evaluation results to 
a text file in order
    Evaluation Method:
        System Name     Score
        .
        .
        .
    
    Evaluation Method:
    .
    .
    .
    
"""


def print_results():
    global result_scores

    # Sort the baseline scores and print to a results file
    file_name = path.join(path.dirname(path.abspath(__file__)), "Output", "evaluation_results.txt")
    with open(file_name, 'w+', encoding='utf-8') as file:
        for model in result_scores:
            v = result_scores[model]
            v = sorted(v, key=itemgetter(1), reverse=True)
            result_scores[model] = v

        for item in result_scores:
            file.write("\n" + item + ":\n\n")
            for results in result_scores[item]:
                file.write('{0:25} {1}\n'.format(results[0], results[1]))


# Main program to start the evaluation execution
if __name__ == '__main__':
    calculate_map()
    print_results()