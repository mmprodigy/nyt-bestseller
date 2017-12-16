import ast, re, random
import collections
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.decomposition import TruncatedSVD
#import matplotlib.pyplot as plt
#import matplotlib
import scipy
import numpy as np 

#Converts a text file to a python list of default dictionairies representing books

#with open('extractedfeatures.txt', 'r') as myfile:
with open('extractedfeatures-final-clean.txt', 'r') as myfile:
	data = myfile.read()

output = open('final-set-output.txt', 'a')


#testset = [i for i in range(0, 6790, 5)]


d = ']!!!!['

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

#BOOK_LIMIT = 100000




dataList =  [e for e in data.split(d)] #List of strings representing dictionairies/books
bVariables = [] #List of dicts representing sparce vectors representing books
pVariables = []
bookct = 0
for book in dataList:
#        book = dataList[idx]
#	quit()
#	if ct > BOOK_LIMIT: 
#		break
#	print("book is: ", book)
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
	print("title is: ", booklist[1])
#	print("str booklist[5] is: ", str(booklist[5]))

	if booklist[5] != '':
		month = {"pubmonth = " + str(booklist[5]) : 1}
	else:
		month["pubmonth = "] = 1

	### popular shelves
	shelves = collections.defaultdict()
	#print booklist[12]
	for item in booklist[12]:
		#print("item is:", item)
		shelves[item[0]] = item[1]
	shelves["book"] = 1
	'''
	### description 
	description = collections.defaultdict()
	words = booklist[8].split()
	if len(words) > 1:
		for i in xrange(len(words)-1):
			description[(words[i], words[i+1])] = 1
	description["book"] = 1
	'''
	### reviews
	wc = 0
	bigram = collections.defaultdict()
	reviewed = False
	if len(booklist[13])>0:
		for review in booklist[13]:
			words = review.split()
			wc += len(words) 
			if reviewed == False:
				reviewed = True
				for i in range(0,len(words)-1):
					bigram[(words[i], words[i+1])] = 1
		newlist.append(wc)	#word count 3
		wc = wc/ float(len(booklist[13]))
	else:
		bigram[("book","book")] = 1

	newlist.append(wc) # average word count of review 4
	newlist.append(shelves) # 5
	newlist.append(author) # 6
	newlist.append(year) # 7
	newlist.append(month) # 8
	newlist.append(bigram) # 9
#	newlist.append(description) #10
	pVariables.append(booklist[14]) # y values if it is a best seller or not
	print("line")
#	print("newlist is: ", newlist)
#	print("pVariables are: ", pVariables)
	bVariables.append(newlist)

	print("length of newlist is: ", len(newlist))
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
#print("bVariables is: ", bVariables)



#also check why length isn't same
for i in range(len(bVariables)):
	print("i is: ", i)
	for j in range(5):
#		print("i, j is: ", (i,j), "bVariables[i][j] is: ", bVariables[i][j])
		try:
			# try to add these continuous features 
			bMatrix[i].append(float(bVariables[i][j])) ##Add in continuous features
		except:
			# if it cannot be cast as a float
#			if not bVariables[i][j]:
			bMatrix[i].append(0.0)
			'''
			elif type(bVariables[i][j]) == unicode: 
				bMatrix[i].append("")
				print(type(bVariables[i][j]))
				print(bVariables[i][j])
#				quit()
#			print("Problem is, we have :", bVariables[i][j], ", that is type", type(bVariables[i][j]))
#			quit()
			'''

	for j in range(5,len(bVariables[i])):
#		print("i, j is: ", (i,j), "bVariables[i][j] whoo is: ", bVariables[i][j])
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
#				if bVariables[i][j] == {}:
#					bMatrix[i][index] = 0
#				else:
				bMatrix[i][index] = float(bVariables[i][j][key])

#print("type is: ", type(bMatrix[0][0]))


'''
print("checking length")
for i in range(len(bMatrix)):
	print(len(bMatrix[i]))
	for j in range(len(bMatrix[i])):
		item = float(bMatrix[i][j])
	#	if not (type(item) is float or type(item) is int):
#			if item == "":
		bMatrix[i][j] = 0
'''
'''
		else:
			bMatrix[i][j] = float(item)
			print("Error: Invalid Matrix Entry")
			print("Item is", item)
			print("At position i, j is: ", (i , j))
			print("Type of item is: ", type(item))
#			quit()
		'''

#print("first row is: ", bMatrix[0])
#print("second row is: ", bMatrix[1])


tsvd = TruncatedSVD(n_components=110)
n_matrix = np.matrix(bMatrix)
X_sparse = scipy.sparse.csr_matrix(n_matrix)
X_sparse_tsvd = tsvd.fit_transform(X_sparse)
print("Created!")
print('Original number of features:' + str(X_sparse.shape[1]))
print('Reduced number of features:' + str(X_sparse_tsvd.shape[1]))
#quit()
output.write('Original number of features:' + str( X_sparse.shape[1]))
output.write('Reduced number of features:' + str(X_sparse_tsvd.shape[1]))

#print()
#print len(bMatrix[0])

trainingB = []
trainingP = []
testingB = []
testingP = []
#pVariables = [[var] for var in pVariables]
#Replace all this with this
#bMatrix = np.array(bMatrix, dtype='float32')
#pVariables = np.array(pVariables)


print("bMatrix length is: ", len(bMatrix))
print("bMatrix[0] length is: ", len(bMatrix[0]))

output.write("bMatrix length is: " + str(len(bMatrix)))
output.write("bMatrix[0] length is: " + str(len(bMatrix[0])))


trainingB, testingB, trainingP, testingP = train_test_split(X_sparse_tsvd, pVariables, test_size=0.50)
#print("type of trainingB[0][0] is: ", type(trainingB[0][0]))
#print("type of trainingP[0] is: ", type(trainingP[0]))
#print(pVariables)


output.write("trainingB is: ")
output.write(str(trainingB))
output.write("testingB is: ")
output.write(str(testingB))
output.write("trainingP is: ")
output.write(str(trainingP))
output.write("testingP is: ")
output.write(str(testingP))
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

output.write("len trb is: " + str(len(trainingB)))
output.write("len teb is: " + str(len(testingB)))
output.write("len trp is: " + str(len(trainingP)))
output.write("len tep is: " + str(len(testingP)))




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

output.write(str(classification_report(testingP,testing_pred)))
output.write("testing_pred is: " + str(testing_pred ))

#quit()

print "Loss: ", trained.loss
print "Parameters: ", trained.get_params(deep=True)
print "Trained Score: ", trained.score(trainingB,trainingP)
print "Weights are: "
for coeff in nn.coefs_:
        print coeff
output.write( "Loss: " + str( trained.loss))
output.write( "Parameters: " + str( trained.get_params(deep=True)))
output.write( "Trained Score: " + str(trained.score(trainingB,trainingP)))
output.write( "Weights are: ")
for coeff in nn.coefs_:
        output.write(coeff)

output.close()

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

