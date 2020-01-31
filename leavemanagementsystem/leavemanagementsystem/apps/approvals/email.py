from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from leavemanagementsystem.apps.authentication.backends import \
    JWTAuthentication


def send_email(request, username, email, start_date, end_date, status_update):
    """
    Method to send notification email to users
    """
    subject = 'Leave update'
    message = 'Status on your leave update'
    domain = get_current_site(request).domain
    token = JWTAuthentication.generate_token(username)
    protocol = request.META['SERVER_PROTOCOL'][:4]
    notification_link = protocol + '://' + domain + '/api/auth/' + token
    body = render_to_string('notification.html', {
        'link': notification_link,
        'name': username,
        'start': start_date,
        'end': end_date,
        'status': status_update
    })
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=body,
        )
    except Exception:
        return Response(data={"message": "This request has failed"},
                        status=status.HTTP_400_BAD_REQUEST)
