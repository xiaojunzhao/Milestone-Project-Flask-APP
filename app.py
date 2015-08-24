from flask import Flask, render_template,request
import csv
import json
import urllib2
from bokeh.plotting import figure, output_file,show
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components

import pandas as pd
import numpy as np

f =  open('WIKI_tickers.txt','r')
csv1 = csv.reader(f, delimiter = ',')


ticker_list=[]

for item in csv1:
    ticker_list.append(item[0])


f.close()


app = Flask(__name__)

@app.route("/",methods = ['GET'])
def home():
	return render_template('home.html')



@app.route("/index",methods = ['POST'])
def index():
	date_list = []
	closing_list = []
	volume_list = []
	adj_closing_price = []
	ticker_name = request.form['ticker']
	ticker = "WIKI/"+ticker_name
	if ticker not in ticker_list:	
		return render_template('home.html')
	else: 
		url = "https://www.quandl.com/api/v1/datasets/"+ticker+".json"
		json_obj = urllib2.urlopen(url)
		json_data =  json.load(json_obj)
		data = sorted(json_data['data'], key = lambda data: data[0])

		for item in data:
			date_list.append(str(item[0]))
			closing_list.append(item[4])
			volume_list.append(item[5])
			adj_closing_price.append(item[11])
		dates = np.array(date_list,dtype = np.datetime64)
		closing_price = np.array(closing_list)
		volume = np.array(volume_list)
		adjusted = np.array(adj_closing_price)


		volume_list = []
		closing_list = []
		date_list= []
		adj_closing_price = []
		if request.form['features'] == 'close':
			p = figure(title = "Closing price",x_axis_label = 'Date', x_axis_type = "datetime",y_axis_label = 'Closing Price')
			p.line(dates,closing_price,legend = "Closing price", line_width = 1)
			script, div = components(p)
			html = file_html (p,CDN,'my plot')
			#return html
			return render_template('plot.html',script = script, div = div)
		elif request.form['features'] == 'volume': 
			p = figure(title = "Volume",x_axis_label = 'Date', x_axis_type = "datetime",y_axis_label = 'Volume')
			p.line(dates,volume,legend = "Volume", line_width = 1)
			html = file_html (p,CDN,'my plot')
			script, div = components(p)
			#return html
			return render_template('plot.html',script = script, div = div)
		elif request.form['features'] == 'adj_close':
			p = figure(title = "Adjusted closing price",x_axis_label = 'Date', x_axis_type = "datetime",y_axis_label = 'Price')
			p.line(dates,adjusted,legend = "Adj.Close", line_width = 1)
			html = file_html (p,CDN,'my plot')
			script, div = components(p)
			#return html
			return render_template('plot.html',script = script, div = div)


if __name__ == "__main__":
    app.run(debug=True,port=33507)
