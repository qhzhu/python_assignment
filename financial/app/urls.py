from django.urls import path
from app.views import get_financial_data
from app.views import get_statistics

urlpatterns = [
    path('financial_data', get_financial_data, name='get_financial_data'),
    path('statistics', get_statistics, name='statistics'),
]