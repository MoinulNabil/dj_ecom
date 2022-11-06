import os
from io import BytesIO

import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

from order.models import Order

@shared_task
def send_email_with_pdf(order_id, subject, message, recipients):
    model = Order
    order = model.objects.get(id=order_id)
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipients
    )
    html = render_to_string('pdf.html', {"order": order})
    output = BytesIO()
    stylesheets = [weasyprint.CSS(os.path.join(settings.STATIC_ROOT, 'css/pdf.css'))]
    weasyprint.HTML(
        string=html
    ).write_pdf(
        output,
        stylesheets=stylesheets
    )
    email.attach(
        f"order_{order_id}.pdf",
        output.getvalue(),
        'application/pdf'
    )
    email.send()