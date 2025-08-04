from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class UserNote (models.Model) : 
    
    type = models.CharField(default='Note')
    employee = models.ForeignKey(User, related_name= 'user_note', on_delete=models.CASCADE)
    body = models.TextField()
    date_create = models.DateField(default=now, blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} from {self.employee} at {self.date_create}"
    
    class Meta : 
        verbose_name = 'Note'
    
class UserShopOrder (models.Model) : 

    type = models.CharField(default='Shop Order')
    employee = models.ForeignKey(User, related_name='shop_order', on_delete=models.CASCADE)
    order_date = models.DateField(blank=True, null=True)
    prod_order_name = models.CharField()
    prod_order_qty = models.IntegerField(blank=True, null= True)
    body = models.TextField(blank=True, null=True)
    date_create = models.DateField(default=now, blank=True, null=True)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.type} from, {self.employee} | {self.prod_order_name} at, {self.order_date}"
    
    class Meta : 
        verbose_name = 'Shop order'

class UserCustomer (models.Model) : 
    type = models.CharField(default='Customer') 
    employee = models.ForeignKey(User, related_name='user_customer', on_delete=models.CASCADE)
    customer_name = models.CharField() 
    customer_phone = models.CharField() 
    body = models.TextField(blank=True, null=True)  
    date_create = models.DateField(default=now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.type} from, {self.employee} | Name : {self.customer_name} ,Phone : {self.customer_phone}"
    
    class Meta : 
        verbose_name = 'Customer'
    
class UserCustomerOrder (models.Model) : 
    type = models.CharField(default='Customer Order') 
    employee = models.ForeignKey(User, related_name='user_customer_order', on_delete=models.CASCADE)    
    customer_name = models.CharField() 
    customer_phone = models.CharField() 
    product_order = models.CharField() 
    is_paid = models.BooleanField(default=False)
    amount_paid = models.IntegerField(null=True, blank=True)
    order_date = models.DateField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)  
    date_create = models.DateField(default=now, blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} from {self.employee} | Name : {self.customer_name} ,Phone : {self.customer_phone} ,Product : {self.product_order}"
    
    class Meta : 
        verbose_name = 'Customer Order'