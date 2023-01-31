from rest_framework import generics, status
from rest_framework.response import Response

from client.serializers import ClientSerializer
from registration.models import RegistrationTry
from registration.serializers import RegisterConfirmSerializer, CreateRegisterTrySerializer
from registration.business_logic import final_send_mail, final_creation
from Web_Menu_DA.permissions import IsNotAuthenticated

"""Next 12 string need for correct work knox Authentication"""

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class RegisterTryView(generics.CreateAPIView):
    serializer_class = CreateRegisterTrySerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reg_try = serializer.save()
        final_send_mail(reg_try)

        return Response(
            self.serializer_class(instance=reg_try).data,
            status=status.HTTP_201_CREATED,
        )


class RegisterConfirmView(generics.CreateAPIView):
    serializer_class = RegisterConfirmSerializer
    permission_classes = [IsNotAuthenticated]
    queryset = RegistrationTry.objects.all()
    lookup_field = 'code'

    def post(self, request, *args, **kwargs):
        serializer_context = {'request': request}  # need to use HyperlinkedModelSerializer in ClientSerializer
        reg_try = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = final_creation(serializer.validated_data, reg_try)

        return Response(  # todo Make variable for different requests (Client, owner, manager)
            ClientSerializer(instance=user, context=serializer_context).data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """Check confirmation_time if it is null then allows to make registration"""
        queryset = self.queryset.filter(
            confirmation_time__isnull=True,
        )
        return queryset
