from django.db import models

# Create your models here.
class FinancialDataModel(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=20)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=20, decimal_places=2)
    close_price = models.DecimalField(max_digits=20, decimal_places=2)
    volume = models.IntegerField()

    def __str__(self):
        return self.symbol
    
    class Meta:
        db_table = "financial_data"
        unique_together = ['symbol', 'date']

