import numpy as np
import pandas as pd
import requests
import yfinance as yf
from . import iexapi
api = iexapi.IEXAPI()

class PortfolioStats:
    def __init__(self, name, init_balance, currency, list_of_transactions, start_date, end_date) -> None:
        self.name = name 
        self.init_balance = init_balance
        self.currency = currency
        self.transactions = list_of_transactions
        self.start_date = start_date
        self.end_date = end_date
        
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
        open_pos_list = list(open_pos['trans_units'].keys())
        trans = self.get_trans_as_dict()
        print(trans)
        
        open_positions = []

        for position in open_pos["trans_units"]:
            buy_transactions = {}
            for transaction in trans :
                if transaction["type"] == "BUY" and transaction["symbol"] == position:
                    symbol = transaction["symbol"]
                    price = transaction["trans_price"]
                    units = transaction["trans_units"]
                    if symbol in buy_transactions:
                        buy_transactions[symbol]["total_cost"] += price * units
                        buy_transactions[symbol]["total_units"] += units
                    else:
                        buy_transactions[symbol] = {"total_cost": price * units, "total_units": units}
                
                
            for symbol, data in buy_transactions.items():
                portfolio_pos = {}
                avg_price = data["total_cost"] / data["total_units"]
                data["avg_price"] = avg_price
                portfolio_pos["symbol"] = symbol
                portfolio_pos["avg_price"] = data["avg_price"]
                portfolio_pos["open_pos"] = open_pos["trans_units"][symbol]
                portfolio_pos["cost_basis"] = portfolio_pos["avg_price"]*portfolio_pos["open_pos"]
                #quote = api.get_quote_field(symbol)
                try:
                    quote = yf.download(symbol, period="1d")
                    portfolio_pos["quote"] = quote["Adj Close"].iloc[0]
                    portfolio_pos["market_value"] = portfolio_pos["open_pos"] * portfolio_pos["quote"] 
                except:
                    portfolio_pos["quote"]=""
                    portfolio_pos["market_value"] =""
                    
                open_positions.append(portfolio_pos)
                print(f"Symbol: {symbol}, Average Buy Price: {avg_price:.2f}")

        return open_positions,open_pos_list
    
    def get_news_for_positions(self):
        stock_list = self.get_open_positions()[1]
        data = yf.Ticker("PBR")
        news = data.news[0:6]
        return news
    
    
    def get_open_position_prices(self):
        stock_list = self.get_open_positions()[1]
        # Stažení dat z Yahoo Finance
        data = yf.download(stock_list, period="1d")["Adj Close"]
        return data