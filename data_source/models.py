from django.db import models
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

# Create your models here.
class DataVendor(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, verbose_name= _("Data Vendor"))
    
    def __str__(self):
        return self.name


"""   
class AssetClass(models.Model):
    ASSET_TYPE = (
        ("STOCK", _("Stock")),
        ("ETF", _("Etf")),
        ("COMMODITY", _("Commodity")),
        ("CRYPTO", _("Crypto")),
        ("FOREX", _("Currency")),
    )
    name = models.CharField(max_length=200, unique=True, blank=False, choices=ASSET_TYPE, verbose_name= _("Asset Class"))
    def __str__(self):
        return self.name
"""
    
class Instrument(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    vendor = models.ForeignKey(DataVendor, verbose_name=_("Data Vendor"), on_delete=models.CASCADE)
    ticker = models.CharField(primary_key= True, max_length=10, unique=True, blank=False, verbose_name= _("ticker"))
    
    def __str__(self):
        return self.ticker
    

class HistoricalData(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    ticker = models.ForeignKey(Instrument, verbose_name=_("Instrument"), on_delete=models.CASCADE)
    date = models.DateField( null=False, blank=False )
    open = models.FloatField(null=True, blank=True )
    high = models.FloatField(null=True, blank=True )
    low = models.FloatField(null=True, blank=True )
    close = models.FloatField(null=True, blank=True )
    adj_close = models.FloatField(null=True, blank=True )
    volume = models.BigIntegerField(null=True, blank=True )
    
    class Meta:
        verbose_name = _("Historical Data")
        verbose_name_plural = _("Historical Data")

    def __str__(self):
        return self.ticker.ticker
