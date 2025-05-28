from django.core.mail import send_mail
from django.template.loader import render_to_string

def enviar_correo(destinatario, asunto, plantilla, contexto):
    cuerpo = render_to_string(plantilla, contexto)
    send_mail(
        subject=asunto,
        message='',
        html_message=cuerpo,
        from_email=None,
        recipient_list=[destinatario],
        fail_silently=False
    )
