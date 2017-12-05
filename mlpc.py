import ast, re, random
import collections
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
import matplotlib

#Converts a text file to a python list of default dictionairies representing books

with open('feature-extractor-outputold.txt', 'r') as myfile:
	data = myfile.read()



d = '!!!!'

'''for i in range(0, len(trainingBMatrix)):
	for book in trainingB:
	for key in book:
	if key not in uniquenessCheck:
	# ADD TO UNIQUE DICT
	#ADD TO TRANINGBMATRIX[book] AS 1, 0 FOR EVERYTHING ELSE
	#ADD TO fITOD
	#ADD TO fDTOI
	else:
	#FIND INDEX USING fDESCRIPTIONTOI THEN SET TO 1
	#'''
'''book_id [0], title [1], num_pages [2], author [3], publication_year [4] /
	publication_month [5], publication_day [6], publisher [7], description [8], reviews_count [9], /
	average rating [10], rating_count [11], popular_shelves (shelves with count geq 50) [12],  reviews[13],bestSeller[14],'''
'''
	TODO: isolate [14] as Y
	don't need book_id or title
	num_pages : cont add directly into matrix
	publication_year and month : needs to be made categorical
	average rating: cont
	rating_count: cont
	popular_shelves, each a cont elemnt
	reviews, make into n grams,
	make author parse vector
	"author = author name " = 1
	"pyear = year" = 1
	popular shelves should be a dictionary convert from tuple
	"pyear = month" = 1
	
	
	'''

dataList =  [e for e in data.split(d)] #List of strings representing dictionairies/books
bVariables = [] #List of dicts representing sparce vectors representing books
pVariables = []
for book in dataList:
	#Create nlp features, right now individual words
	try:
		booklist = ast.literal_eval(book)
	except:
		booklist = []
		continue
	newlist = []
	newlist.append(booklist[2]) # page num 0
	newlist.append(booklist[10]) # av rating 1
	newlist.append(booklist[11]) # rating count2
	
	author = {"author = "+ booklist[3] : 1}
	year = {"pubyear = " + booklist[4] : 1}
	month = collections.defaultdict()
	if booklist[5] != '':
		month = {"pubmonth = " + booklist[5] : 1}

	### popular selves
	selves = collections.defaultdict()
	for item in booklist[12]:
		selves[item[0]] = item[1]
	### description 
	description = collections.defaultdict()
	words = booklist[8].split()
	if len(words) > 1:
		for i in xrange(len(words)-1):
			description[(words[i], words[i+1])] = 1

	### reviews
	wc = 0
	bigram = collections.defaultdict()
	if booklist[13] != [] :
		for review in booklist[13]:
			words = review.split()
			wc += len(words) #word count 3
			for i in range(0,len(words)-1):
				bigram[(words[i], words[i+1])] = 1
		wc = wc/ float(len(booklist[13]))
	newlist.append(wc) # average word count of review 4
	newlist.append(selves) # 5
	newlist.append(author) # 6
	newlist.append(year) # 7
	newlist.append(month) # 8
	newlist.append(bigram) # 9
	newlist.append(description) #10
	pVariables.append(booklist[14]) # y values if it is a best seller or not
	bVariables.append(newlist)

myfile.close()

'''#Normalization
	scaler = StandardScaler()
	scaler.fit(trainingB)
	StandardScaler(copy=True, with_mean=True, with_std=True)
	# Now apply the transformations to the data:
	trainingB= scaler.transform(trainingB)
	testingB = scaler.transform(testingB)'''

#TODO: Reshape testingB and trainingb data into 2D ARRAY size n x m where n is the number of samples and m is the num of features
#Consider all unqiue features and ndarray()?
#HERE:

bMatrix = [[] for _ in range(len(bVariables))]
featureIndexToDescription = {}
featureDescriptionToIndex = {}
uniquenessCheck = set()

count = 0

for i in range(len(bVariables)):
	for j in range(0,5):
		bMatrix[i].append(bVariables[i][j]) ##Add in continuous features
	for j in range(5,len(bVariables[i])):
		for key in bVariables[i][j]:
			if key not in uniquenessCheck:
				uniquenessCheck.add(key)
				bMatrix[i].append(bVariables[i][j][key])
			for k in range(0, i):
				bMatrix[k].append(0)
			for k in range(i+1, len(bMatrix)):
				bMatrix[k].append(0)
			featureIndexToDescription[len(bMatrix[i]) - 1] = key
			featureDescriptionToIndex[key] = len(bMatrix[i]) - 1
		else:
			index = featureDescriptionToIndex[key]
			if bVariables[i][j] == {}:
				bMatrix[i][index] = 0
			else:
				bMatrix[i][index] = bVariables[i][j][key]

#print bMatrix
#print len(bMatrix[0])

trainingB = []
trainingP = []
testingB = []
testingP = []
#Replace all this with this
trainingB, testingB, trainingP, tesingP = train_test_split(bMatrix, pVariables)


numNeurons = len(trainingB[0]) * 2 /3
layers = [numNeurons] * 30
nn = MLPClassifier(hidden_layer_sizes = layers,activation = 'tanh', solver = 'adam',\
				  batch_size= 'auto',learning_rate='constant',  learning_rate_init =0.001,max_iter=500, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=None,tol=0.0001, validation_fraction=0.1, verbose=False, warm_start=False)


#adjust parameters if needed, espeically layers, use heuristics in write up



predictions= nn.fit(trainingB,trainingP)

###predictions = nn.predict(testingBMatrix)
###print confusion_matrix(y_test,predictions)
print(classification_report(testingP,predictions))

print "loss: ", trained.loss
print "parameters: ", trained.get_params(deep=True)
print trained.score(trainingB,trainingP)
'''v = sum([(t - np.mean(trainingP))**2 for t in trainingP])
error = (1 - float(trained.score(trainingBMatrix,trainingP)))*v
print "error: ", error
se = (1 + float(trained.score(trainingBMatrix,trainingP)))*v
print "supposed error ", se'''
#Change because it is changed to a classifier


'''
   print( len(mlp.coefs_))
   print(len(mlp.coefs_[0]))
	print(len(mlp.intercepts_[0]))
'''


#Testing dataset'


'''
test = trained.predict(testingBMatrix)
print trained.score(testingBMatrix, testingP)
v = sum([(t - np.mean(testingP))**2 for t in testingP])
print "error: ", (1- float(trained.score(testingBMatrix,testingP)))*v
print "suppose error: ", (1 + float(trained.score(testingBMatrix,testingP)))*v'''

