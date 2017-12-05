#from sknn.mlp import Classifier, Layer
from bs4 import BeautifulSoup
import sys
import mechanize
import json, requests


'''
	XML Feature Extractor
	----------------------
	Extracts an array of features (enumerated below) from input file of one or more lxml files.
'''

# FILL IN THIS WITH YOUR INPUT FILE. THIS SHOULD BE IN THE SAME DIRECTORY AS feature_extractor.py
INPUT_FILE = 'nytGR_output_tot.txt'
# THIS IS THE OUTPUT FILE AND DOES NOT NEED TO BE CHANGED.
OUTPUT_FILE = 'feature-extractor-output3.txt'


# opens input file
with open(INPUT_FILE, 'r') as myfile:
	data = myfile.read()
feature_data = open(OUTPUT_FILE, 'a')


d = '</GoodreadsResponse>'
dataList =  data.split(d)[2000:3000] #List of strings representing dictionairies/books
print len(dataList)

'''
The features include, book_id [0], title [1], num_pages [2], author [3], publication_year [4] /
publication_month [5], publication_day [6], publisher [7], description [8], reviews_count [9], /
average rating [10], rating_count [11], popular_shelves (shelves with count geq 50) [12],  reviewers,bestSeller,
'''
book_features = []

for data in dataList:
#	print("data is: ", data)
	if not data or len(data) < 150: continue
#	print("data is: ", data)
	#print("bs starts here:")
	soup = BeautifulSoup(data, 'html.parser')
	print("title is: ", soup.title.text)

	book_id = soup.id.text
	title = soup.title.text

	try:
		num_pages = soup.num_pages.text
	except:
		num_pages = ""

	try:
		author = soup.author.text
	except:
		author = ""

	try:
		publication_year = soup.publication_year.text
	except:
		publication_year = ""


  	try: 
	  	publication_month = soup.publication_month.text
  	except: 
  		publication_month = ""

  	try: 
	  	publication_day = soup.publication_day.text
  	except: 
  		publication_day = ""
  	try:
  		publisher = soup.publisher.text
  	except:
  		publisher = ""

  	try:
	  	description = soup.description.text
	except:
		description = ""

	try:
		reviews_count = soup.reviews_count.text
	except:
		reviews_count = ""

	try:
	  	average_rating = soup.average_rating.text
	except:
		average_rating = ""

	try:
	  	ratings_count = soup.ratings_count.text
	except:
		ratings_count = ""

	#####Get Reviews!
	widget = soup.reviews_widget

	startIndex = (widget.text).find('</style>') + len('</style>')
	iframeDiv = widget.text[startIndex:]
	try:
		iframeSoup = BeautifulSoup(iframeDiv, 'html.parser')
	except:
		print("OH NO! COULDN'T MAKE IFRAME SOUP!")
		raise
	try:
		reviewPageUrl = iframeSoup.iframe['src']
	except:
		print("OH NO! COULDN'T FIND REVIEW LINK!")
		raise

	br = mechanize.Browser()
	br.set_handle_robots(False)

	try:
		webResponse = br.open(reviewPageUrl)
	except:
		print("OH NO! COULDN'T OPEN REVIEW URL!")
		raise

	reviewWebPage = webResponse.read()

	try:
		reviewPageSoup = BeautifulSoup(reviewWebPage, "html.parser")
	except:
		print("OH NO! COULDN'T MAKE REVIEW PAGE SOUP!")
		raise
	reviews = []
	count = 0
	for reviewDivs in reviewPageSoup.findAll("div", {"class" : "gr_review_text"}):
		if count < 5:
			webResponse = br.open(reviewDivs.link['href'])
			try:
				reviewSoup = BeautifulSoup(webResponse.read(), "html.parser")
			except:
				print("OH NO! COULDN'T OPEN REVIEW SOUP!")
				raise
			review = reviewSoup.findAll("div", {"class" : "hreview"})
			reviewText = review[0].findAll("div", {"class" : "reviewText"})
			reviews.append(reviewText[0].text)
			count += 1
  	popular_shelves = []
  	shelves = soup.popular_shelves
#  	print("popular shelves are: ", shelves)
	if bool(shelves):
	  	for shelf in shelves.findChildren():
	#  		print("shelf is: ", shelf)
	#  		print("shelf.count is:", shelf["count"])
	  		name, count = shelf["name"], int(shelf["count"])
	  		if count >= 50:
	  			popular_shelves.append((name, count))
	bestSeller = 1
	feature_data.write(str(list([book_id, title, num_pages, author, publication_year, publication_month, publication_day, publisher, description, reviews_count, average_rating, ratings_count, popular_shelves,  reviews, bestSeller])))
	delimitor = "!!!!"
	feature_data.write(delimitor)
'''

	print("title is: ", title)
	print("num_pages is: ", num_pages)
	print("author is: ", author)
	print("publication_year is: ", publication_year)
	print("publication_month is: ", publication_month)
	print("publication_day is: ", publication_day)
	print("publisher is: ", publisher)
	print("description is: ", description)
	print("reviews_count is: ", reviews_count)
	print("shelves is: ", popular_shelves)
'''

myfile.close()
feature_data.close()

