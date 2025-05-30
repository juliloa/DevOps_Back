from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from dbmodels.models import Warehouses  
from django.views.decorators.http import require_GET, require_POST


@require_GET
def warehouse_list(request):
    warehouses = Warehouses.objects.all()
    return render(request, 'warehouse_list.html', {'warehouses': warehouses})

@require_POST
def warehouse_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        location = request.POST.get('location')
        max_capacity = request.POST.get('max_capacity')
        open_hours = request.POST.get('open_hours')

        Warehouses.objects.create(
            name=name,
            phone=phone,
            email=email,
            location=location,
            max_capacity=max_capacity,
            open_hours=open_hours,
        )
    return redirect(reverse('warehouse-list'))

@require_POST
def warehouse_edit(request, id):
    warehouse = get_object_or_404(Warehouses, pk=id)
    if request.method == 'POST':
        warehouse.name = request.POST.get('name')
        warehouse.phone = request.POST.get('phone')
        warehouse.email = request.POST.get('email')
        warehouse.location = request.POST.get('location')
        warehouse.max_capacity = request.POST.get('max_capacity')
        warehouse.open_hours = request.POST.get('open_hours')
        warehouse.save()
    return redirect(reverse('warehouse-list'))

@require_POST
def warehouse_delete(request, id):
    warehouse = get_object_or_404(Warehouses, pk=id)
    if request.method == 'POST':
        warehouse.delete()
    return redirect(reverse('warehouse-list'))
