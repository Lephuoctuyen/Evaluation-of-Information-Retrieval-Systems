# file which reads the output produced by lucene and creates a dictionary that contains
# query id and the documents retrieved in order of their rank

from os import path
import codecs
import os
import json
import operator
from collections import OrderedDict

lines = []
dict = {}

# for every line in the result file of lucene
for line in codecs.open('results.txt', 'r', encoding="utf-8"):
    ln = line.strip('\n')
    if ln:
        lg = ln.split('\t')

        # field at position  0 is the query id
        qnum = int(lg[0])

        # field at position 2 is the doc id
        doc = lg[2]
        print(lg)

        if qnum not in dict:
            dict[qnum] = []
            dict[qnum].append(doc)
        else:
            dict[qnum].append(doc)

sorted_1 = sorted(dict.items(), key=operator.itemgetter(0), reverse=False)

sorted_1 = OrderedDict(sorted_1)
print(sorted_1)

file_p = open(os.path.join("result_dict1.json"), "w", encoding='utf-8')
json.dump(sorted_1, file_p, indent=2)
