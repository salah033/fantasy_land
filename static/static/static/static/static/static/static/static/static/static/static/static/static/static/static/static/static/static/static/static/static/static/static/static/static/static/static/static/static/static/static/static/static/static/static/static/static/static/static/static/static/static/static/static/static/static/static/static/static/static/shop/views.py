from django.shortcuts import render
from django.http import JsonResponse
#from .utils import get_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@login_required
def shop_home (request) : 
    return render (request, "shop/shop.html")

'''
@csrf_exempt
def chatbot_ask (request) : 
    
    if request.method == "POST":
        message = request.POST.get("message", "")
        
        response = get_response(message)
        return JsonResponse({"response": response})'''