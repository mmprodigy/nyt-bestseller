import mechanize
import re
import ast 
from bs4 import BeautifulSoup
import urllib2
import dryscrape
import collections


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




br = mechanize.Browser()
session = dryscrape.Session()
isbnToSales = collections.defaultdict(float)


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
	isbnToSales[book["book_details"][0]["primary_isbn10"]] = (novNum + octNum)/2

print isbnToSales
