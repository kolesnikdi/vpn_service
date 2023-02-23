from rest_framework import generics, status
from rest_framework.response import Response


from registration.models import RegistrationTry, WebMenuUser
from registration.serializers import RegisterConfirmSerializer, CreateRegisterTrySerializer, WebMenuUserSerializer,\
    LoginWebMenuUserSerializer
from registration.business_logic import final_send_mail, final_creation
from Web_Menu_DA.permissions import IsNotAuthenticated

"""Next 12 string need for correct work knox Authentication"""

from django.contrib.auth import login

from rest_framework import permissions
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class WebMenuUserViewSet(generics.RetrieveAPIView):
#     queryset = WebMenuUser.objects.all().order_by('-date_joined')   # todo
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WebMenuUserSerializer
    authentication_classes = (TokenAuthentication,)    # need in every view wear authentication is necessarily

    def get_object(self):
        return self.request.user


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginWebMenuUserSerializer   # todo
    authentication_classes = []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # login(request, user)
        token = AuthToken.objects.create(user)[1]

        print(request.headers)
        # return super(LoginView, self).post(request, format=None)
        return Response({
                    "user": WebMenuUserSerializer(user).data,
                    "token": token     # todo
                })


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
        reg_try = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = final_creation(serializer.validated_data, reg_try)

        return Response(  # todo Make variable for different requests (Client, owner, manager)
            WebMenuUserSerializer(instance=user).data,   # todo return variable for different requests (Client, owner, manager)
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        """Check confirmation_time if it is null then allows to make registration"""
        queryset = self.queryset.filter(
            confirmation_time__isnull=True,
        )
        return queryset
