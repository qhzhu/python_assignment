from rest_framework import serializers
from app.models import FinancialDataModel

class FinancialDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDataModel
        fields = ['symbol', 'date', 'open_price', 'close_price', 'volume']
        
        
# curl -X GET 'http://localhost:8000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'
