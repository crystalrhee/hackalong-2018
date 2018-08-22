#!/usr/local/bin/python3
import config
import csv
import json

import numpy as np

from repoFetcher import getReadmeFromUrl
from textToDict import textToDict


def main(input_url = None, top_x = 5, debug = False):
	input_readme = {"this":2, "is":1, "a":0, "lit":20, "test":5, "tagline":8, "dish":420, "wash":0, "famalam":40}
	if input_url:
		readme = getReadmeFromUrl(input_url)
		if readme:
			input_readme = textToDict(readme)
		else:
			print('unable to find input repo\'s readme')
			exit()

	with open(config['input'], newline='') as csvfile:
		with open('commonWords.csv', newline='') as csvfile2:
			scrapedData = csv.reader(csvfile)
			commonWords = csv.reader(csvfile2)
			# key = repo url, value = similarity score (range from [-1, 1], 1 being the same)
			similarities = {}

			def unsharedWordsRemoval(textDict):
				intersection = [i for i in set(textDict.keys()).intersection(set(input_readme.keys()))]
				if len(intersection) == 0:
					return 0
				else:
					return intersection

			def commonWordRemoval(wordList):
				for word in commonWords:
					wordList.remove(word)
			
			inputMagnitude = np.linalg.norm([input_readme[word] for word in tfidf(input_readme, 30)]) 
			for row in scrapedData:
				gitURL = row[0]
				tagLineDict = json.loads(row[1])
				words = unsharedWordsRemoval(tagLineDict)
				if words != 0:
					scrapedVector = [tagLineDict[word] for word in words]
					inputVector = [input_readme[word] for word in words]
					scrapedMagnitude = np.linalg.norm([tagLineDict[word] for word in tfidf(tagLineDict, 30)])
					cosValue = np.divide(np.dot(scrapedVector, inputVector), np.multiply(scrapedMagnitude, inputMagnitude)) #cos(theta) = a.b/|a||b|
					print(gitURL, cosValue)
					similarities[gitURL] = cosValue
				else:
					similarities[gitURL] = -1

			# sorting it to be [1, 1.2, -1.3, ...] and grabs the first top_x elements
			top_repos = sorted(similarities, key=lambda repo: abs(similarities[repo] - 1.0))[:top_x]

			if debug:
				for repo in top_repos:
					print(similarities[repo], repo)

			# if debug:
			# 	from texttable import Texttable
			# 	table = Texttable()
			# 	table.set_cols_dtype(['f', 'f', 't'])
			# 	table.add_row(['similarity', 'delta', 'url'])
			# 	for repo in top_repos:
			# 		delta = abs(similarities[repo] - 1)
			# 		table.add_row([similarities[repo], delta, repo])
			# 	print(table.draw())

			return top_repos

if __name__ == '__main__':
	urls = main('https://github.com/mojombo/glowstick', 20, debug=True)
