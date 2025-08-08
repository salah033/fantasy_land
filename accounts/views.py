from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserNote, UserShopOrder, UserCustomer, UserCustomerOrder
from datetime import datetime
from django.template.loader import render_to_string
from django.db.utils import IntegrityError

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
def accounts_logout(request):
    print("LOGOUT_WORKING")
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
                return HttpResponse("Please fill the Required fields*")

            form  = UserNote.objects.create(employee=user_name,
                                            body=body,)
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
                return HttpResponse("Please fill the Required fields*")
            try:
                prod_qty = int(request.POST.get('quantity', 1) or 1)
            except ValueError:
                prod_qty = 0
            body = request.POST.get('shop_order_notes', '')
            form = UserShopOrder.objects.create(employee=user_name,
                                           order_date=order_date,
                                           prod_order_name=prod_name,
                                           prod_order_qty=prod_qty,
                                           body=body,)
            form.save()

        elif selected_type == 'customer' :
            cus_name = request.POST.get('customer_name','')
            cus_phone = request.POST.get('customer_phone','')

            if not cus_phone or not cus_phone : 
                return HttpResponse("Please fill the Required fields*")
            body = request.POST.get('customer_notes','')
            try : 
                form = UserCustomer.objects.create(employee=user_name,
                                               customer_name=cus_name,
                                               customer_phone=cus_phone,
                                               body=body)
            except IntegrityError : 
                return HttpResponse("Phone number already exist")
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
            
            try:
                cus_id = int(request.POST.get('costumer_ID', None) or None)
            except ValueError:
                cus_id = None
            if not isinstance(cus_id, int): 
                return HttpResponse("Please fill the COSTUMER ID FIELD WITH NUMBERS ONLY***")
            
            costomer = get_object_or_404(UserCustomer, id=cus_id)            

            product = request.POST.get('order_product','')
            if not product or not cus_id : 
                return HttpResponse("Plese fill the Required fields*")
            ispaid = request.POST.get('is_paid') == 'on' 
            if not ispaid : 
                amount = 0
            else : 
                try:
                    amount = int(request.POST.get('amount_paid', 0) or 0)
                except ValueError:
                    amount = 0
            if amount == 0 and ispaid : 
                return HttpResponse("ERROR, Please enter the amount Paid in advance or uncheck Paid**")
                
            
            body = request.POST.get('order_notes','')
            #quantity = request.POST.get('cus_quantity')
            try:
                quantity = int(request.POST.get('cus_quantity', 1) or 1)
            except ValueError:
                quantity = 1
            form = UserCustomerOrder.objects.create(employee=user_name,
                                                    customer_exist=costomer,
                                                    product_order=product,
                                                    is_paid=ispaid,
                                                    amount_paid=amount,
                                                    order_date=order_date,
                                                    body=body,
                                                    quantity_order=quantity,)
            form.save()

        return render (request, 'accounts/submitted.html')

@csrf_exempt
@login_required
def show_memos (request) :
    #if request.method == 'GET':
        #print ('GET')
        #print (request.GET.get('id_input',''))
    if request.method == 'POST':
        category = request.POST.get('category')

        if category == 'notes':
            #x = request.GET.get('id_input','')
            #print (x)
            notes = UserNote.objects.filter(employee=request.user).order_by('is_done')
            html = render_to_string('accounts/partials/notes_section.html', {'notes': notes})
            return JsonResponse({'html': html})

        elif category == 'shop_orders':
            shop_orders = UserShopOrder.objects.all().order_by('is_done', 'date_create')
            html = render_to_string('accounts/partials/shop_orders_section.html', {"shop_orders" : shop_orders})
            return JsonResponse({'html': html})

        elif category == 'customers' : 
            customers = UserCustomer.objects.all().order_by('-date_create')
            html = render_to_string('accounts/partials/customers_section.html', {'customers': customers})
            return JsonResponse({'html': html})
        else : 
            customer_orders = UserCustomerOrder.objects.all().order_by('is_done', 'date_create')
            html = render_to_string('accounts/partials/customer_orders_section.html', {'customer_orders': customer_orders})
            return JsonResponse({'html': html})

    return render(request, "accounts/show_memo.html")

