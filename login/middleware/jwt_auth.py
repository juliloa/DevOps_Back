from django.contrib.auth import logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin
import logging
from django.urls import reverse
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

class JWTMiddleware(MiddlewareMixin):
    def __call__(self, request):

        if request.path == reverse('login') or request.path.startswith('/login/'):
            return super().__call__(request)

        
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                validated_token = JWTAuthentication().get_validated_token(access_token)
                user = JWTAuthentication().get_user(validated_token)

                logger.info(f"Usuario válido del token: {user.email}")
                request.user = user  

                if not user.is_active:
                    raise AuthenticationFailed("El usuario no está activo.")
            except AuthenticationFailed as e:
                logger.error(f"Error de autenticación en el middleware: {str(e)}")

                if refresh_token:
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
                else:
                    logger.warning("No se encontró refresh token en las cookies.")
                    return self.clear_session(request)  
        else:
            logger.warning("No se encontró access token en las cookies.")
            return self.clear_session(request)  
        
        return super().__call__(request)  

    def clear_session(self, request):
        """Función para limpiar la sesión y las cookies del usuario"""
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')


        if request.user.is_authenticated:
            logout(request)

        request.session.flush()  

        return response
