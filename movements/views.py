# movements/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from dbmodels.models import Movements
from .serializers import MovementSerializer
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv 

load_dotenv()

class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movements.objects.all()
    serializer_class = MovementSerializer

    @action(detail=True, methods=['patch'], url_path='confirm')
    def confirm_movement(self, request, pk=None):
        try:
            movement = self.get_object()
            if movement.status != 'Pending':
                return Response({'detail': 'Solo se pueden confirmar movimientos en estado Pending.'}, status=400)
            movement.status = 'Completed'
            movement.save(update_fields=['status'])  
            self.send_notification(movement, 'confirmed')
            return Response({'detail': 'Movimiento confirmado correctamente.'})
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
    
    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel_movement(self, request, pk=None):
        try:
            movement = self.get_object()
            if movement.status == 'Canceled':
                return Response({'detail': 'El movimiento ya está cancelado.'}, status=400)
            if movement.status == 'Pending':
                movement.status = 'Canceled'
                movement.save(update_fields=['status'])
                self.send_notification(movement, 'canceled')
                return Response({'detail': 'Movimiento cancelado correctamente.'})
            return Response({'detail': 'Solo se pueden cancelar movimientos en estado Pending.'}, status=400)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

    def send_notification(self, movement, action):
        user_email = movement.user.email if movement.user and movement.user.email else None
        destination_email = movement.destination_warehouse.email if movement.destination_warehouse and movement.destination_warehouse.email else None
        source_email = movement.source_warehouse.email if movement.source_warehouse and movement.source_warehouse.email else None

        recipients = [email for email in [user_email, destination_email, source_email] if email]

    
        attributes = movement.variant.attributes
        color = attributes.get('color', 'No color')
        size = attributes.get('size', 'No size')

        if recipients:
            subject = f'Movimiento {action.capitalize()} - {movement.id}'
            message = f'El movimiento con ID {movement.id} ha sido {action}.\n' \
                    f'Producto: {movement.variant.product.name} (Color: {color}, Size: {size})\n' \
                    f'Cantidad: {movement.quantity}\n' \
                    f'Origen: {movement.source_warehouse.name}\n' \
                    f'Destino: {movement.destination_warehouse.name}'

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    recipients,
                    fail_silently=False
                )
            except Exception as e:
                print(f"Error al enviar correo: {e}")  
