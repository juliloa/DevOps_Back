
from django.urls import path
from products.views.product_views import ProductListView
from products.views.filter_views.attribute_filter import ProductAttributeFilterView
from products.views.filter_views.category_filter import ProductCategoryFilterView
from products.views.filter_views.price_filter import ProductPriceFilterView
from products.views.filter_views.warehouse_filter import ProductWarehouseFilterView
urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/category/<int:category_id>/', ProductCategoryFilterView.as_view(), name='product-category-filter'),
    path('products/warehouse/<int:warehouse_id>/', ProductWarehouseFilterView.as_view(), name='product-warehouse-filter'),
    path('products/filter/attributes/', ProductAttributeFilterView.as_view(), name='product-attribute-filter'),
    path('products/filter/price/', ProductPriceFilterView.as_view(), name='product-price-filter'),
]
