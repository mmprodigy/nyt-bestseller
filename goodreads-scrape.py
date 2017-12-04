import requests, random, time
from collections import defaultdict


#input should be [isbn, title, author]
ct = 4937 - 374 - 1086 - 521 - 26 - 707
d = open("cache.txt", "r")


cache = defaultdict(int)
for key in d: 
	cache[key] = 1
book_id = random.randrange(10000000, 99999999)
file = open("goodreads_output.txt", "a")
d.close()
cache_file = open("cache.txt", "w")

def scrape_review(book_id, file_object):
	print("book_id is: ", book_id)
	url =  'https://www.goodreads.com/book/show.xml'
	cherie_key = "BfTf8h3nSb4TgiHUH6EgHA"
	alice_key = "BAiZXR4dXM1lFBoRsQ"
	params = {
				"format" : 'xml',
				"key" : alice_key,
				"id" : book_id,
				"text_only" : True,
			}
	resp = requests.get(url=url, params=params)
	if len(resp.content) < 1000: return 0
	print resp.content
	file.write(resp.content)
	return 1
#		print("oh no, value error!")


# example: 
#test_isbn = "9788700631625"
i = 0
while i < ct:
	while(cache[book_id]):
		book_id = random.randrange(10000000, 99999999)
#	print("book_id is:", book_id)
	cache[book_id] = 1
	i += scrape_review(book_id, file)
#	print("count is: ", i)
	time.sleep(1)
#	print(i, book_id, book.title)
#	print("cache is:", cache)
	cache_file.write(str(cache))
	print("count is:", i)


cache.close()
file.close()



#get_max_book_id(gc)

