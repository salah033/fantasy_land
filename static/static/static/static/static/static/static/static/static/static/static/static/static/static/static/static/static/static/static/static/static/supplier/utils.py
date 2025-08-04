from .models import Suppliers 
def all_suppliers () : 
    all_suppliers = Suppliers.objects.all()
    return all_suppliers