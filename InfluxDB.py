import requests
import time
import json
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
if {'name': 'BitFinex'} not in client.get_list_database():
	client.create_database('BitFinex')
	print("Не удалось подключиться в БД, создал заного")
	
urlBitFinex = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"
urlInfluxDB = 'http://localhost:8086/write?db=BitFinex'
count = 1

while True:
	response = requests.get(urlBitFinex)
	allPairs = json.loads(response.text)

	for i in allPairs:
		body = f"BitFinex,pair={i[0]},mid={i[5]},bid={i[1]},ask={i[3]},last_price={i[7]},low={i[10]},high={i[9]},volume={i[8]} fields={count}"
		requests.post(urlInfluxDB, data=body)
		count += 1

	print("OK")
	time.sleep(10)
