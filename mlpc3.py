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

#with open('extractedfeatures.txt', 'r') as myfile:
with open('extractedfeatures-fixed-cleaned.txt', 'r') as myfile:
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
	print("book is: ", book)
	#Create nlp features, right now individual words
	try:
		booklist = ast.literal_eval(book)
	except:
		booklist = []
		continue
	newlist = []
	if len(booklist) != 15 :
		continue
	newlist.append(booklist[2]) 	# page num 		0
	newlist.append(booklist[10]) 	# av rating 	1
	newlist.append(booklist[11]) 	# rating count 	2
	
	author = {"author = "+ booklist[3] : 1}
	year = {"pubyear = " + booklist[4] : 1}
	month = {}
	print("booklist[5] is: ", booklist[5])
	print("str booklist[5] is: ", str(booklist[5]))

	if booklist[5] != '':
		month = {"pubmonth = " + str(booklist[5]) : 1}
	else:
		month["pubmonth = "] = 1

	### popular selves
	selves = collections.defaultdict()
	#print booklist[12]
	for item in booklist[12]:
		#print("item is:", item)
		selves[item[0]] = item[1]
	selves["book"] = 1

	### description 
	description = collections.defaultdict()
	words = booklist[8].split()
	if len(words) > 1:
		for i in xrange(len(words)-1):
			description[(words[i], words[i+1])] = 1
	description["book"] = 1


	### reviews
	wc = 0
	bigram = collections.defaultdict()
	if len(booklist[13])>0:
		for review in booklist[13]:
			words = review.split()
			wc += len(words) #word count 3
			for i in range(0,len(words)-1):
				bigram[(words[i], words[i+1])] = 1
		wc = wc/ float(len(booklist[13]))
	else:
		bigram["book"] = 1
	newlist.append(wc) # average word count of review 4
	newlist.append(selves) # 5
	newlist.append(author) # 6
	newlist.append(year) # 7
	newlist.append(month) # 8
	newlist.append(bigram) # 9
	newlist.append(description) #10
	pVariables.append(booklist[14]) # y values if it is a best seller or not
	print("line")
	print("newlist is: ", newlist)
#	print("pVariables are: ", pVariables)
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

print("")
print("")
print("")
print("")
print("bVariables is: ", bVariables)

for i in range(len(bVariables)):
	for j in range(0,5):
		try:
			bMatrix[i].append(float(bVariables[i][j])) ##Add in continuous features
		except:
			if not bVariables[i][j]:
				continue
			elif type(bVariables[i][j]) == unicode: 
				bMatrix[i].append("")
				print(type(bVariables[i][j]))
				print(bVariables[i][j])
#				quit()
			print("Problem is, we have :", bVariables[i][j], ", that is type", type(bVariables[i][j]))
#			quit()

	for j in range(5,len(bVariables[i])):
		for key in bVariables[i][j]:
#			if not key: continue
			if key not in uniquenessCheck:
				uniquenessCheck.add(key)
				bMatrix[i].append(float(bVariables[i][j][key]))
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
					bMatrix[i][index] = float(bVariables[i][j][key])

#print("type is: ", type(bMatrix[0][0]))

print("checking length")
for i in range(len(bMatrix)):
	print(len(bMatrix[i]))
	for j in range(len(bMatrix[i])):
		item = bMatrix[i][j]
		if not (type(item) is float or type(item) is int):
			if item == "":
				bMatrix[i][j] = 0
			else:
				print("Error: Invalid Matrix Entry")
				print("Item is", item)
				print("At position i, j is: ", (i , j))
				print("Type of item is: ", type(item))
#			quit()


#print()
#print len(bMatrix[0])

trainingB = []
trainingP = []
testingB = []
testingP = []
#pVariables = [[var] for var in pVariables]
#Replace all this with this
bMatrix = np.array(bMatrix, dtype='float32')
pVariables = np.array(pVariables)

trainingB, testingB, trainingP, testingP = train_test_split(bMatrix, pVariables, test_size=0.50)
print("type of trainingB[0][0] is: ", type(trainingB[0][0]))
print("type of trainingP[0] is: ", type(trainingP[0]))



#print(pVariables)


print("trb is: ", trainingB )
print("teb is: ", testingB)
print("trp is: ", trainingP)
print("tep is: ", testingP)



#quit()


numNeurons = int(len(trainingB[0]) * 2 /3)
#layers = [numNeurons] * 30
layers = [numNeurons] * 10
#nn = MLPClassifier(hidden_layer_sizes = layers,activation = 'tanh', solver = 'adam',\
#				  batch_size= 'auto',learning_rate='constant',  learning_rate_init =0.001,max_iter=500, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=None,tol=0.0001, validation_fraction=0.1, verbose=False, warm_start=False)
nn = MLPClassifier(hidden_layer_sizes = layers,activation = 'tanh', solver = 'adam',\
				  batch_size= 'auto',learning_rate='constant',  learning_rate_init =0.001,max_iter=200, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=None,tol=0.0001, validation_fraction=0.1, verbose=False, warm_start=False)

#trainingB = np.array(trainingB).reshape(-1, 1)
#testingB = np.array(trainingB).reshape(-1, 1)

#trainingB = np.array(trainingB,dtype=str)
#testingB = np.array(testingB,dtype=str)

print("len trb is: ", len(trainingB))
print("len teb is: ", len(testingB))
print("len trp is: ", len(trainingP))
print("len tep is: ", len(testingP))


#adjust parameters if needed, espeically layers, use heuristics in write up

#print("trainingB is: ", trainingB)
#print("testingB is: ", testingB)


trained= nn.fit(trainingB, trainingP)
#predictions= nn.fit([map(float, x) for x in trainingB],map(float, trainingP))

#print(predictions)

###predictions = nn.predict(testingBMatrix)
###print confusion_matrix(y_test,predictions)
testing_pred = trained.predict(testingB)
print(classification_report(testingP,testing_pred))
print("testing_pred is: ", testing_pred )

print "loss: ", classification_report.loss
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

