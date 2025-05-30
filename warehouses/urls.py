from django.urls import path
from .views.views_warehouses import warehouse_create,warehouse_delete,warehouse_edit,warehouse_list
from .views.warehouses_views import WarehouseByProductView, WarehouseDetailView, WarehouseCoordinatesOnlyView
from .views.map_view import warehouse_map_view

urlpatterns = [

    path('bodegas/', warehouse_list, name='warehouse-list'),
    path('bodegas/crear/', warehouse_create, name='warehouse-create'),
    path('bodegas/editar/<int:id>/', warehouse_edit, name='warehouse-edit'),
    path('bodegas/eliminar/<int:id>/', warehouse_delete, name='warehouse-delete'),

    path('warehouses/<int:warehouse_id>/', WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('warehouses/by-product/<int:product_id>/', WarehouseByProductView.as_view(), name='warehouse-by-product'),
    path('mapa-bodegas/', warehouse_map_view, name='warehouse-map'),
    path('warehouses/coordinates/', WarehouseCoordinatesOnlyView.as_view(), name='warehouse-coordinates'),
]