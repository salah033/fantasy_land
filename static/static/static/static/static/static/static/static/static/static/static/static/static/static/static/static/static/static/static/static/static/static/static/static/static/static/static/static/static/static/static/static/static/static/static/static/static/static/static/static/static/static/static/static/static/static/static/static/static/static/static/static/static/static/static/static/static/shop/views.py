from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def shop_home (request) : 
    return render (request, "shop/shop.html")

