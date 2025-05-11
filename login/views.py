from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.contrib import messages
from urllib.parse import urlparse
import logging
from django.views.decorators.http import require_GET, require_POST

@require_GET
def root_redirect(_request):
    return redirect('login')  

@require_GET
def login_form_view(request):
    return render(request, 'login.html') 


logger = logging.getLogger(__name__)

@require_POST
def login_submit_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        logger.info(f"Usuario autenticado: {user.email}")

        
        refresh = RefreshToken.for_user(user)
        response = HttpResponseRedirect('/products/')

        
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=False, samesite='Lax')
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax')

        logger.info(f"Token de acceso configurado: {refresh.access_token}")

        return response 
    else:
        messages.error(request, 'Credenciales inválidas.')
        return render(request, 'login.html')



def logout_view(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    request.session.flush() 
    return response

