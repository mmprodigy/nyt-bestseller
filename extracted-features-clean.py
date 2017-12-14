import ast, re, random
from collections import defaultdict


#CHANGE THIS FILE TO INPUT FILE 
INPUT = 'extractedfeatures-fixed.txt'
#"CHANGE THIS TO OUTPUT CLEANED FILE"
OUTPUT = 'extractedfeatures-fixed-cleaned.txt'


def fix_unicode(a):
	if type(a) == unicode:
		return a.encode('utf8')
	if type(a) == int or type(a) == float or type(a) == str:
		return a
	if type(a) == list:
		return [fix_unicode(b) for b in a]
	if type(a) == tuple:
		return ([fix_unicode(b) for b in a])

d = '!!!!'
bookct = 0
not_lit_eval_ct = 0
not_u_encode_ct = 0

wrongoutfile = open('extractedfeatures-fixed-cleaned-w.txt', 'a')
with open(INPUT, 'r') as infile:
	with open(OUTPUT, 'a') as outfile:
		data = infile.read()
#		print(data)
		datalist = data.split(d)
		for book in datalist:
			for i in range(3):	print("%")

			# NOTE 	text.encode('utf-8') to convert unicode to english text

			# find valid book entries

			try:
				booklist = ast.literal_eval(book)
			except:
				not_lit_eval_ct += 1
				print("not literal_evaluable: ",  booklist)
				booklist = []
				continue

			try:
				fix_unicode(booklist[1]).decode("ascii")
			except UnicodeDecodeError:
#				print("the failed book is:")
#				print(booklist)
				not_u_encode_ct += 1
				print("failed to convert from unicode: ",  booklist)
				booklist = []
				continue
			except:
				continue

			if len(booklist) != 15: continue

			bookct += 1

			# convert 13/15 entries from unicode
			toFix = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]
			for i in toFix:
				entry = booklist[i]
				if type(entry) is list:
					for j in range(len(entry)):
						entry[j] = fix_unicode(entry[j])
				else:
					entry = fix_unicode(entry)
				booklist[i] = entry


			# fix author name formatting
			author = booklist[3]
			if len(author) >= 100:
				indicator = 'https://www.goodreads.com/author/show/'
				start = author.find(indicator) + len(indicator) + 6
#				print("start is: ", start)
#				print("substring is: ", author[start:])
				name = (author[start:].split('\n'))[0].replace('_', ' ')
#				print(name)
				booklist[3] = fix_unicode(name)


			# fix review formatting
			reviews = booklist[13]
			passed_reviews = []
#			print("review count is: ", len(reviews))
			for ct, review in enumerate(reviews):
#				print(ct, "review is: ", review)
				try:
					review.encode('utf-8').decode('ascii')
					passed_reviews.append(fix_unicode(review))
					continue
				except UnicodeDecodeError:
					continue
				except:
					passed_reviews.append(fix_unicode(review))
					continue
#				print(ct, "review type is: ", type(review.encode('utf-8')))
#				print(review.encode('utf-8'))
#				print('\u0' not in review)
#			print(len(passed_reviews), " passed_reviews")
#			print("passed_reviews are: ", passed_reviews)
			booklist[13] = passed_reviews





			

#			print("the fixed booklist is: ")
#			print(booklist)
#			outfile.write(str(booklist)+'!!!!')


			'''
			To fix in script:
			entry 3
			1) author name
			parse author name from entry
			for example:
				'\n13957\nScott Westerfeld\n\n\nhttps://images.gr-assets.com/authors/1442207392p5/13957.jpg\n\n\
				nhttps://images.gr-assets.com/authors/1442207392p2/13957.jpg\n\nhttps://www.goodreads.com/author/
				show/13957.Scott_Westerfeld\n3.84\n1250868\n72844\n'
				\find "goodreads.com/author/show/*****.$$author here$$/

			entry 13
			2) parse description and remove unicode chunks


			'''

			# to fix - 3 - parse, if length > 


#			for i in range(15):
#				print("item ", i, "is: ", booklist[i])

			print("Length of booklist is: ", len(booklist))
#			for ct, val in enumerate(book):
#				print("This is the ", ct,"th entry: ", val) 

	print("Original Count is: ", len(datalist))
	print("Final Count is: ", bookct)
	print("Not Lit Evaluable: ", not_lit_eval_ct)
	print("Not Unicode Convertable: ", not_u_encode_ct)

	outfile.close()
infile.close()

