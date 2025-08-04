from django.db import models
from django.utils import timezone


class Sale(models.Model):
    date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Sale #{self.id} - {self.date.strftime('%d/%m/%Y %H:%M')}" 
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    
