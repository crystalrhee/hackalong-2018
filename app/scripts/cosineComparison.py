import numpy as np 
import csv
import json
from textToDict import textToDict
from repoFetcher import getReadmeFromUrl
from config import CosineComparison as config

def main(input_url = None, top_x = 5):
	input_readme = {"this":2, "is":1, "a":0, "lit":20, "test":5, "tagline":8, "dish":420, "wash":0, "famalam":40}
	if input_url:
		input_readme = textToDict(getReadmeFromUrl(input_url))

	with open(config['input'], newline='') as csvfile:
		scrapedData = csv.reader(csvfile)
		similarities = {}

		def unusedWordRemoval(textDict):
			intersection = {i:textDict[i] for i in {j for j in textDict}.intersection({k for k in input_readme})}
			if len(intersection) == 0:
				return 0
			else:
				return intersection

		def tfidf(textDict):
			if textDict == 0:
				return 0
			else: 
				words = list(textDict.keys())
				importance = {}
				for word in words:
					importance[word] = np.divide(1, textDict[word]) #1/freqency -> importance
				sortedDict = sorted(importance, key=importance.get) #defined outside of loop to only have it sorted once
				importantWords = []
				for i in range(20): #return list of 20 most important words
					try:
						importantWords.append(sortedDict[-i])
					except IndexError:
						return importantWords #if less than 20 words, return existing list
				return importantWords

		for row in scrapedData:
			gitURL = row[0]
			tagLineDict = json.loads(row[1])
			words = tfidf(unusedWordRemoval(tagLineDict))
			if words != 0:
				scrapedVector = [tagLineDict[i] for i in words]
				frontEndVector = [input_readme[word] for word in words]
				#theta = cos^-1(a.b/|a||b|)
				theta = np.arccos(np.divide(np.dot(scrapedVector, frontEndVector), np.multiply(np.linalg.norm(scrapedVector), np.linalg.norm(frontEndVector))))
				similarities[gitURL] = theta
			else:
				similarities[gitURL] = -1

		scores = sorted(similarities, key=similarities.get)[-top_x:] #FIX - honestly not sure how your edits work, please make sure this and the following line work the same now that scores is a list with one dimentions, not two.
		repos = list(map(lambda x: x, scores))
		return repos

if __name__ == '__main__':
	urls = main('https://github.com/jnewland/lazy_record', 1)
	for url in urls: 
		print (url