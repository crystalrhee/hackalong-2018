import json
import string
import csv

INPUT_FILE = 'test-dataset.csv'
OUT_FILE = "out.csv"

with open(INPUT_FILE, 'r') as f:
    with open(OUT_FILE, 'w') as outfile:
        reader = csv.reader(f, quotechar='"')
        writer = csv.writer(outfile)
        for row in reader:
            vector = {}
            try:
                url, text = row
            except Exception as e:
                print('bad csv format')
                raise e
            for word in text.translate(string.punctuation) \
                            .replace('\n', '') \
                            .split(' '):
                vector[word] = vector[word] + 1 if word in vector else 0
            writer.writerow([url, vector])
