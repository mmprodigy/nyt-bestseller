# nyt-bestseller
Stanford CS221 project for predicting the sale statistics of a book.


## Getting Started

To view the raw text file with formatting, paste this text file in this Github-flavored Markdown Previewer [http://tmpvar.com/markdown.html](http://tmpvar.com/markdown.html) or use some other markdown viewer. 


### Dependencies

The data acquisition portion of this project requires an internet connection along with several different libraries. 

* Numpy
* Matplotlib
* Scikit-Learn
* Beautiful Soup
* Mechanize


## Files

* **book\_corpus\_reader.py** - Script that makes HTTP requests to the New York Times API. The script iterates through 1 week increments between a given start date and given end date, and requests a json containing all books that were on the Bestseller list during that period of time. Output: An intermediate text file containing book data.

* **corpus-consolidator.py** - Script that goes through the various output files from book\_corpus\_reader.py and consolidates them into one file without duplicates. Output: A text file representation of a python list of default dictionaries representing books, b-variables-corpus.txt. 

* **isbn\_list\_builder.py** - Script that takes the output of corpus-consolidator.py generates a list of book title and author pairs (unique book IDs) corresponding to each of the books in a New York Times Bestseller.  Output: A text file representation of a python list of author title tuples.

* **nyt\_gr\_scraper.py** - Script that takes the output of isbn\_list\_builder.py and interates through the list making Goodreads API calls on each book using the title and author. Output: a text file containing the Goodreads API response for each NYT bestseller book. 

* **goodreads-scrape.py** - Script that makes Goodreads API calls similar to nyt\_gr\_scraper.py , except on random non-NYTBestseller books. Output: a text file containing the Goodreads API response for a random set of non-NYT bestseller book. 

* **feature-extractor.py** - Script that takes the output files of goodreads-scrape.py and nyt\_gr\_scraper.py and extracts the relevant book features from the block text within the HTTP response. The output is a text file containing a python list of python lists. Each item in the list corresponds to a book. Each book is represented by a list containing the following information: ```
str(list([book_id, title, num_pages, author, publication_year, publication_month, publication_day, publisher, description, reviews_count, average_rating, ratings_count, popular_shelves,  reviews, bestSeller]))
```

* **extracted-features-clean.py** - After concatting all the feature-extractor outputs into one file, there are a lot of words and images that are uninterpretable because they are written with unicode symbols such as: ```u0434\u0430\u0432\u0430\u0439\u0442\u0435 \u0441\u0435\u0431\u044f \u043e\u0434\u0443```. These symbols sometimes denote images used in reviews, non-English languages, or sometimes English. This script removes these large unicode symbol chunks from the the feature-extractor output, or converts the unicode if it was meant to be English text. 

* **extractedfeatures-final-clean-subset.txt** - A subset of the data contained in extractedfeatures-final-clean.txt. This text file contains the data for our neural net to run, the meta-data of a little over 6750 books. It is the output of extracted-features-clean.py. This file must be in the same directory as mlpc.py in order to run the neural net.

* **mlpc.py** - Script that takes the output of extracted-features-clean.txt and runs the neural net. It iterates through each book represented in the file and 



## How to Run

The codebase contains several scripts for generating intermediary files. However, to run the neural network, you only need mlpc.py and extractedfeatures-final-clean-subset.txt and in the same directory. Than do the following command: 

```
python mlpc.py
```

And then it will train and test using the data provided in extractedfeatures-final-clean-subset.txt.

## Authors

* **Cherie Xu**
* **Alice Yang**
* **Monica Anuforo**

See also the list of [contributors](https://github.com/mmprodigy/nyt-bestseller/graphs/contributors) who participated in this project.