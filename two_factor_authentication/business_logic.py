""" Two-factor verification.
Realised as a decorator @enabled_2fa()
Can be executed on any Views method
It can perform any verification method provided here. Now it (Email, Google Authentication)
The verification method is set in WebMenuUser.type_2fa
"""
# Google Authentication - in development
# Can be switched on forcibly - in development
import os
import random
from functools import wraps

from django.core.mail import send_mail
from django.core.cache import cache
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.response import Response

from Web_Menu_DA.settings import CACHE_TIMEOUT_2FA


def enabled_2fa():
    def decorator(func):
        @wraps(func)
        def early_exit(self, request, *args, **kwargs):
            """Checks whether the user is authorised and has Two-factor verification."""
            if request.user.is_authenticated:  # and request.user.type_2fa # todo check if 2fa is on in user model
                error_response = perform_2fa_request(request)
                if error_response:
                    return error_response
            return func(self, request, *args, **kwargs)

        return early_exit

    return decorator


class Base2FA:
    """Base class for Two-factor verification.
    Includes:
    1. Persistent Responses
    2. Persistent methods for checking or performing Two-factor
    verification.
    The methods (_perform_2fa, _check_2fa) have a state that obliges
    to override them for each unique class that inherits this class"""
    already_exists = Response(
        data={'error': 'You already have unfinished 2fa confirmation.'},
        status=status.HTTP_400_BAD_REQUEST,
    )
    code_expired = Response(
        data={'error': 'Your code is already expired. Request a new one.'},
        status=status.HTTP_400_BAD_REQUEST,
    )
    not_valid = Response(
        data={'error': 'Not valid 2fa data.'},
        status=status.HTTP_400_BAD_REQUEST,
    )
    auth2fa_type = None

    @classmethod
    def _approve_answer(cls):
        msg = {
            'error': '2fa required',
            'hint': 'Put received code into HTTP_2FACODE header and send request again.',
            'msg': f'Check your {cls.auth2fa_type} for code'
            }
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def perform_2fa(cls, user):
        """methods that obliges to override _perform_2fa"""
        return cls._perform_2fa(user)

    @classmethod
    def _perform_2fa(cls, user):
        raise NotImplementedError

    @classmethod
    def check_2fa(cls, user, code):
        """methods that obliges to override _check_2fa"""
        return cls._check_2fa(user, code)

    @classmethod
    def _check_2fa(cls, user, code):
        raise NotImplementedError


class Cache2FA(Base2FA):
    """This class is intended for followers that use the cache to write 2fa code """
    cache_delay = 300

    @classmethod
    def cache_set(cls, user):
        code_2fa = ''.join(random.choices('123456789', k=6))
        cache.set(user.id, {'code': code_2fa}, cls.cache_delay)
        return code_2fa


class Auth2FAEmail(Cache2FA):
    """Class which uses Email for checking or performing Two-factor verification"""
    auth2fa_type = 'Email'
    cache_delay = CACHE_TIMEOUT_2FA.get(auth2fa_type)

    @classmethod
    def _perform_2fa(cls, user):
        """Method that:
        1. Checks if 2fa code already exists.
        2. If the 2fa code doesn't exist, this method will create and send it to email.
        returns a Response depending on the state of execution."""
        if cache.get(user.id, None):
            return cls.already_exists

        code_2fa = cls.cache_set(user)
        context = {
            'code_2fa': f'{code_2fa}',
        }
        confirmation_email = {
            'subject': 'Personal code for Two-Factor Authentication',
            'message': 'Personal code for Two-Factor Authentication',
            'from_email': os.environ.get('auth_user'),
            'recipient_list': [user.email],
            'fail_silently': False,
            'auth_user': os.environ.get('auth_user'),
            'auth_password': os.environ.get('email_token'),
            'html_message': render_to_string('2fa_mail.html', context=context),
        }
        send_mail(**confirmation_email)

        return cls._approve_answer()

    @classmethod
    def _check_2fa(cls, user, received_code):
        """Method that:
        1. Checks if system 2fa code exists.
        2. Checks if system 2fa code identical to the users 2fa code.
        returns a Response depending on the state of execution or delete
        system 2fa code."""
        cache_code = cache.get(user.id, {}).get('code', None)
        if not cache_code:
            return cls.code_expired
        if cache_code != received_code:
            return cls.not_valid

        cache.delete(user.id)   # 2fa already passed so we deleted code from cache


class Auth2FAGAUTH(Base2FA):
    """Class which uses Google Authentication for checking or performing
    Two-factor verification"""
    pass


def perform_2fa_request(request):
    """ An Abstraction that defines the type of Two-factor
    verification. Performs primary routing depending on the
    presence of request.header. """

    user = request.user
    # if user.type_2fa == 'email'
    Auth2FAClass = Auth2FAEmail

    if not (received_code := request.META.get('HTTP_2FACODE', None)):
        return Auth2FAClass.perform_2fa(user)

    return Auth2FAClass.check_2fa(user, received_code)
