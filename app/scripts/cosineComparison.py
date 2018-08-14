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
			return {i:textDict[i] for i in {j for j in textDict}.intersection({k for k in testFrontEndInput})}

		def tfidf(textDict):
			words = list(textDict.keys())
			importance = {}
			for word in words:
				importance[word] = np.divide(1, textDict[word]) #1/freqency -> importance
			sortedDict = sorted(importance.values()) #defined outside of loop to only have it sorted once
			importantWords = []
			for i in range(20): #return list of 20 most important words
				try:
					importantWords.append(sortedDict[-i])
				except IndexError:
					return importantWords #if less than 20 words, return existing list
			return importantWords

		for row in scrapedData:
			frontEndVector = []
			gitURL = row[0]
			tagLineDict = json.loads(row[1])
			words = tfidf(unusedWordRemoval(tagLineDict))
			scrapedVector = [tagLineDict[i] for i in words]
			for word in words:
				try:
					frontEndVector.append(testFrontEndInput[word])
				except KeyError:
					frontEndVector.append(0) #this means only keys that are in the current scraped dictionary will be added to the inputted one. If they were added, they would be 0 (as they're only in one of the dicts) and so this saves computation time
			if np.sum(frontEndVector) != 0 and len(words) != 0:
				#carrying out all mathematical functions in numpy to utalize that sweet C speed
				theta = np.arccos(np.divide(np.dot(scrapedVector, frontEndVector), np.multiply(np.linalg.norm(scrapedVector), np.linalg.norm(frontEndVector)))) #theta = cos^-1(a.b/|a||b|)
				similarities[gitURL] = theta
			else:
				similarities[gitURL] = -1
		scores = sorted(similarities.items())[-top_x:]
		repos = list(map(lambda x: x[0], scores))
		return repos

if __name__ == '__main__':
	urls = main('https://github.com/jnewland/lazy_record', 1)
	for url in urls: 
		print (url)