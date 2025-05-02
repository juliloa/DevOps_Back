

from django.urls import path
from .views import login_view, root_redirect

urlpatterns = [
    path('', root_redirect),  
]

