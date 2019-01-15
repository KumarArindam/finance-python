import pickle
import pandas as pd

### Since we do not have the adjusted close so we will use the close for now

def compile_data():
    with open('ticker_wiki.pickle','rb') as f:
        tickers = pickle.load(f)      ## list of the tickers

    main_df = pd.DataFrame()       ## empty dataframe

    for count,ticker in enumerate(tickers[:30]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))

        df.set_index('Date',inplace=True)

        ## we can also do the following for information
        ##  df['{}_HL_diff_pct'.format(ticker)] = (df['High']-df['Low'])/df['Low']
        ##  df['{}_daily_chn_pct'.format(ticker)] = (df['Close']-df['Open'])/df['Open']

        df.rename(columns={'Close':ticker},inplace=True)                    ## renaming the  close column to ticker.
        df.drop(['Open','High','Low','Volume'],1,inplace=True)

        if main_df.empty:
            main_df=df

        else:
            main_df = main_df.join(df,how='outer')          ## when using outer there may be overlap but we do this to avoid any loss of data

        if count%10 == 0:           ## so that we donot print everything and only the ones which are in the multiples of 10
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_tickers_joined.csv')

compile_data()