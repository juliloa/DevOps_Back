from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from urllib.parse import urlparse
from django.views.decorators.http import require_GET, require_POST

@require_GET
def root_redirect(_request):
    return redirect('login')  

@require_GET
def login_form_view(request):
    return render(request, 'login.html') 

@require_POST
def login_submit_view(request):
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
        return redirect('catalogo-view')
    else:
        messages.error(request, 'Credenciales inválidas.')
        return render(request, 'login.html')
