import json
import string
import csv

INPUT_FILE = 'repo-contents.csv'
OUT_FILE = "out.csv"

def textToDict(text):
    vector = {}
    for word in text.translate(string.punctuation) \
                    .replace('\n', '') \
                    .lower() \
                    .split(' '):
        vector[word] = vector[word] + 1 if word in vector else 1
    return vector


with open(INPUT_FILE, 'r') as f:
    with open(OUT_FILE, 'w') as outfile:
        reader = csv.reader(f, quotechar='"')
        writer = csv.writer(outfile)
        for row in reader:
            try:
                url, text = row
            except Exception as e:
                print('bad csv format')
                raise e
            writer.writerow([url, json.dumps(textToDict(text))])
