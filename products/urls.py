from django.urls import path
from products.views.product_views import catalogo_view
from products.views.filter_views.attribute_filter import ProductAttributeFilterView
from products.views.product_detail_view import ProductDetailView
from products.views.filter_views.attribute_filter import ProductListView
from products.views.filter_views.category_filter import ProductCategoryFilterView
from products.views.filter_views.price_filter import ProductPriceFilterView
from products.views.filter_views.warehouse_filter import ProductWarehouseFilterView

urlpatterns = [
    path('', catalogo_view, name='catalogo-view'),
    
    path('products/', ProductListView.as_view(), name='product-list'),

    path('products/category/<int:category_id>/',ProductCategoryFilterView.as_view(), name='product-category-filter'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # GET /products/warehouse/2/   → filtrar por bodega
    path('warehouse/<int:warehouse_id>/', ProductWarehouseFilterView.as_view(), name='product-warehouse-filter'),

    # GET /products/filter/attributes/?color=...&size=... 
    path('filter/attributes/', ProductAttributeFilterView.as_view(), name='product-attribute-filter'),

    # GET /products/filter/price/?min_price=10&max_price=100
    path('filter/price/', ProductPriceFilterView.as_view(), name='product-price-filter'),
]
