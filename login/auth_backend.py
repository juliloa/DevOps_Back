
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from dbmodels.models.users import Users
from django.utils import timezone  

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Users.objects.get(email=email)

            if check_password(password, user.password):
                user.last_login = timezone.now()
                user.save()

                # Simular los atributos que Django espera para login()
                user.is_authenticated = True
                user.is_active = True
                user.is_anonymous = False
                user.is_staff = getattr(user, 'is_staff', False)
                user.get_username = lambda: user.email  

                return user
        except Users.DoesNotExist:
            return None
        except Exception as e:
            print(f"[ERROR] Excepción en auth backend: {e}")
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
