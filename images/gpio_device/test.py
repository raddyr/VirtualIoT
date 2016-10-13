import urllib, json
import os
import time

gpio0 = os.getenv('GPIO_0');
gpio1 = os.getenv('GPIO_1');
gpio2 = os.getenv('GPIO_2');

url = "https://query.yahooapis.com/v1/public/yql?q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20%3D%20502075&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
response = urllib.urlopen(url)
data = json.loads(response.read())['query']['results']['channel']['item']['condition']['code']

with open(gpio2, 'w') as f:
	if data == '29': #29,30 == Partly Cloudy
		f.write('1')
	else:
		f.write('0')
	f.flush()

with open(gpio1, 'w') as led:
	with open(gpio0, 'r') as switch:
		while True:
			read = switch.read(1)
			print read
			led.write(read)
			led.flush()
			time.sleep(1)

