import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

from registration.models import WebMenuUser


def final_send_mail(reg_try):
    context = {                                             #    """ more data in context to customisation email"""
        'registration_link': f'{settings.HOST}/registration/{reg_try.code}',
        'registration_link2': f'{settings.HOST}/registration/djangofunction/{reg_try.code}'
    }

    registration_mail = {
        'subject': 'Web_Menu_DA registration',
        'message': 'Web_Menu_DA registration',
        'from_email': os.environ.get('auth_user', 'segareta@ukr.net'),
        'recipient_list': [reg_try.email],
        'fail_silently': False,
        'auth_user': os.environ.get('auth_user', 'segareta@ukr.net'),
        'auth_password': os.environ.get('email_token', 'Y32RepfABOJMYyui'),
        'html_message': render_to_string('registration_mail.html', context=context),
    }
    send_mail(**registration_mail)


def final_creation(validated_data, reg_try):
    user = WebMenuUser.objects.create(
        mobile_phone=validated_data['mobile_phone'],
        email=reg_try.email,
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        fathers_name=validated_data['fathers_name'],
        country=validated_data['country'],
        city=validated_data['city'],
        street=validated_data['street'],
        house_number=validated_data['house_number'],
        flat_number=validated_data['flat_number'],
        passport_series=validated_data['passport_series'],
        passport_number=validated_data['passport_number'],
        passport_date_of_issue=validated_data['passport_date_of_issue'],
        passport_issuing_authority=validated_data['passport_issuing_authority'],
    )

    user.set_password(validated_data['password'])
    user.save()
    reg_try.confirmation_time = timezone.now()
    reg_try.save()
    return user
