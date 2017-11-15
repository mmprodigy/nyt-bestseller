import json, requests
from datetime import timedelta, date
from sets import Set

text_file = open("book-corpus.txt", "w")

url = 'https://api.nytimes.com/svc/books/v3/lists.json'

isbns = set()

def daterange(start_date, end_date):
	for n in range(int ((start_date - end_date).days)):
		yield start_date - timedelta(n)

start_date = date(2017, 11, 15)
#end_date = date(2017, 11, 12)
end_date = date(2008, 1, 1)
#end_date = date(2016, 11, 15)
for single_date in daterange(start_date, end_date):
	dateParam = single_date.strftime("%Y-%m-%d")
	for i in range(0, 2):
		if i == 0:
			bookType = "hardcover-fiction"
		else:
			bookType = "hardcover-nonfiction"
		params = {
			"api_key" : '0567a6ed99cf46ed8b113b0553378413',
			"date" : dateParam,
			"list" : bookType
		}

		try:
			resp = requests.get(url=url, params=params)
			data = json.loads(resp.text)
		except ValueError:
			print("oh no, value error!")
			continue

		if "results" in data:
			for item in data["results"]: 
				if item["isbns"][0]["isbn10"] not in isbns:
					text_file.write(str(item))
					isbns.add(item["isbns"][0]["isbn10"])
				else:
					continue

text_file.close()