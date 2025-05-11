from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.contrib import messages
from dbmodels.models import Users, Roles, Warehouses
from   LOGIVAG import settings
import logging

@require_GET
def user_list_view(request):
    users = Users.objects.select_related('role', 'warehouse').all()
    return render(request, 'users/list.html', {'users': users})

@require_GET
def user_create_form_view(request):
    roles = Roles.objects.all()
    warehouses = Warehouses.objects.all()
    return render(request, 'users/create.html', {'roles': roles, 'warehouses': warehouses})

@require_POST
def user_create_submit_view(request):
    data = request.POST
    user = Users(
        email=data['email'],
        name=data['name'],
        id_card=data['id_card'],
        phone=data.get('phone'),
        warehouse_id=data.get('warehouse') or None,
        role_id=data['role'],
        status=True
    )
    user.set_password(data['password'])  
    user.save()
    return redirect('user-list')

@require_GET
def user_edit_form_view(request, user_id):
    user = get_object_or_404(Users, id_card=user_id)
    roles = Roles.objects.all()
    warehouses = Warehouses.objects.all()
    return render(request, 'users/edit.html', {'user': user, 'roles': roles, 'warehouses': warehouses})

@require_POST
def user_edit_submit_view(request, user_id):
    user = get_object_or_404(Users, id_card=user_id)
    data = request.POST
    user.name = data['name']
    user.email = data['email']
    user.phone = data.get('phone')
    user.warehouse_id = data.get('warehouse') or None
    user.role_id = data['role']
    user.status = data.get('status') == 'on'
    
    if data.get('password'):
        user.set_password(data['password'])

    user.save()
    return redirect('user-list')

@require_POST
def user_delete_view(request, user_id):
    Users.objects.filter(id_card=user_id).delete()
    return redirect('user-list')

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

        
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax')

        logger.info(f"Token de acceso configurado: {refresh.access_token}")

        return response 
    else:
        messages.error(request, 'Credenciales inválidas.')
        return render(request, 'login.html')

@require_POST
def logout_view(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    request.session.flush() 
    return response

@require_GET
def password_reset_request_view(request):
    return render(request, 'password_reset_form.html', {'form': PasswordResetForm()})

@require_POST
def password_reset_submit_view(request):
    form = PasswordResetForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = Users.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            protocol = 'https' if not settings.DEBUG else 'http'
            link = f'{protocol}://{domain}/reset/{uid}/{token}/'

            subject = "Restablecimiento de Contraseña"
            message = render_to_string('password_reset_email.html', {'link': link, 'user': user})
            send_mail(subject, message, 'noreply@miempresa.com', [user.email])
            messages.success(request, 'Te hemos enviado un correo para restablecer tu contraseña.')
            return redirect('login') 
        return HttpResponse('Te hemos enviado un correo para restablecer tu contraseña.')
    
    return render(request, 'password_reset_form.html', {'form': form})

@require_GET
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except (Users.DoesNotExist, ValueError, TypeError):
        return HttpResponse('El enlace de restablecimiento es inválido.')

    if default_token_generator.check_token(user, token):
        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {
            'form': form,
            'uidb64': uidb64,  
            'token': token     
        })

    return HttpResponse('El enlace ha expirado o no es válido.')

@require_POST
def password_reset_confirm_submit_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except (Users.DoesNotExist, ValueError, TypeError):
        return HttpResponse('El enlace de restablecimiento es inválido.')

    if default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST)
        
        if form.is_valid():
            form.save()  # Guarda la nueva contraseña

            # No es necesario autenticar al usuario en este momento
            messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
            
            # Redirige al login para que el usuario se autentique con la nueva contraseña
            return redirect('login')  # Redirigir al login

        else:
            # Aquí puedes agregar un log o depuración para revisar qué no está validando correctamente.
            logger.error(f"Formulario de cambio de contraseña no válido: {form.errors}")
            return render(request, 'password_reset_confirm.html', {
                'form': form,
                'uidb64': uidb64,
                'token': token
            })

    return HttpResponse('El enlace de restablecimiento ha expirado o es inválido.')
