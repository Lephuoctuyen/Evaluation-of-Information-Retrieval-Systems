# Set of functions which generate a corpus out of the raw html documents
from bs4 import BeautifulSoup
from os import listdir
from os import path
import re
import string
import nltk
import threading

files = []
counter = 0
stopwords = []


class MyThread(threading.Thread):
    def __init__(self, thread_ID, name, p, out_path, flist):
        threading.Thread.__init__(self)
        self.threadID = thread_ID
        self.name = name
        self.rc_path = p
        self.out = out_path
        self.flist = flist

    def run(self):
        print("Started " + self.name)
        for item in self.flist:
            parse_pages(self.rc_path, item, self.out)
        print("Exiting " + self.name)


def getStopWords():
    global stopwords

    p = path.join(path.pardir, path.pardir, path.pardir, "utilities", "Material", "common_words.txt")
    with open(p, "r") as ins:
        for line in ins:
            line = line.strip('\n')
            stopwords.append(line)


def parse_pages(raw_corpus_path, names, corpus_out):
    global counter
    global files
    global stopwords

    # Debug Information
    counter += 1
    if counter == len(files) * 0.1:
        print("Processed 10% of the Corpus")
    elif counter == len(files) * 0.3:
        print("Processed 30% of the Corpus")
    elif counter == len(files) * 0.5:
        print("Processed 50% of the Corpus")
    elif counter == len(files) * 0.7:
        print("Processed 70% of the Corpus")
    elif counter == len(files) * 0.9:
        print("Processed 90% of the Corpus")
    elif counter == len(files):
        print("Processing Complete.")

    # Form the absolute path
    file_path = path.join(raw_corpus_path, str(names))

    # Extract the title from the absolute file name
    file_title = re.match("(.*?).html", names)
    if file_title:
        file_title = file_title.group(1)

    # Open the file to parse through it to
    # extract only the plain text
    with open(file_path, 'r', encoding='utf-8') as file:
        soup_object_inter = BeautifulSoup(file.read(), 'html.parser')
        text = str(soup_object_inter.getText()).encode('ascii', 'ignore')
        text = text.decode('utf-8', 'ignore')
        text = re.sub("\d+\t\d+\t\d+", '', text)
        tokens = nltk.word_tokenize(text.strip())

        with open(path.join(corpus_out, str(file_title) + ".txt"), 'w+', encoding='utf-8') as output_file:
            for keys in tokens:
                keys = keys.strip(string.punctuation)
                filter_output = re.match(
                    '(\w+(\.\w+)+)|(\w+(-\w+)+)+|(\w+(_\w+)+)+|[A-z]+|(\d(-\d+)+)+|(\d(\.\d+)+)+'
                    '|(\d(\,\d+)+)+|(\d+:\d+\w+)|\d+|[^_\-,⋅.?:’\')({}\]\[]',
                    keys)

                # check if the word is not a stopword
                if filter_output is not None:
                    # Case-folding the appropriate words- Converting to lower case
                    if str(filter_output.group().lower()) not in stopwords:
                        output_file.write(str(filter_output.group().lower()) + "\n")

        # Close the file pointer to the corpus
        output_file.close()

        # Close the file pointer to the raw html page
        file.close()


# Function which creates a thread and splits the
# pages parsed
def split_and_parse():
    global files
    global counter

    raw_c_path = path.join(path.pardir, path.pardir, path.pardir,
                           "utilities", "Material", "cacm.tar")
    corpus_out = path.join(path.pardir, path.pardir, path.pardir,
                           "Corpuses", "Stopped_Corpus_Files")
    files = listdir(raw_c_path)
    num = len(files) / 1000
    threads = []
    print("Starting Parser...")
    print("Spanning Threads")
    for i in range(1, int(num) + 2):
        name = "Thread-" + str(i)
        if i == 1:
            try:
                threads.append(MyThread(i, name, raw_c_path, corpus_out, files[0: i * 1000]))
            except IndexError:
                threads.append(MyThread(i, name, raw_c_path, corpus_out, files[0: len(files)]))
        else:
            try:
                threads.append(MyThread(i, name, raw_c_path, corpus_out, files[(i - 1) * 1000: i * 1000]))
            except IndexError:
                threads.append(MyThread(i, name, raw_c_path, corpus_out, files[(i - 1) * 1000: len(files)]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Debug Information
    print("Parsing complete. Check Corpus_Files folder for more information.")


# Driver Program
if __name__ == '__main__':
    getStopWords()

    split_and_parse()
