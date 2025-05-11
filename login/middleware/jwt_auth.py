from django.http import HttpResponseRedirect
import logging
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication  # Importación correcta

logger = logging.getLogger(__name__)

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Guardar el get_response proporcionado por Django

    def __call__(self, request):
        if self._is_login_path(request):
            return self._handle_login_path(request)

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            return self._handle_access_token(request, access_token)

        if refresh_token:
            return self._handle_refresh_token(request, refresh_token)

        logger.warning("No se encontró access token ni refresh token en las cookies.")
        return self.clear_session(request)

    def _is_login_path(self, request):
        """ Verifica si la URL actual es de login. """
        return request.path == reverse('login') or request.path.startswith('/login/')

    def _handle_access_token(self, request, access_token):
        """ Maneja la autenticación del access token. """
        try:
            validated_token = JWTAuthentication().get_validated_token(access_token)
            user = JWTAuthentication().get_user(validated_token)
            logger.info(f"Usuario válido del token: {user.email}")
            request.user = user

            if not user.is_active:
                raise AuthenticationFailed("El usuario no está activo.")
            return self.get_response(request)  # Procede con la respuesta original
        except AuthenticationFailed as e:
            logger.error(f"Error de autenticación en el middleware: {str(e)}")
            return self.clear_session(request)

    def _handle_refresh_token(self, request, refresh_token):
        """ Maneja la renovación del access token usando el refresh token. """
        try:
            refresh = RefreshToken(refresh_token)

            if refresh.is_expired():
                logger.error("El refresh token ha expirado.")
                raise AuthenticationFailed("El refresh token ha expirado. Inicie sesión nuevamente.")

            new_access_token = str(refresh.access_token)
            logger.info("Nuevo access token generado")
            response = HttpResponseRedirect(request.path)
            response.set_cookie('access_token', new_access_token, httponly=True, secure=False, samesite='Lax')

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

    def clear_session(self, request):
        """ Limpia la sesión del usuario. """
        logger.info("Limpiando sesión debido a error de autenticación.")
        # Aquí agregarías el código necesario para limpiar la sesión
        return HttpResponseRedirect(reverse('login'))  # Redirige a la página de login

    def _handle_login_path(self, request):
        """ Si es la ruta de login, deja pasar la solicitud. """
        return self.get_response(request)
