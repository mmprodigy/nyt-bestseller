import ast, re, random
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
import matplotlib.pyplot as plt
%matplotlib inline
import matplotlib

#Converts a text file to a python list of default dictionairies representing books

with open('b-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

data = data[28:]
data = data[:-3]

d = '}), defaultdict(<type "int">, {'

dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books

bVariables = [] #List of dicts representing sparce vectors representing books
###Outdated update with new data
for book in dataList:
	#Create nlp features, right now individual words
	bookdict = ast.literal_eval(book)
	for key in bookdict.keys():
		if re.match('rank.*',key): bookdict[key] = 0 #zeroing out rank data
		'''if re.match('description.*',key):
			words = key.split(" ")
			for w in words[2:]:
				if w != '':
					bookdict[w] = 1'''
	bVariables.append(bookdict)

myfile.close()


with open('p-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

pVariables = ast.literal_eval(data) #List of variables representing the P variables
#create training and testing
myfile.close()
trainingB = []
trainingP = []
testingB = []
testingP = []
#Replace all this with this
trainingB, testingB, trainingP, tesingP = train_test_split(bVariables, pVariables)

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

trainingBMatrix = [[] for _ in range(len(trainingB))]

#for i in range(0, len(bVariables)):


#twoDArrays = [3]
#for i in range(0, trainingB):
#	twoDArrays


featureIndexToDescription = {}
featureDescriptionToIndex = {}
uniquenessCheck = set()


'''
for book in trainingB:
	bookFeatures = []
	trainingBMatrix.append(bookFeatures)
'''


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


count = 0

for i in range(0, len(trainingBMatrix)):
	for key in trainingB[i]:
		if key not in uniquenessCheck:
			uniquenessCheck.add(key)
			trainingBMatrix[i].append(1)
			for j in range(0, i):
				trainingBMatrix[j].append(0)
			for j in range(i+1, len(trainingBMatrix)):
				trainingBMatrix[j].append(0)
			featureIndexToDescription[len(trainingBMatrix[i]) - 1] = key
			featureDescriptionToIndex[key] = len(trainingBMatrix[i]) - 1
		else:
			index = featureDescriptionToIndex[key]
			trainingBMatrix[i][index] = 1
testingBMatrix = [[0]*len(uniquenessCheck) for _ in range(len(testingB))]
for i in xrange(len(testingBMatrix)):
    for key in testingB[i]:
        if key in uniquenessCheck:
            index = featureDescriptionToIndex[key]
            testingBMatrix[i][index] = 1

#GET THE Total NUMBER OF FEATURES BY DOING len(uniquenessCheck)


numNeurons = len(uniquenessCheck) * 2 /3
layers = [numNeurons] * 30
nn = MLPClassifier(hidden_layer_sizes = layers,activation = 'tanh', solver = 'adam',\
                  batch_size= 'auto',learning_rate='constant',  learning_rate_init =0.001,max_iter=500, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=None,tol=0.0001, validation_fraction=0.1, verbose=False, warm_start=False)


#adjust parameters if needed, espeically layers, use heuristics in write up



predictions= nn.fit(trainingBMatrix,trainingP)

###predictions = nn.predict(testingBMatrix)
###print confusion_matrix(y_test,predictions)
print(classification_report(testingP,predictions))

print "loss: ", trained.loss
print "parameters: ", trained.get_params(deep=True)
print trained.score(trainingBMatrix,trainingP)
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
''''


#Testing dataset'


'''
test = trained.predict(testingBMatrix)
print trained.score(testingBMatrix, testingP)
v = sum([(t - np.mean(testingP))**2 for t in testingP])
print "error: ", (1- float(trained.score(testingBMatrix,testingP)))*v
print "suppose error: ", (1 + float(trained.score(testingBMatrix,testingP)))*v'''

