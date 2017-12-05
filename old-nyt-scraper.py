import ast
import requests
from time import sleep


file = open("oldnytGR_output.txt", "a")
with open('old_nyt_corpus.txt', 'r') as myfile:
	data = myfile.read()
delimitor  = "!!!this is a delimitor!!"
books = ast.literal_eval(data)

key = 'LZH0ts76EISqgfIICORHPA'
url =  'https://www.goodreads.com/book/title.xml'
i = 0

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
	i+=1
	file.write(resp.content)
	file.write(delimitor)
	print str(i) + "books scraped"

	sleep(1)
file.close()
	


	
