import json, requests
from time import sleep
from bs4 import BeautifulSoup
import mechanize


key = 'LZH0ts76EISqgfIICORHPA'
url =  'https://www.goodreads.com/book/title.xml'
title = "Ender's Game"
author = "Orson Scott Card"
params = {
			"format" : 'xml',
			"key" : key,
			"title" : title,
			"author" : author
		}

try:
	resp = requests.get(url=url, params=params)
except:
	print("OH NO! COULDN'T GET REQUEST!")
	raise


try:
	soup = BeautifulSoup(resp.content, 'xml')
except:
	print("OH NO! COULDN'T MAKE XML SOUP!")
	raise


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


for reviewDivs in reviewPageSoup.findAll("div", {"class" : "gr_review_text"}):
	webResponse = br.open(reviewDivs.link['href'])
	try:
		reviewSoup = BeautifulSoup(webResponse.read(), "html.parser")
	except:
		print("OH NO! COULDN'T OPEN REVIEW SOUP!")
		raise
	
	review = reviewSoup.findAll("div", {"class" : "hreview"})
	reviewText = review[0].findAll("div", {"class" : "reviewText"})
	print reviewText[0].text	
	print("###############################################################################3")


	


