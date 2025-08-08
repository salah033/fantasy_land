from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
            return redirect(next_url)  # Redirect to a dashboard or home page
        else:
            messages.error(request, 'Invalid username or password.')
    
    next_url = next_url.split("/")
    next_url = next_url[-2].capitalize()

    return render(request, 'accounts/login.html', {'next': next_url})

def accounts_register(request) :
    return render (request , 'accounts/register.html')
# Create your views here.
