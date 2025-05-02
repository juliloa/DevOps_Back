from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('', include('login.urls')), 

    # productos
    path('products/', include('products.urls')),

    # bodegas
    path('warehouses/', include('warehouses.urls')),

    # movimientos
    path('movements/', include('movements.urls')),

]
