import re
from django.http import HttpResponseForbidden

RESTRICTED_PATTERNS = [
    # Usuarios
    (r'^/users/', ['Administrador']),
    (r'^/users/create/', ['Administrador']),
    (r'^/password_reset/', ['Administrador']),
    (r'^/reset/', ['Administrador']),

    # Movimientos
    (r'^/movements/$', ['Administrador', 'Operativo']),
    (r'^/movements/movements/create/', ['Administrador', 'Operativo']),
    (r'^/movements/confirm/\d+/', ['Administrador']),
    (r'^/movements/cancel/\d+/', ['Administrador']),
    (r'^/api/available-warehouses/', ['Administrador', 'Operativo']),

    # Productos
    (r'^/products/create/$', ['Administrador']),
    (r'^/products/create/post/$', ['Administrador']),
    (r'^/products/\d+/edit/$', ['Administrador']),
    (r'^/products/\d+/edit/post/$', ['Administrador']),
    (r'^/products/\d+/delete/$', ['Administrador']),

    # Variantes
    (r'^/products/\d+/variants/create/$', ['Administrador']),
    (r'^/products/\d+/variants/create/post/$', ['Administrador']),
    (r'^/products/variants/\d+/edit/$', ['Administrador']),
    (r'^/variants/\d+/edit/post/$', ['Administrador']),
    (r'^/products/variants/\d+/delete/$', ['Administrador']),
]

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if not user.is_authenticated:
            return self.get_response(request)

        user_role = user.role.name

        for pattern, allowed_roles in RESTRICTED_PATTERNS:
            if re.match(pattern, path):
                if user_role not in allowed_roles:
                    return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        return self.get_response(request)
