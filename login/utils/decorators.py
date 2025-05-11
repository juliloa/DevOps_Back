
from functools import wraps
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

def jwt_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token_str = request.COOKIES.get('access_token')
        refresh_token_str = request.COOKIES.get('refresh_token')

        if not access_token_str:
            return redirect('login')

        try:
            access_token = AccessToken(access_token_str)
            user_id = access_token['id_card']  
            user = User.objects.get(id_card=user_id) 
            request.user = user
            return view_func(request, *args, **kwargs)
        except TokenError:
            if not refresh_token_str:
                return redirect('login')
            try:
                refresh_token = RefreshToken(refresh_token_str)
                user_id = refresh_token['id_card']
                user = User.objects.get(id_card=user_id) 
                new_access_token = str(refresh_token.access_token)
                request.user = user
                response = view_func(request, *args, **kwargs)
                response.set_cookie('access_token', new_access_token, httponly=True, samesite='Lax')
                return response
            except (TokenError, User.DoesNotExist):
                return redirect('login')
        except User.DoesNotExist:
            return redirect('login')

    return _wrapped_view

