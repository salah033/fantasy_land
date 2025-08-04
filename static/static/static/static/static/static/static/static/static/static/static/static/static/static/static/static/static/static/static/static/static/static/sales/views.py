from django.shortcuts import render
from django.http import JsonResponse
from products.models import Products
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Sale, SaleItem
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from django.contrib.auth.decorators import login_required

@login_required
def sale_page(request) : 

    return render (request, 'sales/sale.html') 


def get_product_by_barcode(request) : 

    barcode_ref = request.GET.get('barcode')
    if not barcode_ref:
        return JsonResponse({'success': False, 'error': 'No barcode or referenceprovided'})
    
    try:
        product = Products.objects.get(Q(bare_code=barcode_ref) | Q(reference=barcode_ref))
        data = {
            'success': True,
            'id': product.id,
            'name': product.name,
            'price': product.price,  
        }
    except Products.DoesNotExist:
        data = {'success': False, 'error': 'Product not found'}

    return JsonResponse(data)

def confirm_sale(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            products = data.get('products', [])
            total = 0

            adjusted_time = timezone.now() + timedelta(hours=1)
            sale = Sale.objects.create(date=adjusted_time, total_amount=0)
            #sale = Sale.objects.create(total_amount=0)  

            for item in products:
                product = Products.objects.get(pk=item['id'])
                qty = item['qty']

                if product.quantity < qty:
                    sale.delete()
                    return JsonResponse({'success': False, 'error': f"Not enough stock for {product.name}"})
                    
                #sale = Sale.objects.create(date=adjusted_time, total_amount=0)
                product.quantity -= qty
                product.save()

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=qty,
                    unit_price=product.price
                )
                
                total += product.price * qty

            sale.total_amount = total
            sale.save()
            
            return JsonResponse({'success': True, 'sale_id': sale.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def sale_receipt(request, sale_id):
    sale = Sale.objects.get(pk=sale_id)
    items = SaleItem.objects.filter(sale=sale).select_related('product')

    ################_###
    '''for item in items:
        product = item.product
        if len(product.name) > 20:
            new_name = product.name[:20] + ".."
            print("NAME:", new_name)
            product.name = new_name
            product.save()'''

    return render(request, 'sales/receipt.html', {
        'sale': sale,
        'items': items,
    })

@login_required
def all_receipts (request) : 

    sales = Sale.objects.all()

    receipt_id = request.GET.get('id_input')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if receipt_id : 
        sales = sales.filter(id=receipt_id)
    if start_date : 
        sales = sales.filter(date__date__gte=start_date)
    if end_date : 
        sales = sales.filter(date__date__lte=end_date)
    
    context = {'sales' : sales,}
    return render (request, 'sales/all_receipts.html', context)

@login_required
def close_drawer(request) : 

    non_closed = Sale.objects.filter(is_closed=False)

    today = timezone.now().date()

    total = non_closed.aggregate(
    total_non_closed=Sum('total_amount'))['total_non_closed']
    


    #######
    summary = (
    SaleItem.objects
    .filter(sale__is_closed=False)
    .values('product__name')
    .annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('unit_price'),
                output_field=FloatField()
            )
        )
    )
)

    '''summary = (
    non_closed
    .values('product__name')
    .annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('unit_price'),
                output_field=FloatField()
            )
        )
    )
)            '''                                        

    context = {'summary' : summary,
               'total' : total,
               'date' : today, }
    print (context)
    


    #TO_PASS_IT_TO_CONFIRMED_CLOSE#
    request.session['drawer_summary'] = list(summary)
    request.session['drawer_total'] = float(total) if total else 0.0

    return render (request, 'sales/close_drawer.html', context)

@login_required
def close_confirmed (request) : 

    today = timezone.now().date()

    summary = request.session.get('drawer_summary', [])
    total = request.session.get('drawer_total', 0)
    

    context = {
        'summary': summary,
        'total': total,
        'date' : today, }
    
    summary = request.session.pop('summary', [])
    total = request.session.pop('total', 0)

    Sale.objects.filter(is_closed=False).update(is_closed=True)

    return render (request , 'sales/close_confirmed.html', context)



    
