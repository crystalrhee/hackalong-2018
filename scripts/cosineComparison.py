import numpy as np 
import csv
import json

with open("out.csv", newline='') as csvfile:

	scrapedData = csv.reader(csvfile)
	testInput = {"dish":420, "wash":69, "lit":1337, "tv":0} #to be replaced with real input from the front end
	testFrontEndInput = {"this":2, "is":1, "a":0, "lit":20, "test":5, "tagline":8, "dish":420, "wash":0, "famalam":40}
	similarities = {}

	for row in scrapedData:
		frontEndVector = []
		gitURL = row[0]
		tagLineDict = json.loads(row[1])
		scrapedVector = list(tagLineDict.values())
		for word in list(tagLineDict.keys()): #need only dict keys, need to convert the returned value froms .keys() from a dict object to a list
			try:
				frontEndVector.append(testFrontEndInput[word])
			except KeyError:
				frontEndVector.append(0) #this means only keys that are in the current scraped dictionary will be added to the inputted one. If they were added, they would be 0 (as they're only in one of the dicts) and so this saves computation time
		if sum(frontEndVector) != 0:
			theta = np.arccos(np.divide(np.dot(scrapedVector, frontEndVector), np.multiply(np.linalg.norm(scrapedVector), np.linalg.norm(frontEndVector)))) #theta = cos^-1(a.b/|a||b|)
			similarities[gitURL] = theta
		else:
			theta = 0

print("Most similar github repo:", sorted(similarities.items())[-1][0])