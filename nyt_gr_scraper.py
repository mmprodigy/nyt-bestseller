import requests, random, time
from collections import defaultdict


#input should be [isbn, title, author]

file = open("nytGR_output10.txt", "a")
isbnList = str(open("nyt_corpus_isbn.txt","r").readlines()).split(',')
isbnList = isbnList[187+380+56:2000]
deliminator = "!!!this is a deliminator!!!"

def scrape_review(isbn, file_object):
	url =  'https://www.goodreads.com/book/isbn/ISBN?format=FORMAT'
	cherie_key = "DRZpJdOHuw0bM6Y35eiKQ"
	alice_key = "BAiZXR4dXM1lFBoRsQ"
	params = {
				"format" : 'xml',
				"key" : cherie_key,
				"isbn" : isbn,
				"text_only" : True
			}
	resp = requests.get(url=url, params=params)
	if len(resp.content) < 1000: return 0
	file.write(resp.content)
	file.write(deliminator)
	return 1
#		print("oh no, value error!")


# example: 
#test_isbn = "9788700631625"
i = 0
for isbn in isbnList:
#	print("book_id is:", book_id)
	i += scrape_review(isbn, file)
#	print("count is: ", i)
	time.sleep(.9)
#	print(i, book_id, book.title)
#	print("cache is:", cache)
	print("count is:", i)


file.close()

 
