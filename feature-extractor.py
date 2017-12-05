#from sknn.mlp import Classifier, Layer
from bs4 import BeautifulSoup
import sys


'''
	XML Feature Extractor
	----------------------
	Extracts an array of features (enumerated below) from input file of one or more lxml files.
'''

# FILL IN THIS WITH YOUR INPUT FILE. THIS SHOULD BE IN THE SAME DIRECTORY AS feature_extractor.py
INPUT_FILE = 'sample-output.xml'
# THIS IS THE OUTPUT FILE AND DOES NOT NEED TO BE CHANGED.
OUTPUT_FILE = 'feature-extractor-output.txt'


# opens input file
with open(INPUT_FILE, 'r') as myfile:
	data = myfile.read()
feature_data = open(OUTPUT_FILE, 'w')


d = '</GoodreadsResponse>'
dataList =  data.split(d) #List of strings representing dictionairies/books


'''
The features include, book_id [0], title [1], num_pages [2], author [3], publication_year [4] /
publication_month [5], publication_day [6], publisher [7], description [8], reviews_count [9], /
average rating [10], rating_count [11], popular_shelves (shelves with count geq 50) [12]
'''
book_features = []

for data in dataList:
#	print("data is: ", data)
	if not data or len(data) < 150: continue
#	print("data is: ", data)
	print("bs starts here:")
	soup = BeautifulSoup(data, 'html.parser')
#	print("title is: ", soup.title.text)

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
	book_features.append([book_id, title, num_pages, author, publication_year, publication_month, publication_day, publisher, description, reviews_count, average_rating, ratings_count, popular_shelves])

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

feature_data.write(str(book_features))
myfile.close()
feature_data.close()

