import json, requests
 
url = 'https://api.nytimes.com/svc/books/v3/lists.json'

 
params = {
    "api_key" : '0567a6ed99cf46ed8b113b0553378413',
    "date" : "2017-11-14",
    "list" : "hardcover-fiction"
}
 
 
resp = requests.get(url=url, params=params)
data = json.loads(resp.text)


print data["results"]

