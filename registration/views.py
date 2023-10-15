from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.views import LoginView as KnoxLoginView

from registration.models import WebUser
from registration.serializers import RegisterConfirmSerializer, WebUserSerializer, LoginWebMenuUserSerializer, \
    WebUserUpdateSerializer
from vpn_service.permissions import IsNotAuthenticated, IsOwnerOr404


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny, IsNotAuthenticated)
    serializer_class = LoginWebMenuUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        request.user = user
        response = super(LoginView, self).post(request, format=None)

        return Response(response.data, status=status.HTTP_201_CREATED)


class RegisterConfirmView(generics.CreateAPIView):
    serializer_class = RegisterConfirmSerializer
    permission_classes = [IsNotAuthenticated]
    queryset = WebUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = WebUser.objects.create_user(**serializer.validated_data)
        return Response(WebUserSerializer(instance=user).data, status=status.HTTP_201_CREATED)


class WebUserViewSet(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebUserSerializer

    def get_object(self):
        return self.request.user


class WebUserUpdateView(generics.UpdateAPIView):
    """Partial update any field"""
    queryset = WebUser.objects.all()
    serializer_class = WebUserUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
