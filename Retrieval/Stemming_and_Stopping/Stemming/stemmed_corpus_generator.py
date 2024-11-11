import os
from os import path

doc_counter = 0
all_terms = []
directory = "STEMMED_CORPUS_FILES"


def printfile(all_terms, doc_counter):
    l = all_terms[::-1]
    count = -1
    for item in l:
        count = count + 1
        if (item.isdigit()):
            continue
        else:
            found_pos = count
            break
    reqd = l[found_pos:]
    reqd = reqd[::-1]  # reverse the list to get the order in which terms appear in the document
    with open(os.path.join(directory, "CACM_" + str(doc_counter) + ".txt"), 'a', encoding='utf-8') as file:
        for term in reqd:
            file.write(term + "\n")

    file.close()


def readDoc():
    global all_terms, doc_counter, directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    p = str(path.join(path.pardir, "Material/cacm_stem.txt"))
    # with open("cacm_stem.txt", "r") as ins:
    with open(p, "r") as ins:
        for line in ins:
            if (line.startswith('#')):  # found a new document when hash is encountered
                doc_counter = doc_counter + 1
                print(doc_counter)

                if (doc_counter != 1):
                    printfile(all_terms, doc_counter - 1)  # print the previous document
                    all_terms = []
                continue

            # print(line) write to a file
            else:
                terms = line.split()
                all_terms.extend(terms)

    printfile(all_terms, doc_counter)  # to print the last document


readDoc()
print(path.pardir)
