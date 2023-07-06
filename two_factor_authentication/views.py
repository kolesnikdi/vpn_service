import qrcode
import qrcode.image.svg
from io import BytesIO

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from two_factor_authentication.business_logic import setup_2fa, enable_2fa
from two_factor_authentication.models import GoogleAuth
from two_factor_authentication.serializers import Enable2faSerializer


class Enable2FAView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Enable2faSerializer

    @enable_2fa(force=True)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        response = {'error': 'Something went wrong. Contact the site administrator.'}
        res_status = status.HTTP_400_BAD_REQUEST
        with transaction.atomic():
            response = setup_2fa(serializer.validated_data['type_2fa'], request.user) or response
            res_status = status.HTTP_200_OK
        return Response(response, status=res_status)


class DisplayQrView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'display_qr_template.html'

    def get(self, request, *args, **kwargs):
        gauth = get_object_or_404(GoogleAuth, owner=request.user, is_active=True, is_hidden=False)
        img = qrcode.make(gauth.otp_auth_url, image_factory=qrcode.image.svg.SvgPathImage, box_size=38)
        stream = BytesIO()
        img.save(stream)
        gauth.is_hidden = True
        gauth.save()
        return Response({'otp_base32': gauth.otp_base32, 'svg': stream.getvalue().decode()}, status=status.HTTP_200_OK)
