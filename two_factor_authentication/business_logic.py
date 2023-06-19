import os
import uuid
import random
from functools import wraps

from django.core.mail import send_mail
from django.core.cache import cache
from django.http import JsonResponse
from django.template.loader import render_to_string

from rest_framework import status

from registration.models import WebMenuUser


def enabled_2fa(timeout):

    def decorator(func):
        @wraps(func)
        def check_headers(self, request, *args, **kwargs):
            # if request.user.type_2fa is not None:
            if 'HTTP_2FACODE' in request.META.keys() and 'HTTP_2FATOKEN' in request.META.keys():
                # code_2fa, token_2fa = creation_2fa_data_and_cache(timeout, request.user.id)
                ff = request.META['HTTP_2FATOKEN']
                if cache_data := cache.get(request.META['HTTP_2FATOKEN'], None):
                    # import ipdb
                    # ipdb.set_trace()
                    if request.user.id == cache_data[1] and request.META['HTTP_2FACODE'] == cache_data[0]:
                        return func(self, request, *args, **kwargs)
                else:
                    return JsonResponse({'error': 'Not valid 2fa data', }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # token_2fa = manufacture_2fa(timeout, request.user)
                code_2fa, token_2fa = creation_2fa_data_and_cache(timeout, request.user.id)
                # return JsonResponse({'error': '2fa required', 'token': token_2fa}, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse({'error': '2fa required', 'token': token_2fa, 'code': code_2fa}, status=status.HTTP_400_BAD_REQUEST)

            return func(self, request, *args, **kwargs)
        return check_headers
    return decorator


def manufacture_2fa(timeout, user):
    code_2fa, token_2fa = creation_2fa_data_and_cache(timeout, user.id)
    # send_2FA(code_2fa, user)
    return token_2fa

def creation_2fa_data_and_cache(timeout, user_id):
    code_2fa = ''.join(random.choice('123456789') for i in range(6))
    token_2fa = uuid.uuid4()
    cache.set(token_2fa, (code_2fa, user_id), timeout['2fa'])
    return code_2fa, token_2fa

def send_2FA(code_2fa, user):
    # send_to = user.type_2fa
    send_to = 'email'
    if send_to == 'email':
        context = {
            'code_2fa': f'{code_2fa}',
        }

        registration_mail = {
            'subject': 'Personal code for Two-Factor Authentication',
            'message': 'Personal code for Two-Factor Authentication',
            'from_email': os.environ.get('auth_user', 'segareta@ukr.net'),
            'recipient_list': [user.email],
            'fail_silently': False,
            'auth_user': os.environ.get('auth_user', 'segareta@ukr.net'),
            'auth_password': os.environ.get('email_token', 'Y32RepfABOJMYyui'),
            'html_message': render_to_string('2fa_mail.html', context=context),
        }
        send_mail(**registration_mail)
    else:
        pass
