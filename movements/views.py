from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
from django.urls import reverse
from dbmodels.models import Movements, Inventory
from .MovementForm import MovementForm

# Constantes de rutas
MOVEMENT_FORM_TEMPLATE = 'movements/movement_form.html'
MOVEMENT_LIST_TEMPLATE = 'movements/movement_list.html'
ADMIN_EMAIL = 'juliana.loaiza14@gmail.com'

# ------------------- Función general para enviar correos -------------------
def enviar_correo(destinatario, asunto, plantilla, contexto):
    cuerpo = render_to_string(plantilla, contexto)
    send_mail(
        subject=asunto,
        message='',
        html_message=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinatario],
        fail_silently=False
    )

# ------------------- API de bodegas con stock -------------------
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

# ------------------- Vista de listado de movimientos -------------------
@require_GET
def movement_list_view(request):
    movements = Movements.objects.all()
    return render(request, MOVEMENT_LIST_TEMPLATE, {'movements': movements})

# ------------------- Crear movimiento: GET -------------------
@require_GET
def movement_create_get_view(request):
    form = MovementForm()
    return render(request, MOVEMENT_FORM_TEMPLATE, {'form': form})

# ------------------- Crear movimiento: POST -------------------
@require_POST
@transaction.atomic
def movement_create_post_view(request):
    form = MovementForm(request.POST)
    if form.is_valid():
        movement = form.save(commit=False)
        movement.user = request.user

        inv = Inventory.objects.select_for_update().filter(
            variant=movement.variant,
            warehouse=movement.source_warehouse
        ).first()

        if not inv or inv.quantity < movement.quantity:
            return render(request, MOVEMENT_FORM_TEMPLATE, {'form': form})

        movement.status = 'Pending'
        movement.save()

        # Correos
        enviar_correo(
            request.user.email,
            "Movimiento creado",
            "emails/movimiento_creado.html",
            {"movement": movement, "user": request.user}
        )

        enviar_correo(
            ADMIN_EMAIL,
            "Nuevo movimiento pendiente",
            "emails/movimiento_pendiente_admin.html",
            {
                "movement": movement,
                "confirm_url": request.build_absolute_uri(reverse("movement-confirm-submit", args=[movement.pk])),
                "cancel_url": request.build_absolute_uri(reverse("movement-cancel-submit", args=[movement.pk]))
            }
        )
        return redirect('movement-list')
    else:
        return render(request, MOVEMENT_FORM_TEMPLATE, {'form': form})

# ------------------- Confirmar movimiento -------------------
@require_POST
@transaction.atomic
def confirm_movement(request, pk):
    movement = get_object_or_404(Movements.objects.select_for_update(), pk=pk)

    if movement.status != 'Pending':
        return redirect('movement-list')

    inv_source = Inventory.objects.select_for_update().filter(
        variant=movement.variant,
        warehouse=movement.source_warehouse
    ).first()

    if not inv_source or inv_source.quantity < movement.quantity:
        return redirect('movement-list')

    # Actualizar stock
    inv_source.quantity -= movement.quantity
    inv_source.save()

    inv_dest, _ = Inventory.objects.get_or_create(
        variant=movement.variant,
        warehouse=movement.destination_warehouse,
        defaults={'quantity': 0}
    )
    inv_dest.quantity += movement.quantity
    inv_dest.save()

    movement.status = 'Completed'
    movement.save()

    # Correos
    enviar_correo(
        movement.user.email,
        "Movimiento confirmado",
        "emails/movimiento_confirmado.html",
        {"movement": movement}
    )

    if hasattr(movement.destination_warehouse, 'email') and movement.destination_warehouse.email:
        enviar_correo(
            movement.destination_warehouse.email,
            "Actualización de inventario - Movimiento recibido",
            "emails/notificacion_bodega.html",
            {"movement": movement}
        )
    return redirect('movement-list')

# ------------------- Cancelar movimiento -------------------
@require_POST
@transaction.atomic
def cancel_movement(request, pk):
    movement = get_object_or_404(Movements.objects.select_for_update(), pk=pk)

    if movement.status != 'Pending':
        return redirect('movement-list')

    movement.status = 'Canceled'
    movement.save()

    enviar_correo(
        movement.user.email,
        "Movimiento cancelado",
        "emails/movimiento_cancelado.html",
        {"movement": movement}
    )

    return redirect('movement-list')
