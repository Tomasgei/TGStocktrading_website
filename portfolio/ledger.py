import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import yfinance as yf
from yahoo_fin import stock_info as si
from pandas.core.tools.datetimes import to_datetime


def get_price(stock):
    try:
        return np.round(si.get_live_price(stock), decimals=2)
    except:
        print(f"{stock.upper()} is not a valid ticker")


def get_data(stock, start, end):
    try:
        stock_data = yf.download(stock, start=start, end=end)
        return stock_data["Adj Close"]
    except yf.errors.YFinanceError:
        print(f'No data found for {stock}.')


class Ledger:
    def __init__(self, name, currency):
        self.name = name
        self.transactions = []
        self.holdings = {"USD": 0}

    def get_holdings(self):
        return self.holdings

    def get_transactions(self):
        return self.transactions

    def register_transaction(self, transaction, symbol, shares, date, price):
        #price = np.round(price, decimals=2)
        cost_basis = price * shares
        transaction_info = {
            "type": transaction,
            "date": date,
            "symbol": symbol.upper(),
            "shares": shares,
            "pps": price,
            "total": cost_basis,
        }
        self.transactions.append(transaction_info)

        holdings = self.get_holdings()
        if transaction == "BUY":
            if symbol in holdings:
                holding = holdings[symbol]
                holdings["USD"] -= cost_basis if holdings["USD"] > cost_basis else holdings["USD"]
                holding["pps"] = ((holding["pps"] * holding["shares"] + cost_basis) / (holding["shares"] + shares))
                holding["shares"] += shares
            else:
                holdings[symbol] = {
                    "shares": shares,
                    "pps": price
                }
        elif transaction == "SELL":
            if symbol not in holdings:
                print(f"No holding found for {symbol} on {date}. Skipping sell transaction.")
                return

            holding = holdings[symbol]
            holdings["USD"] += cost_basis
            holding["shares"] -= shares
            if holding["shares"] == 0:
                del holdings[symbol]

    def get_ts(self):
        def get_portfolio(portfolio, start, end):
            series = pd.Series(dtype="float64")
            for symbol in portfolio.keys():
                s = get_data(symbol, start, end) * portfolio[symbol]
                if symbol == "USD":
                    continue
                series = series.add(s, fill_value=0)
            return series + portfolio["USD"]

        transactions = self.get_transactions()
        if not transactions:
            return pd.Series()

        dates = [t["date"] for t in transactions] + [dt.datetime.now().date()]
        dates = sorted(dates, key=lambda x: dt.datetime.combine(x, dt.datetime.min.time()))  # Sort dates to ensure the correct order
        portfolio = {"USD": 0}
        series = pd.Series(dtype="float64")

        for t in range(len(transactions)):
            tr = transactions[t]
            adj = 0
            if tr["type"] == "BUY":
                adj = -1 * (tr["total"] if portfolio["USD"] > tr["total"] else portfolio["USD"])
                if tr["symbol"] in portfolio:
                    portfolio[tr["symbol"]] += tr["shares"]
                else:
                    portfolio[tr["symbol"]] = tr["shares"]
            if tr["type"] == "SELL":
                portfolio["USD"] += tr["total"]
                portfolio[tr["symbol"]] -= tr["shares"]
            add = (tr["total"] - portfolio["USD"]) if tr["total"] > portfolio["USD"] else 0
            portfolio["USD"] += adj
            s = get_portfolio(portfolio, dates[t], dates[t + 1])
            # Convert RangeIndex to normal Index before appending the series
            s.index = s.index.astype(str)
            series = series._append(pd.Series([add], index=[str(s.index[0])]))._append(s)

        # return the series with duplicated index values removed
        return pd.Series([series.loc[x] if isinstance(series.loc[x], np.float64) else series.loc[x].values[0]
                        for x in series.index.unique()],
                        index=series.index.unique())