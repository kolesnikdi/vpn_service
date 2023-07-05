import pyotp

from two_factor_authentication.models import GoogleAuth
from two_factor_authentication.serializers import GoogleAuthSerializer
from Web_Menu_DA import settings
from Web_Menu_DA.constants import Types2FA

MSG_TPL = 'Two-factor verification {}'


def setup_2fa(request_2fa, user):
    """
    :type request_2fa: Web_Menu_DA.constants.Types2FA
    :type user: registration.models.WebMenuUser
    :return: dict
    """
    result = {}
    if request_2fa == Types2FA.DISABLED:
        result = {'msg': MSG_TPL.format('successfully disabled.')}
    elif request_2fa == Types2FA.EMAIL:
        result = {'msg': MSG_TPL.format('with your email successfully enabled')}
    elif request_2fa == Types2FA.GAUTH:
        if previous_gauth := GoogleAuth.objects.filter(owner_id=user.id).last():
            previous_gauth.is_active = False
            previous_gauth.save()
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(name=user.email.lower(), issuer_name="Web_Menu_DA")
        new_gauth = GoogleAuth.objects.create(owner_id=user.id, otp_base32=otp_base32, otp_auth_url=otp_auth_url)
        response = GoogleAuthSerializer(instance=new_gauth).data
        response['msg'] = MSG_TPL.format('with your Google successfully enabled.')
        response['redirect to'] = f'{settings.HOST}/enable2fa/display_qr'
        result = response

    user.type_2fa = request_2fa
    user.save()
    return result
