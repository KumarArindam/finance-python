import bs4 as bs
import pickle
import pandas
import urllib
import datetime as dt
import pandas_datareader as web
import os                 # os is to check for, and create directory

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def save_sp500_tickers():
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    
    soup = bs.BeautifulSoup(respData,'lxml')
    
    ## finding the tables
    table  = soup.find('table',{'class':'wikitable sortable'})
    ## iterating through the table
    tickers=[]
    
    for row in table.findAll('tr')[1:]:     # excluding the first row
        ticker = row.find_all('td')[0].text     ## zeroth column
        tickers.append(ticker)
        
    f = open('ticker_wiki.pickle','wb')
    pickle.dump(tickers,f)
    f.close()
    
    return tickers
        
    #print(tickers)    --  saving it the form of a pickle so that we donot have to access wikipedia everytime
#save_sp500_tickers()

def get_data_from_morningstar(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers
    
    else:
        with open('ticker_wiki.pickle','rb') as f:
            tickers = pickle.load(f)
    
    # creating a new dorectory to store the stock data
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2010,1,1)
    end = dt.datetime.now()
    
    for ticker in tickers[:30]:   # the first thirty tickers
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
           
            df = web.DataReader(ticker,'morningstar',start,end)

            df.reset_index(inplace= True)
            df.set_index('Date',inplace=True)
            
            df=df.drop('Symbol',1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            
        else:
            print('{} is already present'.format(ticker))

get_data_from_morningstar()