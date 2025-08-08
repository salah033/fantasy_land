from django.db import models
from django.utils.timezone import now
#from supplier.models import Suppliers

class Categories (models.Model) : 

    name = models.CharField(max_length=50)

    @property
    def cat_name (self):
        return self.name

    def __str__(self) : 
        return f"{self.id} - {self.name}"
    
    class Meta : 
        verbose_name = 'Categorie'

class Products (models.Model) : 

    name = models.CharField(max_length=50)
    bare_code = models.CharField(max_length=20, unique=True)
    reference = models.CharField(max_length=20, unique=True)
    price = models.FloatField(max_length=10)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    quantity = models.IntegerField()
    designation = models.TextField(max_length=100,null=True, blank=True)
    abbreviation = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="products/", blank=True, null=True, default='no_photo.png') 
    active = models.BooleanField(default=True)
    supplier = models.ForeignKey('supplier.Suppliers', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(default=now, blank=True, null=True)

    def __str__(self) : 
        return self.name
    
    class Meta : 
        verbose_name = 'Product'


 