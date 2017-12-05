import ast 

#Converts a text file to a python list of default dictionairies representing books

with open('book-corpus-edited.txt', 'r') as myfile:
    data = myfile.read()

d = '}{'
dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books


bookList = [] #list of dictionaries representing books

for bookString in dataList: #converts from string to dictionary
	bookList.append(ast.literal_eval(bookString))



