from django.contrib import admin
from django.urls import path, include
from login.views import login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('accounts/login/', login_view, name='login'),
    path('', include('login.urls')), 

    # productos
    path('products/', include('products.urls')),

    # bodegas
    path('warehouses/', include('warehouses.urls')),

    # movimientos
    path('movements/', include('movements.urls')),

]
