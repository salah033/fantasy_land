from django.shortcuts import render, redirect
from products.models import Products
from sales.models import SaleItem
from django.db.models import Sum
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .utils import fetch_games
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def home_redirect (request) :
    return redirect ('HOME')

@login_required
def home_page (request) : 
    low_products_stock = Products.objects.filter(quantity__lte=5).order_by('quantity')

    best_seller = (SaleItem.objects.values('product_id', 'product__name', 'product__category__name')
                  .annotate(total_quantity_sold=Sum('quantity'))
                  .order_by('-total_quantity_sold')
                  )
       
    #####GRAPHS##########

    low_labels = [p.name[:15] for p in low_products_stock]
    low_values = [p.quantity for p in low_products_stock]

    #print (low_labels, low_values)

    best_labels = [item['product__name'][:15] for item in best_seller]
    best_values = [item['total_quantity_sold'] for item in best_seller]

    #print (best_labels, best_values)

    ####TRENDING_GAMES####
    
    today = date.today()
    two_months_later = today + relativedelta(months=3)
    start = '2018-01-01'

    API_KEY = '0322c45dbaa84f9a9322d64b327b4323'

    released_url = (f"https://api.rawg.io/api/games?key={API_KEY}&dates={start},{today}&platforms=7,18,187&ordering=-added&page_size=40")
    upcoming_url = (f"https://api.rawg.io/api/games?key={API_KEY}&dates={today},{two_months_later}&platforms=7,18,187&ordering=-added&page_size=40")

    released_g = fetch_games(released_url)
    upcoming_g = fetch_games(upcoming_url)

    upcoming_g = sorted(
        [g for g in upcoming_g   if g.get('released')],
        key=lambda x: datetime.strptime(x['released'], "%Y-%m-%d")
    )

    released = []
    upcoming = []

    for game in released_g: 
        game_name = game.get('name')
        game_date = game.get('released')
        platforms = [p['platform']['name'] for p in game.get('platforms', []) if p['platform']['id'] in [7, 18, 187]]
        
        released.append({
            'name': game_name,
            'platforms': platforms,
            'released' : game_date
        })
    
    for game in upcoming_g: 
        game_name = game.get('name')
        game_date = game.get('released')
        platforms = [p['platform']['name'] for p in game.get('platforms', []) if p['platform']['id'] in [7, 18, 187]]
        
        upcoming.append({
            'name': game_name,
            'platforms': platforms,
            'released' : game_date
        })
    
    #print(f"{game['name']} → {game['released']}")
    #print (released)
    #print ("####")
    #print (upcoming) 

    context = {'low_products' : low_products_stock,
               'best_seller' : best_seller,
               'released' : released, 
               'upcoming': upcoming,
               'low_labels': json.dumps(low_labels),
               'low_values': json.dumps(low_values),
               'best_labels': json.dumps(best_labels),
               'best_values': json.dumps(best_values),
               } 

    return render(request, 'home/home.html', context)

######___######

def filter_low_stock(request):
    cat_id = request.GET.get('category')
    if cat_id:
        products = Products.objects.filter(quantity__lte=5, category_id=cat_id).order_by('quantity')
    else:
        products = Products.objects.filter(quantity__lte=5).order_by('quantity')

    # Chart data
    labels = [p.name[:15] for p in products]
    values = [p.quantity for p in products]

    html = render_to_string('home/partials/_low_stock_list.html', {'low_products': products})

    return JsonResponse({
        'html': html,
        'labels': labels,
        'values': values,
    })



def filter_best_seller(request):
    cat_id = request.GET.get('category')

    best_seller = (SaleItem.objects
                   .values('product_id', 'product__name', 'product__category__name')
                   .annotate(total_quantity_sold=Sum('quantity'))
                   .order_by('-total_quantity_sold'))
    
    if cat_id:
        best_seller = best_seller.filter(product__category_id=cat_id)

    print (f"BEST_SELLER : {best_seller}")

    labels = [item['product__name'][:15] for item in best_seller]
    values = [item['total_quantity_sold'] for item in best_seller]

    html = render_to_string('home/partials/_best_seller_list.html', {'best_seller': best_seller})
    print (html)
    return JsonResponse({
        'html': html,
        'labels': labels,
        'values': values,
    })



@login_required
def about_page (request) : 
    
    return render(request, 'home/about.html')
     