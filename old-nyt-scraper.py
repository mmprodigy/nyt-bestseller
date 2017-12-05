import ast
import requests
from time import sleep



with open('old_nyt_corpus.txt', 'r') as myfile:
	data = myfile.read()

books = ast.literal_eval(data)

key = 'LZH0ts76EISqgfIICORHPA'
url =  'https://www.goodreads.com/book/title.xml'


for book in books:
	title = book[0]
	author = book[1]
	
	params = {
				"format" : "xml",
				"key" : key,
				"title" : title,
				"author" : author
			}

	try:
		resp = requests.get(url=url, params=params)
	except:
		print("OH NO! COULDN'T GET REQUEST!")
		raise

	bookXml = resp.content #XML OF BOOK
	print bookXml
	sleep(1)

	


	
