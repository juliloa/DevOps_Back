from django.http import HttpResponseRedirect
import logging
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication  
from .RestrictAccessMiddleware import  is_excluded_path  

logger = logging.getLogger(__name__)

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_excluded_path(request.path):
            return self.get_response(request)

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            return self._handle_access_token(request, access_token)

        if refresh_token:
            return self._handle_refresh_token(request, refresh_token)

        logger.warning("No se encontró access token ni refresh token en las cookies.")
        return self.clear_session(request)

    def _handle_access_token(self, request, access_token):
        try:
            validated_token = JWTAuthentication().get_validated_token(access_token)
            user = JWTAuthentication().get_user(validated_token)
            logger.info(f"Usuario válido del token: {user.email}")
            request.user = user

            if not user.is_active:
                raise AuthenticationFailed("El usuario no está activo.")
            return self.get_response(request)
        except AuthenticationFailed as e:
            logger.error(f"Error de autenticación en el middleware: {str(e)}")
            return self.clear_session(request)

    def _handle_refresh_token(self, request, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)

            if refresh.is_expired():
                logger.error("El refresh token ha expirado.")
                raise AuthenticationFailed("El refresh token ha expirado. Inicie sesión nuevamente.")

            new_access_token = str(refresh.access_token)
            logger.info("Nuevo access token generado")
            response = HttpResponseRedirect(request.path)
            response.set_cookie('access_token', new_access_token, httponly=True, secure=True, samesite='Lax')

            validated_token = JWTAuthentication().get_validated_token(new_access_token)
            user = JWTAuthentication().get_user(validated_token)
            logger.info(f"Nuevo token de acceso generado para el usuario: {user.email}")
            request.user = user

            if not user.is_active:
                raise AuthenticationFailed("El usuario no está activo.")
            return response
        except Exception as e:
            logger.error(f"Error al renovar el token de acceso: {str(e)}")
            return self.clear_session(request)

    def clear_session(self, _request):
        logger.info("Limpiando sesión debido a error de autenticación.")
        return HttpResponseRedirect(reverse('login'))
