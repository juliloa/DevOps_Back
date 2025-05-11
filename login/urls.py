
from django.urls import path
from .views import root_redirect
from . import views
from .views import password_reset_request_view, password_reset_submit_view
from .views import password_reset_confirm_view, password_reset_confirm_submit_view

urlpatterns = [
    path('', root_redirect),  
    path('login/', views.login_form_view, name='login'),  
    path('login/submit/', views.login_submit_view, name='login_submit'),  
    path('logout/', views.logout_view, name='logout'),

    path('users/', views.user_list_view, name='user-list'),
    path('users/create/', views.user_create_form_view, name='user-create-form'),
    path('users/create/submit/', views.user_create_submit_view, name='user-create-submit'),
    path('users/<str:user_id>/edit/', views.user_edit_form_view, name='user-edit-form'),
    path('users/<str:user_id>/edit/submit/', views.user_edit_submit_view, name='user-edit-submit'),
    path('users/<str:user_id>/delete/', views.user_delete_view, name='user-delete'),

    path('password_reset/', password_reset_request_view, name='password_reset'),
    path('password_reset/submit/', password_reset_submit_view, name='password_reset_submit'),

    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/submit/', password_reset_confirm_submit_view, name='password_reset_confirm_submit'),
]

