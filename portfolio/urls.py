from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path('<int:ptf_id>/transaction/<int:pk>/delete/',views.transaction_delete, name="transaction_delete" ),
    path('<int:ptf_id>/transaction/<int:pk>/update/',views.transaction_update, name="transaction_update" ),
    path('detail/<str:pk>/',views.portfolio_home, name="portfolio_home" ),
    path('addtransaction/',views.add_transaction, name="add_transaction" ),
    path('dashboard/',views.portfolio_dashboard, name="dashboard" ),
    path('<str:slug>/',views.instrument_detail, name="instrument_detail" ),
    path('volt/',views.index_volt, name="volt_home" ),
    

]
