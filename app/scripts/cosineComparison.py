#!/usr/local/bin/python3
import numpy as np 
import csv
import json
from textToDict import textToDict
from repoFetcher import getReadmeFromUrl
from config import CosineComparison as config

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
		scrapedData = csv.reader(csvfile)
		# key = repo url, value = similarity score (range from [-1, 1], 1 being the same)
		similarities = {}

		def unsharedWords(textDict):
			intersection = {i:textDict[i] for i in {j for j in textDict}.intersection({k for k in input_readme})}
			if len(intersection) == 0:
				return 0
			else:
				return intersection

		def tfidf(textDict, size):
			if textDict == 0:
				return 0
			else: 
				words = list(textDict.keys())
				importance = {}
				for word in words:
					importance[word] = np.divide(1, np.divide(textDict[word], len(input_readme))) #1/freqency -> importance. divided by lenth of input dict to normalize
				sortedDict = sorted(importance, key=importance.get) #defined outside of loop to only have it sorted once
				importantWords = []
				for i in range(size): #return list of 20 most important words
					try:
						importantWords.append(sortedDict[-i - 1])
					except IndexError:
						if len(importantWords) == 0:
							return 0;
						else:
							return importantWords #if less than 20 words, return existing list
				if len(importantWords) == 0:
					return 0;
				else:
					return importantWords
					
		inputMagnitude = np.linalg.norm([input_readme[word] for word in tfidf(input_readme, 30)]) 
		for row in scrapedData:
			gitURL = row[0]
			tagLineDict = json.loads(row[1])
			words = tfidf(unsharedWords(tagLineDict), 30)
			if words != 0:
				scrapedVector = [tagLineDict[word] for word in words]
				inputVector = [input_readme[word] for word in words] #eliminates word frequency
				scrapedMagnitude = np.linalg.norm([tagLineDict[word] for word in tfidf(tagLineDict, 30)])
				cosValue = np.divide(np.dot(scrapedVector, inputVector), np.multiply(scrapedMagnitude, inputMagnitude)) #cos(theta) = a.b/|a||b|
				similarities[gitURL] = cosValue
			else:
				similarities[gitURL] = -1

		# sorting it to be [-1, ..., 1], grabs the last {top_x} elements and reverse it to be [1, .5, ...]
		top_repos = sorted(similarities, key=similarities.get)

		if debug:
			for repo in top_repos:
				print(similarities[repo], repo)

		return top_repos

if __name__ == '__main__':
	urls = main('https://github.com/technoweenie/duplikate', 20, debug=True)
