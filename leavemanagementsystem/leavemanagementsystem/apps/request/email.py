from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from leavemanagementsystem.apps.authentication.backends import \
     JWTAuthentication
from leavemanagementsystem.apps.authentication.models import \
    User

import pdb


# def send_email(request, request_data):
#     # sends email with the activation link with the token
#     subject = 'Kari4me activation email'
#     message = 'Please verify your account '
#     domain = get_current_site(request).domain
#     username = User.objects.values_list('username', flat=True).filter(id=request.user.id)
#     email = User.objects.values_list('email', flat=True).filter(id=request.user.id)

#     # pdb.set_trace()
#     token = JWTAuthentication.generate_token(username[0])
#     protocol = request.META['SERVER_PROTOCOL'][:4]
#     activation_link = protocol + '://' + domain + '/api/request/' + token
#     body = render_to_string('verify_account.html', {
#         'link': activation_link,
#         'name': username[0]
#     })
#     leave_data = {
#         "start_date": request_data['start_date'],
#         "end_date": request_data['end_date'],
#         "description": request_data['description'],
#         "username": username[0],
#         "email":  email[0]
#     }

#     try:
#         send_mail(
#             subject,
#             message,
#             leave_data,
#             settings.EMAIL_HOST_USER,
#             'salmanyagaka@mail.com',
#             html_message=body,
#         )
#     except Exception:
#         return Response(data={"message": ""},
#                         status=status.HTTP_400_BAD_REQUEST)
def send_email(request, user):
    # sends email with the activation link with the token
    subject = 'Kari4me blebleh email'
    message = 'yeyeyeyye '
    domain = get_current_site(request).domain
    token = JWTAuthentication.generate_token('salmanyagaka')
    protocol = request.META['SERVER_PROTOCOL'][:4]
    activation_link = protocol + '://' + domain + '/api/auth/' + token
    body = render_to_string('verify_account.html', {
        'link': activation_link,
        'name': 'salmanyagaka'
    })
    # pdb.set_trace()

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            'nyagzasalma@gmail.com',
            html_message=body,
        )
    except Exception:
        return Response(data={"message": "Email activation failed"},
                        status=status.HTTP_400_BAD_REQUEST)
