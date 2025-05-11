from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLS = [
    '/login/',
    '/login/submit/',
    '/logout/',
    '/admin/',
]

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if any(path.startswith(url) for url in EXEMPT_URLS):
            return self.get_response(request)

        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return redirect(reverse('login'))

        return self.get_response(request)