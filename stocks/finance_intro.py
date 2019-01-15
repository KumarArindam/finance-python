import datetime as dt  			# to work with the dates
import pandas as pd
import pandas_datareader.data as web        # to deal with the finance data.
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')  		# in finance we style the graphs to look pretty for the analysis

start = dt.datetime(2018,1,1)
end = dt.datetime.now()

# The DataReader looks for the stock ticker TSLA(tesla), gets the info from morningstar from the start to the end time specified here
df = web.DataReader('TSLA','morningstar',start,end) 

df.reset_index(inplace=True)		# here we need to reset the index or else we get an error
df.set_index('Date',inplace=True)
df.drop('Symbol',1)

## 	Adj Close is helpful, since it accounts for future stock splits, and gives the relative price to splits. 
## 	For this reason, the adjusted prices are the prices you're most likely to be dealing with.

##df.to_csv('tesla.csv')
print(df.head())