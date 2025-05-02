from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from urllib.parse import urlparse, urljoin
from django.conf import settings

def root_redirect(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                
                parsed_url = urlparse(next_url)
                if parsed_url.netloc == '' or parsed_url.netloc == request.get_host():
                   
                    return redirect(next_url)
                else:
                    return redirect('catalogo-view') 
            return redirect('catalogo-view') 
        else:
            messages.error(request, 'Credenciales inválidas.')
            return render(request, 'login.html')

    return render(request, 'login.html')
