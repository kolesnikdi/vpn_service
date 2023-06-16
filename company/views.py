from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from company.serializers import CreateCompanySerializer, CompanySerializer
from Web_Menu_DA.permissions import IsOwnerOr404
# from Web_Menu_DA.permissions import IsOwnerOr404, TwoFactorAuthenticationOrRedirect


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOr404]
    serializer_class = CompanySerializer

    def get_queryset(self):
        # add .order_by('id') to improve UnorderedObjectListWarning: Pagination may yield inconsistent results with
        # an unordered object_list
        return self.request.user.company.all().order_by('id')


class CreateCompanyView(viewsets.ModelViewSet):
    serializer_class = CreateCompanySerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]
    # permission_classes = [IsAuthenticated, IsOwnerOr404, TwoFactorAuthenticationOrRedirect] #todo delete


    def get_queryset(self):
        return self.request.user.company.all().order_by('id')

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # check password in all action [post, put] don't work for destroy
    def get_serializer(self, *args, **kwargs):
        context = kwargs.setdefault('context', {})  # if no dict in kwargs we make it
        # join user to the serializer context for opportunity def validate in CreateCompanySerializer
        context['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)

    # check password only in one action
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data, context={'user': request.user})
    #     serializer.is_valid(raise_exception=True)
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """signs the company by name of user."""
        serializer.save(owner=self.request.user)
