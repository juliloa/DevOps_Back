import re
from django.shortcuts import redirect
from django.urls import reverse

EXCLUDED_PATHS = [
    r'^/$', 
    r'^/landing/service/?$',
    r'^/landing/about/?$',
    r'^/login/?$',
    r'^/login/submit/?$',
    r'^/logout/?$',
    r'^/admin/.*$',
    r'^/password_reset/?$',
    r'^/password_reset/submit/?$',
    r'^/reset/.+/.+/?$',
]

def is_excluded_path(path):
    return any(re.match(pattern, path) for pattern in EXCLUDED_PATHS)

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_excluded_path(request.path):
            return self.get_response(request)

        access_token = request.COOKIES.get('access_token')
        if not access_token:
            print(f"[RestrictAccessMiddleware] No token, redirigiendo desde {request.path}")
            return redirect(reverse('login'))

        return self.get_response(request)
