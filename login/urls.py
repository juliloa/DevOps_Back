
from django.urls import path
from .views import root_redirect
from . import views
urlpatterns = [
    path('', root_redirect),  
    path('login/', views.login_form_view, name='login'),  
    path('login/submit/', views.login_submit_view, name='login_submit'),  
    path('logout/', views.logout_view, name='logout'),

]

