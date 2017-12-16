import re
import ast 
import urllib2
import dryscrape
import collections
import os
from time import sleep
#import numpy as np


#DON'T RUN - ALREADY HAS BEEN RUN ONCE (or just change the names of the text files)




#Converts a text file to a python list of default dictionairies representing books
#FROM: corpus_reader.py

bookList = []
for filename in os.listdir('.'):
	if filename == "corpus-consolidator.py":
		continue
	print filename
	#sleep(3)
	with open(filename, 'r') as myfile:
		data = myfile.read()

	data = data[1:-1]
	d = '}{'
	dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books

	for bookString in dataList: #converts from string to dictionary
		bookDict = ast.literal_eval(bookString)
		if bookDict in bookList:
			print("Found duplicate in: " + filename)
			continue
		bookList.append(bookDict)
	print len(bookList)
	

bVariables = []


for book in bookList:
	sparceVector = collections.defaultdict(int)
	for key in book:
		if key == "book_details":
			for key2 in book[key][0]:
				try:
					sparceVectorKey = str(key2) + " = " + str(book[key][0][key2])
				except:
					#print("oh no, couldnt add something for " +key2) 
					continue
				sparceVector[sparceVectorKey] = 1
		else:
			try:
				sparceVectorKey = str(key) + " = " + str(book[key])
			except:
				#print("oh no, couldnt add something for " +key)
				continue
			sparceVector[sparceVectorKey] = 1
	bVariables.append(sparceVector)
	

print(len(bVariables))

text_file = open("b-variables-corpus.txt", "w")
text_file.write(str(bVariables))
text_file.close()

