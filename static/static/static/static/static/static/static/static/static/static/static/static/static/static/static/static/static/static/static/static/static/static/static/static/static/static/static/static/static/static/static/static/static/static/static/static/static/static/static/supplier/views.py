from django.shortcuts import render , get_object_or_404
from .models import Suppliers 
from django.contrib.auth.decorators import login_required

@login_required
def suppliers (request) : 

    all_suppliers = {'supplier' : Suppliers.objects.filter(active=True)}

    return render (request, "suppliers/all_suppliers.html", all_suppliers)

@login_required
def supplier_detail (request, pk) :
    
    supplier = get_object_or_404(Suppliers, pk=pk)
    products =  supplier.products_set.filter(active=True)
    return render(request, "suppliers/supplier_detail.html", {'supplier': supplier, 'products': products})