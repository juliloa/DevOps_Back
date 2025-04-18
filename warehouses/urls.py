from django.urls import path
from warehouses.views.warehouses_views import WarehouseByProductView, WarehouseDetailView, WarehouseListView

urlpatterns = [
    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path('warehouses/<int:warehouse_id>/', WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('warehouses/by-product/<int:product_id>/', WarehouseByProductView.as_view(), name='warehouse-by-product'),
]