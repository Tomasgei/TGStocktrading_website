import numpy as np
import pandas as pd
import requests

def get_qoute(symbol):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
    r = requests.get(url)
    data = r.json()
    d = data['Global Quote']['05. price']
    return d


class PortfolioStats:
    def __init__(self,name, init_balance,currency, list_of_transactions) -> None:
        self.name = name 
        self.init_balance = init_balance
        self.currency = currency
        self.transactions = list_of_transactions
        self.start_date = ""
        self.end_date = ""
        
    def get_trans_as_dict(self):
        trans_list = []
        trans = self.transactions 
        for i in range(len(trans)):
            trans_dict = {}
            trans_dict["type"] = trans[i].type
            trans_dict["symbol"] = trans[i].symbol
            trans_dict["trans_units"] = trans[i].trans_units
            trans_dict["trans_date"] = trans[i].trans_date
            trans_dict["trans_price"] = trans[i].trans_price
            trans_dict["commision"] = trans[i].commision
            trans_list.append(trans_dict) 
        return trans_list
    
    def get_trans_as_df(self):
        trans = pd.DataFrame.from_dict(self.get_trans_as_dict()) 
        trans["trans_date"] = pd.to_datetime(trans["trans_date"])
        trans["trans_units"] = np.where( trans["type"]=="SELL",-trans["trans_units"],trans["trans_units"]  )
        #trans["cost_basis"] = trans["units"] * trans["entry_price"]
        trans.set_index("trans_date")
        return trans
    
    def get_open_positions(self):
        transactions = self.get_trans_as_df()
        trans_data = transactions[["symbol","trans_units"]]
        tdf = trans_data.groupby("symbol").sum()
        non_zero_pos = tdf["trans_units"] > 0
        tdf = tdf[non_zero_pos]
        open_pos =  tdf.to_dict()
        return open_pos
    
    def get_open_positions_detail(self):
        open_pos = self.get_open_positions()
        x = open_pos["trans_units"]
        portfolio_positions = []

        for key in x:
            position_dictionary = {} 
            df = self.get_trans_as_df()
            symbol_filter = df.symbol == key
            symbol_transactions = df[symbol_filter]
            symbol_transactions = symbol_transactions.copy()
            trailing_units = symbol_transactions.trans_units.cumsum()
            trailing_buys = symbol_transactions.type == "BUY"
            entry_price_sum = symbol_transactions.trans_price.cumsum()
            invested_amount = symbol_transactions.trans_price.multiply(symbol_transactions.trans_units)

            symbol_transactions["invested_amount"] = invested_amount
            symbol_transactions["total_invested_amount"] = invested_amount.cumsum()
            symbol_transactions["trailing_units"] = trailing_units
            ab = symbol_transactions["total_invested_amount"].divide(symbol_transactions.trailing_units)
            symbol_transactions["trailing_buys"] = trailing_buys.cumsum()
            symbol_transactions["avg_purchase_price"] = symbol_transactions["total_invested_amount"].divide(symbol_transactions.trailing_units)
    
            # create open positions stats
            position_dictionary["ticker"] = key
            position_dictionary["units"] = trailing_units.iloc[-1]
            position_dictionary["avg_price"] = symbol_transactions["avg_purchase_price"].iloc[-1]
            position_dictionary["cost_basis"] = position_dictionary["units"] * position_dictionary["avg_price"]
            portfolio_positions.append(position_dictionary)
            
        return portfolio_positions
        