@csrf_exempt
@login_required
def edit_memo (request, category, pk) : 

    model_map = {
        'note': UserNote,
        'shop_order': UserShopOrder,
        'customer': UserCustomer,
        'customer_order': UserCustomerOrder,
    }
    model_class = model_map.get(category)
    if not model_class:
        return render(request, '404.html', status=404)
    
    obj = get_object_or_404(model_class, pk=pk)

    context = {"object" : obj}

    print (category)

    if request.method == 'POST' : 

        if category == 'note' : 
            body = request.POST.get("body")
            isdone = request.POST.get('is_done_note') == 'on'
            obj.body = body 
            obj.is_done = isdone
            obj.save()

            if not body :
                return HttpResponse("Please fill required fields*")

            return redirect('SHOW_MEMO')
        
        elif category == 'shop_order' : 
            product = request.POST.get('product_name')
            #quantity = request.POST.get('quantity')
            try:
                quantity = int(request.POST.get('quantity', 1) or 1)
            except ValueError:
                quantity = 1
            
            order_date_str = request.POST.get('shop_order_date', '').strip()
            if order_date_str:
                try:
                    date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
            else:
                date = None

            notes = request.POST.get('shop_order_notes')
            isdone = request.POST.get('is_done_shop_order') == 'on'

            if not product : 
                return HttpResponse ("Please fill required fields*")

            obj.prod_order_name = product
            obj.prod_order_qty = quantity
            obj.order_date = date
            obj.body = notes
            obj.is_done = isdone
            obj.save()

            return redirect('SHOW_MEMO')
        
        elif category == 'customer' : 
            name = request.POST.get('customer_name')
            phone = request.POST.get('customer_phone')
            notes = request.POST.get('customer_notes')

            if not name or not phone : 
                return HttpResponse ("Please fill the required fields*")

            try : 
                obj.customer_name = name
                obj.customer_phone = phone
                obj.body = notes
                obj.save()
            except IntegrityError : 
                return HttpResponse("Phone number already exist")
            
            return redirect('SHOW_MEMO')
        
        else : 
            #cus_id = request.POST.get('costumer_id')
            try:
                cus_id = int(request.POST.get('costumer_id', None) or None)
            except ValueError:
                cus_id = None
            if not isinstance(cus_id, int): 
                return HttpResponse("Plese fill the COSTUMER ID FIELD WITH NUMBERS ONLY***")
            
            costomer = get_object_or_404(UserCustomer, id=cus_id)       
            product = request.POST.get('product_name') 
            #quantity = request.POST.get('quantity') 
            try:
                quantity = int(request.POST.get('quantity', 1) or 1)
            except ValueError:
                quantity = 1

            order_date_str = request.POST.get('customer_order_date', '').strip()
            if order_date_str:
                try:
                    date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
            else:
                date = None

            ispaid = request.POST.get('is_paid_customer_order') == 'on'
            #amount_paid = request.POST.get('amount_customer')
            if not ispaid : 
                amount_paid = 0 
            else : 
                try : 
                    amount_paid = int(request.POST.get('amount_customer', 0) or 0)
                except ValueError:
                    amount_paid = 0
            if amount_paid == 0 and ispaid : 
                return HttpResponse("ERROR, Please enter the amount Paid in advance or uncheck Paid**")
            
            notes = request.POST.get('order_order_notes') 
            isdone = request.POST.get('is_done_customer_order') == 'on'

            if not product or not cus_id : 
                return HttpResponse ("Please fill the required fields*")

            obj.customer_exist = costomer
            obj.product_order = product
            obj.quantity_order = quantity
            obj.is_paid = ispaid
            obj.amount_paid = amount_paid
            obj.order_date = date
            obj.body = notes
            obj.is_done = isdone
            obj.save()

            return redirect('SHOW_MEMO')

    return render (request, 'accounts/edit_memo.html', context)

@login_required
def show_costumers (request) : 

    all_costumers = {'costumer' : UserCustomer.objects.all()}

    return render (request, "accounts/all_costumers.html", all_costumers)

@login_required
def customer_details (request, pk) : 

    costumer = get_object_or_404(UserCustomer, pk=pk)
    orders = [order for order in costumer.existant_costumer.all().order_by('is_done', '-date_create')]
    costumer.customer_name = costumer.customer_name.capitalize()
    for item in orders : 
        print (item.date_create)

    context = {'costumer' : costumer,
               'orders' : orders}

    return render (request, 'accounts/customer_details.html', context)


