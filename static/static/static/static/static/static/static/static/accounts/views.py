from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
    print (request)
    if request.method == "POST":
        

        logout(request)
        return JsonResponse({'redirect_url': reverse('ACCOUNTS_LOGIN')})
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def user_dashboard (request) : 
    return render (request, 'accounts/dashboard.html')
# Create your views here.
