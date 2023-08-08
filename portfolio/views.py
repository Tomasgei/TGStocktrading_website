from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import json
import logging
from . models import Portfolio,Transaction
from . portfolio import PortfolioStats
from . forms import AddTransactionForm
from . import iexapi
import pandas as pd
from data_source.models import DataVendor,Instrument,HistoricalData
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from portfolio.ledger import get_price
from . tasks import recalculate_portfolio
from accounts.tasks import send_mail_func

User = get_user_model()
api = iexapi.IEXAPI()
logger = logging.getLogger(__name__)



def index_volt(request):
    context = {}
    return render(request,"volt_templates/core/dashboard.html", context)

def instrument_detail(request, slug):
    
    instrument = Instrument.objects.get(ticker=slug)
    
    context = {"instrument":instrument}
    return render(request,"volt_templates/core/instrument_detail.html", context)

@login_required
def portfolio_dashboard(request):
    send_mail_func.delay()
    user= request.user
    if Portfolio.objects.filter(user=user).exists():
        portfolio = Portfolio.objects.filter(user=user)
    else:
        portfolio = ""
    
    context = {"portfolio":portfolio}
    return render(request,"volt_templates/core/dashboard.html", context)


@login_required
def portfolio_home(request,pk):
    #get user data
    user= request.user
    
    # Form for adding transactions
    form = AddTransactionForm()
    
    if Portfolio.objects.filter(user=user).exists():
        portfolio = Portfolio.objects.filter(user=user)
        # get portfolio data
        selected_portfolio = Portfolio.objects.get(id=pk)
    
        if Transaction.objects.filter(portfolio=selected_portfolio).exists():
            
            # Create portfolio instance
            start_date = '2019-01-01' #Input
            end_date = '2021-12-31'#Input
            transactions = Transaction.objects.filter(portfolio=selected_portfolio)
            #recalculate_portfolio.delay()
            
            ptf = PortfolioStats(selected_portfolio.name,
                                selected_portfolio.initial_balance,
                                selected_portfolio.currency,
                                transactions,
                                start_date,
                                end_date)
                    
            open_positions = ptf.get_open_positions()
            news = ptf.get_news_for_positions()
            #quotes = ptf.get_open_position_prices()
            #quotes = quotes.to_json()
            inst = Instrument.objects.filter(ticker__in =open_positions[1])
            
            id_list = []
            for i in inst:
                id_list.append(i.pk)
            logger.info(f"id: {id_list }")

            # query for historical data Apex chart
            stockdata = HistoricalData.objects.filter(ticker="AMC").values_list("adj_close", flat=True).order_by("date")
            datedata = HistoricalData.objects.filter(ticker="AMC").values_list("date", flat=True).order_by("date")
            hist_data = list(stockdata)
            date = list(datedata)
            dates = [date_obj.strftime('%Y/%m/%d') for date_obj in date]
            
            pe = Portfolio.objects.get(pk=selected_portfolio.pk).portfolio_equity
            portfolio_equity = json.loads(pe)
            portfolio_equity_dates = list(portfolio_equity.keys())
            portfolio_equity_values = list(portfolio_equity.values())
            
            
            holdings = Portfolio.objects.get(pk=selected_portfolio.pk).open_positions
            df = pd.read_json(holdings).transpose()
            df["pps"].loc["USD"] = 1
            df["current_price"] = [df.pps.loc["USD"]] + [get_price(x) for x in df.index[1:]]
            df["equity"] = df.current_price * df.shares
            holdings_sym = list(df.index)
            holdings_val = list(df.equity)
            
            

            context = {
            "portfolio":portfolio,
            "selected_portfolio":selected_portfolio,
            "transactions":transactions,
            "open_positions":open_positions,
            "quotes":"",
            "news":news,
            "hist_data":hist_data,
            "date_data":dates,
            "form":form,
            "portfolio_equity_dates":portfolio_equity_dates,
            "portfolio_equity_values":portfolio_equity_values,
            "holdings_sym":holdings_sym,
            "holdings_val":holdings_val
    
            }

            logger.info(f"portfolios selected for user selected: {selected_portfolio}")

            return render(request,"volt_templates/core/portfolio.html", context)
        else:
            
            
            context = {}
            # in template if portfolio = 0  empty render Call To action to Create new portfolio
        return render(request,"volt_templates/core/portfolio.html", context)
    # get buy
    #buy_lts = Transaction.objects.filter(type="BUY")
    #portfolio_balance = []
    #for t in buy_lts:
    #    amount = t.trans_units * t.trans_price
    #    portfolio_balance.append(amount)
        
    
    #ptf_transactions = Transaction.objects.filter(portfolio=portfolio)
    
    #if ptf_transactions.exists():
    #    ptf = PortfolioStats(portfolio.name,portfolio.initial_balance,portfolio.currency,ptf_transactions)
    #    ptf_stats = ptf.get_trans_as_dict()
    #    ptf_df = ptf.get_trans_as_df()
    #    ptf_op = ptf.get_open_positions()
    #    ptf_op_det = ptf.get_open_positions_detail()
    

    """
    # Form for adding transactions
    form = AddTransactionForm()
    if request.method == "POST":
        if "add_transaction" in request.POST:
            add_trans_form = AddTransactionForm(request.POST)
            if add_trans_form.is_valid():
                add_trans_form.save()
                logger.info("Adding transaction " + str(request.POST))
                return redirect("portfolio:portfolio_home")
    """
def add_transaction(request):
    form = AddTransactionForm()
    if request.method == "POST":
        add_form = AddTransactionForm(request.POST)
        add_form.errors
        print("TSDDKLASDKLASKDALKDSLDKALSKSALASKDSALDKSADL")
        if form.is_valid():
            print(add_form.cleaned_data["portfolio"])
            print(add_form.cleaned_data["type"])
            add_form.cleaned_data["symbol"]
            add_form.cleaned_data["trans_units"]
    
    context = {"form":form}
    return  render(request,"volt_templates/core/transaction.html", context)


def transaction_delete(request,ptf_id,pk):
    trans = Transaction.objects.get(pk=pk)
    trans.delete()
    logger.info("Deleting transaction " + str(pk) )
    return redirect("portfolio:portfolio_home",pk=ptf_id)

def transaction_update(request,ptf_id,pk):
    trans = Transaction.objects.get(pk=pk)
    form = AddTransactionForm(instance=trans)
    pass



def portfolio_home_2(request):

    
    #stock_list = ['BAC', 'C', 'HIG', 'LEN', 'MS'] #Input
    start_date = '2019-01-01' #Input
    end_date = '2021-12-31'#Input
    

    context = {}
    return render(request,"portfolio/portfolio_home.html", context)