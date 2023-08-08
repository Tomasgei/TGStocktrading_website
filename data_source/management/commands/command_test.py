from django.core.management.base import BaseCommand
from django.utils import timezone
import yfinance as yf
import pandas as pd
from data_source . models import DataVendor, Instrument, HistoricalData

from datetime import datetime as dt

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate database by historical price data'

    def handle(self, *args, **kwargs):
        
        instrument = Instrument.objects.get(pk="LEN")  
        
        #date_str = '2023-02-28'
        date_format = '%Y-%m-%d'
        #date_obj = dt.strptime(date_str, date_format)
        
        items = [
        HistoricalData(ticker=instrument, date = '2019-02-28', open= "46.79" , close = "24.21" ),
        HistoricalData(ticker=instrument, date = '2019-02-22', open= "46.65", close= "25.50" ),
        HistoricalData(ticker=instrument, date = '2019-02-01', open= "46.75", close= "20.55" ),
        

        ]    
            
        HistoricalData.objects.bulk_update_or_create(items ,
                                                     update_fields=["open","close"],
                                                     match_field= "date")
        
