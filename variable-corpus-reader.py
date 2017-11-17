import ast, re, random
from sklearn.neural_network import MLPRegressor

#Converts a text file to a python list of default dictionairies representing books

with open('b-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

data = data[28:]
data = data[:-3]

d = '}), defaultdict(<type "int">, {'

dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books

bVariables = [] #List of dicts representing sparce vectors representing books

for book in dataList:
	#Create nlp features, right now individual words
	bookdict = ast.literal_eval(book)
	for key in bookdict.keys():
		if re.match('rank.*',key): bookdict[key] = 0 #zeroing out rank data
		if re.match('description.*',key):
			words = key.split(" ")
			for w in words[2:]:
				if w != '':
					bookdict[w] = 1
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
for i in xrange(len(bVariables)):
	if random.random() < 0.1:
		testingB.append(bVariables[i])
		testingP.append(pVariables[i])
	else:
		trainingB.append(bVariables[i])
		trainingP.append(pVariables[i])

#TODO: Reshape testingB and trainingb data into 2D ARRAY size n x m where n is the number of samples and m is the num of features
#Consider all unqiue features and ndarray()?
#HERE:
nn = MLPRegressor(hidden_layer_sizes = (10,10),activation = 'tanh', solver = 'sgd',\
 batch_size= 'auto',learning_rate='constant', learning_rate_init =0.001,max_iter=200) #adjust parameters if needed, espeically layers, use heuristics in write up
training = nn.fit(trainingB,trainingP)
print nn.score(trainingB,trainingP)