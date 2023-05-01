from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path('<int:ptf_id>/transaction/<int:pk>/delete/',views.transaction_delete, name="transaction_delete" ),
    path('<int:ptf_id>/transaction/<int:pk>/update/',views.transaction_update, name="transaction_update" ),
    path('<int:pk>/',views.portfolio_home, name="portfolio_home" ),
    

]
