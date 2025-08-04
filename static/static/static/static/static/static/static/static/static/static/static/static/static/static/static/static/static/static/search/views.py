from django.shortcuts import render, get_object_or_404
from products.models import Products, Categories
from supplier.models import Suppliers
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def search_item (request) : 
    query = request.GET.get('q')
    search_type = request.GET.get('type')

    results = []
    context = {
        'query': query,
        'search_type': search_type,
        'results': results,
    }

    if query:
        if search_type == 'products':
            results = Products.objects.filter(Q(name__icontains=query) | Q(bare_code__icontains=query) 
                                                        |Q (reference__icontains=query), active=True)
        elif search_type == 'suppliers':
            results = Suppliers.objects.filter(name__icontains=query, active=True)
        
        context['results'] = results

    return render(request, "search/search_item.html", context)

@login_required
def category_detail(request):
    category_type = request.GET.get('category')

    results = []
    category = get_object_or_404(Categories, id=category_type)

    if category_type:
        results = Products.objects.filter(category__id=category_type, active=True)

    context = {
        'category': category,  
        'results': results
    }

    return render(request, 'search/category_detail.html', context)