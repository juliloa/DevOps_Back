
from django.urls import path
from .views import ProductListView, ProductCategoryFilterView, ProductWarehouseFilterView, ProductAttributeFilterView, ProductPriceFilterView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/category/<int:category_id>/', ProductCategoryFilterView.as_view(), name='product-category-filter'),
    path('products/warehouse/<int:warehouse_id>/', ProductWarehouseFilterView.as_view(), name='product-warehouse-filter'),
    path('products/filter/attributes/', ProductAttributeFilterView.as_view(), name='product-attribute-filter'),
    path('products/filter/price/', ProductPriceFilterView.as_view(), name='product-price-filter'),
]
