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

		"""Using cosine similarity to determine how related two readme files are. Had to adapt the idea a little.
		a.b has all unused words removed from a and b as their results in the cross product will be 0 anyway (one of the words will have a frequency of 0)
		and this reduces the amount of loops required to make the vector of the words. After unshaerd words are removed, the tfidf function calculates and returns
		the top 'x' words (testing with 30, can reduce for more accuracy) to increase accuracy by removing common words like 'the' that two readmes may share in high frequencies
		the |a||b| section had to be adapted to these methods by retaining the unshared words (their frequencies still contributed), as well as ommiting their own uncommon words.
		This way, comparisons were not thrown off by one readme being significantly larger than the other, yet still having many of the same unique words, at the same
		time reducing the value if there was a unique word in one readme that didn't appear in the other. The amount of important words considered should strike a 
		balance between ommiting common words, without ommiting important words that happen to appear a lot. An alternative might be compiling a list of common words
		and simply removing those, but that eliminates generality. It may be an idea though to compile a list of common words based on comparing every scraped readme file,
		and then removing words from that - almost like training our function based on data. That way, high frequency yet unique words wouldn't be taken out, as they'd
		only be common to the indivisual readme."""

		inputMagnitude = np.linalg.norm([input_readme[word] for word in tfidf(input_readme, 30)]) 
		for row in scrapedData:
			gitURL = row[0]
			tagLineDict = json.loads(row[1])
			words = tfidf(unsharedWords(tagLineDict), 30)
			if words != 0:
				scrapedVector = [tagLineDict[word] for word in words]
				frontEndVector = [input_readme[word] for word in words] #eliminates word frequency
				# print(gitURL, tagLineDict)
				# print(gitURL, tagLineDict.values())
				# print(gitURL, scrapedVector)
				# print(gitURL, scrapedVector,"\n")
				# print(gitURL, frontEndVector, "\n")
				scrapedMagnitude = np.linalg.norm([tagLineDict[word] for word in tfidf(tagLineDict, 30)])
				print(scrapedMagnitude)
				#cos(theta) = a.b/|a||b|
				cosValue = np.divide(np.dot(scrapedVector, frontEndVector), np.multiply(scrapedMagnitude, inputMagnitude))
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
