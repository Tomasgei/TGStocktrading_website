from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
import yfinance as yf
import pandas as pd
from data_source . models import DataVendor, Instrument, HistoricalData
from datetime import datetime as dt

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
))

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate database by historical price data'

    def handle(self, *args, **kwargs):
        
        # Načtení dat o akciích
        tickers= ["BTU"]
        for t in tickers:
            ticker = t
            logger.info(f"DB qeuery for: {ticker}")
            instrument = Instrument.objects.filter(slug=ticker)
            if instrument.exists():
                logger.info(f"{ticker} is already in database")
                hist_data = HistoricalData.objects.filter(pk=instrument.pk)
                if hist_data.exists():
                    # get latest date of existing data
                    start_date = hist_data.order_by("-date")[0]
                    end_date = date.today()
                    prices = yf.download(ticker, start=start_date.date , end=end_date)
                    logger.info(f"Data downloded for: {ticker} sucessfully")
                    data.columns  = data.columns.str.lower()
                    records = data.to_dict(orient='records')
                    print(len(records))
                else:
                    pass
            else:        
                prices = yf.download(ticker, start=start_date , end=end_date)
                logger.info(f"Data downloded for: {ticker} sucessfully")
                data = prices.reset_index()
                data.columns  = data.columns.str.lower()
                records = data.to_dict(orient='records')
                print(len(records))

                #delete_data = HistoricalData.objects.all()
                #delete_data.delete()
                vendor = DataVendor.objects.get(pk=1)  
                #instrument = Instrument.objects.get(pk=i_obj.pk)  
                
                i_obj, i_created = Instrument.objects.update_or_create(
                    ticker = ticker , defaults={"vendor":vendor}, 
                )
                
                #date_str = '2023-02-28'
                date_format = '%Y-%m-%d'
                #date_obj = dt.strptime(date_str, date_format)
            
                bulk_objects = []
                for r in records:
                    bulk_objects.append(HistoricalData( 
                                        ticker = i_obj,
                                        date = pd.to_datetime(r["date"]) ,
                                        open = round(r["open"],3),
                                        high = round(r["high"],3),
                                        low = round(r["low"],3),
                                        close = round(r["close"],3),
                                        adj_close = round(r["adj close"],3),
                                        volume = r["volume"]
                                        ))
                
                HistoricalData.objects.bulk_update_or_create(bulk_objects ,update_fields=["date","open","close"] , match_field=["ticker"])
                logger.info(f"Data created in DB: {ticker}")
        
