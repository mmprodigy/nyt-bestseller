import ast 

#Converts a text file to a python list of default dictionairies representing books

with open('b-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

data = data[28:]
data = data[:-3]

d = '}), defaultdict(<type "int">, {'

dataList =  ['{' + e + '}' for e in data.split(d)] #List of strings representing dictionairies/books

bVariables = [] #List of dicts representing sparce vectors representing books

for book in dataList:
	bVariables.append(ast.literal_eval(dataList[4]))

myfile.close()



with open('p-variables-corpus.txt', 'r') as myfile:
    data = myfile.read()

pVariables = ast.literal_eval(data) #List of variables representing the P variables

myfile.close()



#HERE:
#use pVariables and bVariables in the regression. Unfortunately bVariables in not a
#defaultdict, its a regular dict. 
