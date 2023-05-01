from django.contrib import admin

from . models import Portfolio, Transaction

@admin.register(Portfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'currency','initial_balance')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'type',"trans_date", 'symbol','trans_units')
