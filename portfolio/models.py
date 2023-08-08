#import jsonfield
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ , gettext as __
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Portfolio(models.Model):
    currency = (
        ("usd","USD"),
        ("eur","EUR"),
        ("czk","CZK"),   
    )
    
    user = models.ForeignKey(User,blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False, null=False)
    currency = models.CharField(max_length=3,choices=currency,default="usd")
    initial_balance = models.FloatField(blank=False, null=False, default=100000)
    portfolio_equity = models.JSONField(default=dict)
    open_positions = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("User Portfolio")
        verbose_name_plural = _("User Portfolios")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("user_portfolio", kwargs={"pk": self.pk})
    
    
    
class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ("BUY", _("Buy")),
        ("SELL", _("Sell")),
        ("DEPOSIT", _("Deposit")),
        ("WIDTHRAWAL", _("Widthrawal")),
        ("DIVIDEND", _("Dividend")),
    )
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE ,blank=False,null=False)
    type = models.CharField(max_length=32, choices=TRANSACTION_TYPE, default=None, blank=False,null=False,)
    symbol = models.CharField(max_length=10,blank=False,null=False) # TO DO: Instrument model Foreign key
    trans_units = models.BigIntegerField()
    trans_date = models.DateField(auto_now=False, auto_now_add=False,blank=False,null=False )
    trans_price = models.FloatField()
    commision = models.FloatField()

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        
    def __str__(self):
        return self.portfolio.name
