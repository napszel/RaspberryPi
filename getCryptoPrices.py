import urllib, json

url = "http://api.coinmarketcap.com/v1/ticker/ethereum"
response = urllib.urlopen(url)
data = json.loads(response.read())
print int(round(float(data[0]["price_usd"])))
