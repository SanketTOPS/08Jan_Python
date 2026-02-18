import requests

url="https://fakestoreapi.com/products"

rq=requests.get(url)
data=rq.json()
#print(data)

for i in data:
    print(i["id"])
    print(i["title"])
    print(i["price"])