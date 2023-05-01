from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

import logging
from . models import Portfolio,Transaction
from . portfolio import PortfolioStats
from . portfolio import get_qoute
from . forms import AddTransactionForm

logger = logging.getLogger(__name__)

def portfolio_home(request,pk):

    # get buy
    buy_lts = Transaction.objects.filter(type="BUY")
    portfolio_balance = []
    for t in buy_lts:
        amount = t.trans_units * t.trans_price
        portfolio_balance.append(amount)
        
    portfolio = get_object_or_404(Portfolio,pk=pk)
    ptf_transactions = Transaction.objects.filter(portfolio=portfolio)
    
    if ptf_transactions.exists():
        ptf = PortfolioStats(portfolio.name,portfolio.initial_balance,portfolio.currency,ptf_transactions)
        ptf_stats = ptf.get_trans_as_dict()
        ptf_df = ptf.get_trans_as_df()
        ptf_op = ptf.get_open_positions()
        ptf_op_det = ptf.get_open_positions_detail()
    

    
    # Form for adding transactions
    form = AddTransactionForm()
    if request.method == "POST":
        if "add_transaction" in request.POST:
            add_trans_form = AddTransactionForm(request.POST)
            if add_trans_form.is_valid():
                add_trans_form.save()
                logger.info("Adding transaction " + str(request.POST))
                return redirect("portfolio:portfolio_home",pk=pk)
    
    
    context = {
            "portfolio":portfolio,
            "ptf_transactions":ptf_transactions,
            "ptf_id":pk,
            "form":form,
            "ptf_stats":ptf_stats,
            "ptf_df":ptf_df,
            "ptf_op":ptf_op,
            "ptf_op_det":ptf_op_det,   
            }
    
    logger.info("Tohle je test loggingu")
    return render(request,"portfolio/portfolio_home.html", context)


def transaction_delete(request,ptf_id,pk):
    trans = Transaction.objects.get(pk=pk)
    trans.delete()
    logger.info("Deleting transaction " + str(pk) )
    return redirect("portfolio:portfolio_home",pk=ptf_id)

def transaction_update(request,ptf_id,pk):
    trans = Transaction.objects.get(pk=pk)
    form = AddTransactionForm(instance=trans)
    pass
