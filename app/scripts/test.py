from textblob import TextBlob as tb
testtext= "hello there"
testtest2 = "goodbye there"
testtext3 = "test test"

blobs = [testtext, testtest2, testtext3]

def blobReturner():
	for i in blobs:
		yield tb(i)

scores = {}

def scoreRecorder(blob):
	i = 0
	for word in blob.words:
		i+=1
		scores[word] = i
	return scores

blolbs = [blob for blob in blobReturner()]


for blob in blolbs:
	scoreRecorder(blob)

for i in list(scores.items())[:-2]:
	print(i)



