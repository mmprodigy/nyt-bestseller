import requests, random, time
from collections import defaultdict


#input should be [isbn, title, author]

file = open("nytGR_output.txt", "a")
isbnList = open("nyt_corpus_title.txt","r").read().split("), (")
isbnList = [(i.split(',')[0][1:len(i.split(',')[0])-1],i.split(',')[1][1:len(i.split(',')[1])-1]) for i in isbnList]
deliminator = "!!!this is a deliminator!!!"

def scrape_review(book, file_object):
	print book
	title = book[1]
	author = book[0]
	
	url =  'https://www.goodreads.com/book/title.xml'
	cherie_key = "DRZpJdOHuw0bM6Y35eiKQ"
	alice_key = "BAiZXR4dXM1lFBoRsQ"
	params = {
				"format" : 'xml',
				"key" : alice_key,
				"title" : title,
				"author" : author
				
			}
	resp = requests.get(url=url, params=params)
	if len(resp.content) < 1000: return 0
	file.write(resp.content)
	file.write(deliminator)
	return 1

i = 0
for isn in isbnList:

	i += scrape_review(isn, file)
#	print("count is: ", i)
	time.sleep(.9)
#	print("cache is:", cache)
	print("count is:", i)


file.close()

 
