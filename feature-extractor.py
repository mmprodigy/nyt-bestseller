#from sknn.mlp import Classifier, Layer
import mechanize
import re
import ast 
from bs4 import BeautifulSoup
import urllib2
#import dryscrape
import collections
#import numpy as np


#DON'T RUN - ALREADY HAS BEEN RUN ONCE (or just change the names of the text files)




#Converts a text file to a python list of default dictionairies representing books
#FROM: corpus_reader.py

with open('sample-output.xml', 'r') as myfile:
	data = myfile.read()

d = '''<?xml version="1.0" encoding="UTF-8"?>'''

dataList =  data.split(d) #List of strings representing dictionairies/books

'''
The features include, Title [0], Page number [1], Author [2], publication_year [3] /
publication_month [4], publication_day, publisher, description [5], reviews_count, average rating [6], list of shleves over 50 [7],
number of text reviews [9]
'''

bookFeatures = []

for data in dataList:
	if not data: continue
#	print("data is: ", data)
	print("bs starts here:")
	soup = BeautifulSoup(data, 'html.parser')
#	print("title is: ", soup.title.text)
	book_id = soup.id.text
	title = soup.title.text
	num_pages = soup.num_pages.text
	author = soup.author.text
	publication_year = soup.publication_year.text
  	publication_month = soup.publication_month.text
  	publication_day = soup.publication_day.text
  	publisher = soup.publisher.text
  	description = soup.description.text
  	reviews_count = soup.reviews_count.text
  	average_rating = soup.average_rating.text
  	shelves = soup.average_rating.shelves
  	ratings_count = soup.ratings_count.text


	print("title is: ", title)
	print("num_pages is: ", num_pages)
	print("author is: ", author)
	print("publication_year is: ", publication_year)
	print("publication_month is: ", publication_month)
	print("publication_day is: ", publication_day)
	print("publisher is: ", publisher)
	print("description is: ", description)
	print("reviews_count is: ", reviews_count)
	print("")

#	currBook.append()


'''
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
'''
