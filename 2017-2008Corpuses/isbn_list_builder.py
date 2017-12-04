import ast, re, random
from sklearn.neural_network import MLPRegressor
import numpy as np

#Converts a text file to a python list of default dictionairies representing books

with open('b-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

data = data[28:]
data = data[:-3]

d = "}), defaultdict(<type 'int'>, {"
dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books
bVariables = [] #List of dicts representing sparce vectors representing books
isbnList = []
for book in dataList:
	bookdict = ast.literal_eval(book)
	for key in bookdict.keys():
		if re.match('primary_isbn13*',key): 
			isbnList.append(key[key.find(" ")+3:])
			break
myfile.close()
print len(isbnList)
print len(dataList)
text_file = open("nyt_corpus_isbn.txt", "w")
text_file.write(str(isbnList))
text_file.close()
