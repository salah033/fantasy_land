from django.shortcuts import render, get_object_or_404
from .models import Products
from django.contrib.auth.decorators import login_required

@login_required
def products (request) :
    
    all_products = {'product' : Products.objects.filter(active=True)}

    return render (request, "products/all_products.html", all_products)

@login_required
def product_detail (request, pk) : 

    product = get_object_or_404(Products, pk=pk)

    return render(request, "products/product_detail.html", {'product': product})



# Create your views here.
