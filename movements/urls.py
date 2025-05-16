from django.urls import path
from . import views

urlpatterns = [
    # Listado de movimientos
    path('', views.movement_list_view, name='movement-list'),
    path('create/', views.movement_create_get_view, name='movement-create'),
    path('create/submit/', views.movement_create_post_view, name='movement-create-submit'),
    path('confirm/<int:pk>/submit/', views.confirm_movement, name='movement-confirm-submit'),
    path('cancel/<int:pk>/submit/', views.cancel_movement, name='movement-cancel-submit'),
    path('api/available-warehouses/', views.available_warehouses_api, name='available-warehouses-api'),
]
