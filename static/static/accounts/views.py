from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserNote,UserShopOrder,UserCustomer,UserCustomerOrder
from datetime import datetime

@login_required
def accounts_home(request) :
    return render (request , 'accounts/home.html')

def accounts_login(request) :
    
    next_url = request.GET.get('next', '/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)  
        else:
            messages.error(request, 'Invalid username or password.')
    
    next_url = next_url.split("/")
    next_url = next_url[-2].capitalize()

    return render(request, 'accounts/login.html', {'next': next_url})

def accounts_register(request) :
    return render (request , 'accounts/register.html')

@login_required
def accounts_logout (request) : 
    print ("LOGOUT_WORKING")
    if request.method == "POST":
        
        logout(request)
        return JsonResponse({'redirect_url': reverse('ACCOUNTS_LOGIN')})
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def user_dashboard (request) : 
    return render (request, 'accounts/dashboard.html')

@login_required
def memo_form (request) : 
    return render (request, 'accounts/memo.html')

@login_required
@csrf_exempt
def submit_user_note (request) : 
    if request.method == 'POST':
        user_name = request.user

        selected_type = request.POST.get('type')
        if selected_type == 'note' :
            
            body = request.POST.get('noteInput', '')
            if not body : 
                return HttpResponse("Plese fill the Required fields*")

            isdone = request.POST.get('is_done_note') == 'on'
            form  = UserNote.objects.create(employee=user_name,
                                            body=body,
                                            is_done=isdone)
            form.save()

        elif selected_type == 'shop_order' :
            
            order_date_str = request.POST.get('shop_order_date', '').strip()
            if order_date_str:
                try:
                    order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
            else:
                order_date = None

            prod_name = request.POST.get('product_name', '')
            if not prod_name : 
                return HttpResponse("Plese fill the Required fields*")
            try:
                prod_qty = int(request.POST.get('quantity', 0) or 0)
            except ValueError:
                prod_qty = 0
            body = request.POST.get('shop_order_notes', '')
            isdone = request.POST.get('is_done_shop_order') == 'on'
            form = UserShopOrder.objects.create(employee=user_name,
                                           order_date=order_date,
                                           prod_order_name=prod_name,
                                           prod_order_qty=prod_qty,
                                           body=body,
                                           is_done=isdone)
            form.save()

        elif selected_type == 'customer' :
            cus_name = request.POST.get('customer_name','')
            cus_phone = request.POST.get('customer_phone','')
            if not cus_phone or not cus_phone : 
                return HttpResponse("Plese fill the Required fields*")
            body = request.POST.get('customer_notes','')
            form = UserCustomer.objects.create(employee=user_name,
                                               customer_name=cus_name,
                                               customer_phone=cus_phone,
                                               body=body)
            form.save()
        
        else : 
            order_date_str = request.POST.get('customer_order_date', '').strip()
            if order_date_str:
                try:
                    order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
            else:
                order_date = None
            
            cus_name = request.POST.get('customer_order_name','')
            cus_phone = request.POST.get('customer_order_phone','')
            product = request.POST.get('order_product','')
            if not cus_name or not cus_phone or not product: 
                return HttpResponse("Plese fill the Required fields*")
            ispaid = request.POST.get('is_paid') == 'on' 
            if not ispaid : 
                amount = 0
            else : 
                try:
                    amount = int(request.POST.get('amount_paid', 0) or 0)
                except ValueError:
                    amount = 0
            body = request.POST.get('order_notes','')
            isdone = request.POST.get('is_done_cust_order') == 'on'
            form = UserCustomerOrder.objects.create(employee=user_name,
                                                    customer_name=cus_name,
                                                    customer_phone=cus_phone,
                                                    product_order=product,
                                                    is_paid=ispaid,
                                                    amount_paid=amount,
                                                    order_date=order_date,
                                                    body=body,
                                                    is_done=isdone)
            form.save()

        return render (request, 'accounts/submitted.html')
@csrf_exempt
@login_required
def show_memos (request) :
    if request.method == 'POST' : 
        print ("POST")
        selected_type = request.POST.get('category') 

        if selected_type == 'notes' :
            print ("NOTES")
        elif selected_type == 'shop_orders' :
            print("SHOP_ORDERS")
        elif selected_type == 'customers' :
            print ("Customers")
        else  :
            print("Customers_order")


    return render (request, 'accounts/show_memo.html')
# Create your views here.
