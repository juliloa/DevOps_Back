from django.urls import path
from products.views.product_views import catalogo_view
from products.views.filter_views.attribute_filter import product_filter_by_attributes_view 
from products.views.product_detail_view import ProductDetailView
from products.views.filter_views.category_filter import product_category_filter_view
from products.views.filter_views.price_filter import product_price_filter_view
from products.views.filter_views.warehouse_filter import product_warehouse_filter_view
from products.views.product_views import product_create, product_delete, product_edit
from products.views.product_detail_view import variant_create,variant_delete,variant_edit
urlpatterns = [
    path('', catalogo_view, name='catalogo-view'),
    path('create/', product_create, name='product-create'),
    path('<int:pk>/edit/', product_edit, name='product-edit'),
    path('<int:pk>/delete/', product_delete, name='product-delete'),
    path('products/category/<int:category_id>/', product_category_filter_view, name='product-category-filter'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/variants/create/', variant_create, name='variant-create'),
    path('variants/<int:variant_id>/edit/', variant_edit, name='variant-edit'),
    path('variants/<int:variant_id>/delete/', variant_delete, name='variant-delete'),
    path('products/warehouse/<int:warehouse_id>/', product_warehouse_filter_view, name='product-warehouse-filter'),
    path('products/price/', product_price_filter_view, name='product-price-filter'),
    path('filtrar-por-atributos/', product_filter_by_attributes_view, name='product-filter-attributes'),

]
