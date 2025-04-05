from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from dbmodels.models.users import Users

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, role_name=None):
        try:
            print(f"[DEBUG] Email: {email}, Password: {password}, Role ID: {role_name}")
            
            user = Users.objects.get(email=email)
            print(f"[DEBUG] Usuario encontrado: {user.name}")

            if check_password(password, user.password):
                print("[DEBUG] Contraseña válida")

                # Validar el rol por ID (no por nombre)
                if role_name and str(user.role.id) != str(role_name):
                    print(f"[DEBUG] Rol inválido. Esperado {user.role.id}, recibido {role_name}")
                    return None

                print("[DEBUG] Autenticación exitosa")
                return user
            else:
                print("[DEBUG] Contraseña inválida")

        except Users.DoesNotExist:
            print("[DEBUG] Usuario no encontrado")
        except Exception as e:
            print(f"[ERROR] Excepción en auth backend: {e}")
        
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
