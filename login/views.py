# login view
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def root_redirect(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Aquí Django usará el backend de autenticación que configuraste
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            
            # Verifica si hay un parámetro "next" en la URL y redirige en consecuencia
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('catalogo-view')  # Redirige al catálogo si no hay "next"
        else:
            messages.error(request, 'Credenciales inválidas.')
            return render(request, 'login.html')

    return render(request, 'login.html')
