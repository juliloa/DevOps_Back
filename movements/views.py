from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_GET, require_POST

from dbmodels.models import Movements, Inventory
from .MovementForm import MovementForm


@require_GET
def available_warehouses_api(request):
    variant_id = request.GET.get("variant_id")
    inventories = Inventory.objects.filter(variant_id=variant_id, quantity__gt=0)
    data = [{
        "id": inv.warehouse.id,
        "name": inv.warehouse.name,
        "quantity": inv.quantity
    } for inv in inventories]
    return JsonResponse(data, safe=False)


@require_GET
def movement_list_view(request):
    movements = Movements.objects.all()
    return render(request, 'movements/movement_list.html', {'movements': movements})


@require_GET
def movement_create_get_view(request):
    form = MovementForm()
    return render(request, 'movements/movement_form.html', {'form': form})


from django.core.exceptions import ValidationError

@require_POST
@transaction.atomic
def movement_create_post_view(request):
    form = MovementForm(request.POST)
    if form.is_valid():
        movement = form.save(commit=False)
        movement.user = request.user

        # Validar stock disponible antes de guardar
        inv = Inventory.objects.select_for_update().filter(
            variant=movement.variant,
            warehouse=movement.source_warehouse
        ).first()

        if not inv or inv.quantity < movement.quantity:
            messages.error(request, "Stock insuficiente en la bodega de origen.")
            return render(request, 'movements/movement_form.html', {'form': form})

        movement.save()
        messages.success(request, "Movimiento creado correctamente.")
        return redirect('movement-list')
    else:
        messages.error(request, "Hubo un error al crear el movimiento.")
        return render(request, 'movements/movement_form.html', {'form': form})


@require_POST
@transaction.atomic
def confirm_movement(request, pk):
    movement = get_object_or_404(Movements.objects.select_for_update(), pk=pk)

    if movement.status != 'Pending':
        messages.error(request, "Este movimiento ya está confirmado o cancelado.")
        return redirect('movement-list')

    inv_source = Inventory.objects.select_for_update().filter(
        variant=movement.variant,
        warehouse=movement.source_warehouse
    ).first()

    if not inv_source:
        messages.error(request, "No existe inventario registrado para esta variante en la bodega origen.")
        return redirect('movement-list')

    if inv_source.quantity < movement.quantity:
        messages.error(request, "Stock insuficiente para confirmar el movimiento.")
        return redirect('movement-list')

    # Actualiza stock
    inv_source.quantity -= movement.quantity
    inv_source.save()

    inv_dest, _ = Inventory.objects.get_or_create(
        variant=movement.variant,
        warehouse=movement.destination_warehouse,
        defaults={'quantity': 0}
    )
    inv_dest.quantity += movement.quantity
    inv_dest.save()

    # Cambia estado del movimiento
    movement.status = 'Completed'
    movement.save()

    messages.success(request, "Movimiento confirmado correctamente.")
    return redirect('movement-list')

@require_POST
@transaction.atomic
def cancel_movement(request, pk):
    movement = get_object_or_404(Movements.objects.select_for_update(), pk=pk)

    if movement.status != 'Pending':
        messages.error(request, "Este movimiento ya está confirmado o cancelado.")
        return redirect('movement-list')

    movement.status = 'Canceled'
    movement.save()

    messages.success(request, "Movimiento cancelado correctamente.")
    return redirect('movement-list')
