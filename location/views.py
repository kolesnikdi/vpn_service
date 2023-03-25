from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from location.models import Location
from location.serializers import CreateLocationSerializer, LocationSerializer
from Web_Menu_DA.permissions import IsOwnerOr404


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOr404]
    serializer_class = LocationSerializer

    def get_queryset(self):
        # queryset = Location.objects.all().order_by('id') this one take all location and next one only owners locations
        # that filter through the company
        return Location.objects.filter(company__owner_id=self.request.user.id).order_by('id')
        # .order_by('id') to improve UnorderedObjectListWarning: Pagination may yield inconsistent results with
        # an unordered object_list


class CreateLocationView(viewsets.ModelViewSet):
    serializer_class = CreateLocationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOr404]

    # check password in all action [post, put] don't work for destroy
    def get_serializer(self, *args, **kwargs):
        context = kwargs.setdefault('context', {})  # if no dict in kwargs we make it
        # join user to the serializer context for opportunity def validate in CreateCompanySerializer
        context['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Location.objects.filter(company__owner_id=self.request.user.id).order_by('id')

