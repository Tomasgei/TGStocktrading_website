from django.contrib import admin
from . models import DataVendor,Instrument,HistoricalData
# Register your models here.



admin.site.register(DataVendor)
admin.site.register(Instrument)
#admin.site.register(HistoricalData)


@admin.register(HistoricalData)
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = ("ticker",'date', 'open', 'high', 'low', 'close','volume')
