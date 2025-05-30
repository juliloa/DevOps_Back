from django.urls import path
from products.views.product_views import update_inventory_quantity,inventory_list_view,catalogo_view,product_list, product_create,product_create_post, product_delete, product_edit_get,product_edit
from products.views.filter_views.attribute_filter import product_filter_by_attributes_view
from products.views.filter_views.category_filter import product_category_filter_view
from products.views.filter_views.price_filter import product_price_filter_view
from products.views.filter_views.warehouse_filter import product_warehouse_filter_view
from products.views.product_detail_view import (
    ProductDetailView,
    variant_create,
    variant_create_post,
    variant_edit_get,
    variant_edit_post,
    variant_delete,
)

urlpatterns = [
    path('inventory/', inventory_list_view, name='inventory-list'),  
    path('inventory/update/', update_inventory_quantity, name='inventory-update'),  

    path('', catalogo_view, name='catalogo-view'),
    path('productos/', product_list, name='product-list'),  
    path('create/', product_create, name='product-create'), 
    path('create/post/', product_create_post, name='product-create-post'), 
    path('<int:pk>/edit/', product_edit_get, name='product-edit'),
    path('<int:pk>/edit/post/', product_edit, name='product-edit-post'),
    path('<int:pk>/delete/', product_delete, name='product-delete'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # Variantes 
    path('<int:product_id>/variants/create/', variant_create, name='variant-create'),
    path('<int:product_id>/variants/create/post/', variant_create_post, name='variant-create-post'),
    path('variants/<int:variant_id>/edit/', variant_edit_get, name='variant-edit'),
    path('variants/<int:variant_id>/edit/post/', variant_edit_post, name='variant-edit-post'),
    path('products/variants/<int:variant_id>/delete/', variant_delete, name='variant-delete'),

    # Filtros
    path('products/category/<int:category_id>/', product_category_filter_view, name='product-category-filter'),
    path('products/warehouse/<int:warehouse_id>/', product_warehouse_filter_view, name='product-warehouse-filter'),
    path('products/price/', product_price_filter_view, name='product-price-filter'),
    path('filtrar-por-atributos/', product_filter_by_attributes_view, name='product-filter-attributes'),
]
