from django.forms import ModelForm
from django import forms
from .models import Transaction,Portfolio
from . tasks import recalculate_portfolio

class AddTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["portfolio",
                  "type",
                  "symbol",
                  "trans_units",
                  "trans_date",
                  "trans_price",
                  "commision"]
        
        widgets = { "portfolio" : forms.Select(attrs={'class' : 'form-control'}),
                    "type" : forms.Select(attrs={'class' : 'form-control'}),
                    "symbol" : forms.TextInput(attrs={'class' : 'form-control'}),
                    "trans_units" : forms.NumberInput(attrs={'class' : 'form-control'}),
                    "trans_date" : forms.SelectDateWidget(attrs={'class' : 'form-control', "id":"datetimepicker1","placeholder":"dd/mm/yyyy"}),
                    "trans_price" : forms.NumberInput(attrs={'class' : 'form-control'}),
                    "commision" : forms.NumberInput(attrs={'class' : 'form-control'}),
                   }
        
        #def update_portfolio(self):
         #   recalculate_portfolio.delay()
