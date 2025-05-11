from django.urls import path
from .views.warehouses_views import WarehouseByProductView, WarehouseDetailView, WarehouseListView, WarehouseCoordinatesOnlyView
from .views.map_view import warehouse_map_view

urlpatterns = [
    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path('warehouses/<int:warehouse_id>/', WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('warehouses/by-product/<int:product_id>/', WarehouseByProductView.as_view(), name='warehouse-by-product'),
    path('mapa-bodegas/', warehouse_map_view, name='warehouse-map'),
    path('warehouses/coordinates/', WarehouseCoordinatesOnlyView.as_view(), name='warehouse-coordinates'),
]