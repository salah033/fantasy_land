from django.db import models

class Suppliers (models.Model) :
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to="suppliers/", blank=True, null=True, default='no_photo.png') 
    active = models.BooleanField(default=True)

    def __str__(self) : 
        return self.name
    
    class Meta : 
        verbose_name = 'Supplier'
    