import json
import logging
from . ledger import Ledger
from celery import shared_task
from . models import Portfolio,Transaction

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def recalculate_portfolio(self):
    portfolio = Portfolio.objects.get(pk=6)
    print(portfolio)

    #for p in portfolio:
    # pokud pro vybrané portfolio existují nějaké transakce
    if Transaction.objects.filter(portfolio=portfolio).exists():
        logger.info(f"Starting calculation for portfolio: {portfolio}, id:{portfolio.pk}")
        portfolio_transactions = Transaction.objects.filter(portfolio=portfolio)
        #založ pro portfolio instanci
        ledger = Ledger(portfolio.name,
                        portfolio.currency)
        
        for t in portfolio_transactions:
            # zaregistruj všechny transakce navázané na potrfolio
            # a spočítej otevřené pozice portfolia
            transaction = ledger.register_transaction(t.type, t.symbol,t.trans_units,t.trans_date,t.trans_price)
            logger.info(f"Registering transaction: {transaction }")
            
        logger.info(f"Registered all transactions")
        #Získej seznam otevřených pozic a jejich hodnot
        holdings = ledger.get_holdings()
        portfolio.open_positions = json.dumps(holdings)
        portfolio.save()
        logger.info(f"Calculated actual portfolio holdings:{holdings}")
        
        # ulož otevřené pozice do databáze
        
        #Vypočítej portfolio křivku
        portfolio_equity_ts = ledger.get_ts()
        print(portfolio_equity_ts.to_json())
        portfolio.portfolio_equity = portfolio_equity_ts.to_json()
        portfolio.save()
        logger.info(f"Portfolio equity was inserted in database")