import numpy as np
import csv
from textblob import TextBlob as tb
from itertools import tee
from operator import itemgetter

with open('scores.csv', newline='') as csvfile:
	csvLength, csvContents = tee(csv.reader(csvfile), 2)
	length = sum(1 for row in csvLength)

	#using a generator to avoid using several gigs of memory while calculating
	def textBlobIterator(): 
		for row in csvContents:
			readme = row[1]
			yield tb(readme)

	#creates two independant generators that wont share iteraiton position

	textBlob1, textBlob2 = tee(textBlobIterator(), 2)

	def tf(word, blob):
		return np.divide(blob.words.count(word), len(blob.words))

	def n_containing(word):
	    return sum(1 for blob in textBlob2 if word in blob.words)

	def idf(word):
	    return np.log(np.divide(length, np.add(1, n_containing(word))))

	def tfidf(word, blob):
	    return np.multiply(tf(word, blob), idf(word))

	scores = {}

	for blob in textBlob1:
		scores = {word: tfidf(word, blob) for word in blob.words}

	size = 50
	sorted_words = sorted(scores.items(), key=lambda x: x[1])[:size]
	print(sorted_words)

	with open('commonWords.csv', 'w') as outfile:
		writer = csv.writer(outfile, delimiter=' ')

		for word in list(scores.keys()):
			writer.writerow(word)

