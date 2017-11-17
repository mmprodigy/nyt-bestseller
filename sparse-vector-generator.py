#from sknn.mlp import Classifier, Layer
import mechanize
import re
import ast 
from bs4 import BeautifulSoup
import urllib2
import dryscrape
import collections
#import numpy as np


#DON'T RUN - ALREADY HAS BEEN RUN ONCE (or just change the names of the text files)




#Converts a text file to a python list of default dictionairies representing books
#FROM: corpus_reader.py

with open('book-corpus-2017-only.txt', 'r') as myfile:
	data = myfile.read()

data = data[1:-1]
d = '}{'
dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books

bookList = [] #list of dictionaries representing books

for bookString in dataList: #converts from string to dictionary
	bookList.append(ast.literal_eval(bookString))


#A lot of this code is FROM: web-scraper.py

br = mechanize.Browser()
session = dryscrape.Session()
isbnToSales = collections.defaultdict(float)

#bookToSales = collections.defaultdict(int)

newBookList = [] #must be the same size as salesList
pVariables = []


for book in bookList:

	amazonUrl = book["amazon_product_url"]
	asinNumber = amazonUrl.partition("dp/")[-1].rpartition('?')[0]
	try:
		response = br.open("https://www.novelrank.com/asin/" + asinNumber)
	except urllib2.URLError, e:
		print(e.args)
		print " for " + "https://www.novelrank.com/asin/" + asinNumber
		continue
	except urllib2.HTTPError, e:
		print (e.code)
		print " for " + "https://www.novelrank.com/asin/" + asinNumber
		continue
	htmlDoc = response.read()
	soup = BeautifulSoup(htmlDoc, 'html.parser')
	tables = soup.find_all("table", class_="table table-condensed table-striped")
	if len(tables) == 0:
		continue
	tableString = tables[0].get_text()
	if 'N/A' in tableString:
		continue
	novNum = int(tableString.partition("November Sales:")[-1].rpartition('October')[0])
	
	restOfString = tableString[tableString.find("Reviews:"):]
	octNum = int(tableString.partition("October Sales:")[-1].rpartition(restOfString)[0])
	
	newBookList.append(book)
	pVariables.append((novNum + octNum)/2)
	#bookToSales[book] = (novNum + octNum)/2
	#break
	#isbnToSales[book["book_details"][0]["primary_isbn10"]] = (novNum + octNum)/2


#X_train = np.ndarray(shape=(len(bookToSales), 1))

print len(pVariables)

bVariables = []


for book in newBookList:
	sparceVector = collections.defaultdict(int)
	for key in book:
		if key == "book_details":
			for key2 in book[key][0]:
				try:
					sparceVectorKey = str(key2) + " = " + str(book[key][0][key2])
				except:
					print("oh no, couldnt add something for " +key2) 
					continue
				sparceVector[sparceVectorKey] = 1
		else:
			try:
				sparceVectorKey = str(key) + " = " + str(book[key])
			except:
				print("oh no, couldnt add something for " +key)
				continue
			sparceVector[sparceVectorKey] = 1
	bVariables.append(sparceVector)
	

print(len(bVariables))

text_file = open("b-variables-corpus.txt", "w")
text_file.write(str(bVariables))
text_file.close()

text_file = open("p-variables-corpus.txt", "w")
text_file.write(str(pVariables))
text_file.close()
	#break

#print isbnToSales
