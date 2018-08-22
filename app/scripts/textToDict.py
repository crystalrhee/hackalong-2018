#!/usr/local/bin/python3
import config
import csv
import json
import string


def removeChars(text):
    return ''.join([x for x in text.lower() if x in string.ascii_letters + '\'- '])

def textToDict(text):
    vector = {}
    for word in removeChars(text).split():
        vector[word] = vector[word] + 1 if word in vector else 1
    return vector

if __name__ == '__main__':
    with open(config.READMES, 'r') as f:
        with open(config.SCORES, 'w') as outfile:
            reader = csv.reader(f, quotechar='"')
            writer = csv.writer(outfile)
            for row in reader:
                try:
                    url, text = row
                    text = json.loads(text)
                except Exception as e:
                    print('bad csv format')
                    raise e
                writer.writerow([url, json.dumps(textToDict(text))])
