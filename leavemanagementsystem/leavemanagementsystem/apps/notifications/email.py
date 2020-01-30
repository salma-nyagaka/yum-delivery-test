from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from leavemanagementsystem.apps.authentication.backends import \
    JWTAuthentication
import pdb


def send_email(request, username, email, start, end, leave_status):
    # sends email with the activation link with the token
    subject = 'Notificaiton blah blah'
    message = 'blah blah'
    # pdb.set_trace()
    domain = get_current_site(request).domain
    token = JWTAuthentication.generate_token(username)
    protocol = request.META['SERVER_PROTOCOL'][:4]
    notification_link = protocol + '://' + domain + '/api/auth/' + token
    body = render_to_string('notification.html', {
        'link': notification_link,
        'name': username,
        'start': start,
        'end': end,
        'status': leave_status
    })
    # pdb.set_trace()
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=body,
        )
    except Exception:
        return Response(data={"message": "blah blah failed"},
                        status=status.HTTP_400_BAD_REQUEST)
