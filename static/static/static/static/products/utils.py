from .models import Products 
def all_products () : 
    all_products = Products.objects.all()
    return all_products