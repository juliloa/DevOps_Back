# movements/urls.py
from django.urls import path
from .views import available_warehouses_api
from . import views

urlpatterns = [
    path('', views.movement_list_view, name='movement-list'),  
    path('movements/create/', views.movement_create_get_view, name='movement-create'),
    path('movements/create/submit/', views.movement_create_post_view, name='movement-create-submit'),
    path('movements/confirm/<int:pk>/', views.confirm_movement, name='movement-confirm'),
    path('movements/cancel/<int:pk>/', views.cancel_movement, name='movement-cancel'),
    path('api/available-warehouses/', available_warehouses_api, name='available-warehouses-api'),
]
