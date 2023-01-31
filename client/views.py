from django.contrib.auth.models import User

from rest_framework import viewsets

from client.serializers import ClientSerializer, ClientSerializerPutPost
from Web_Menu_DA.permissions import IsAdminUserOrReadOnly


class ClientViewSet(viewsets.ModelViewSet):  # todo Change according to a new project
    # turn off 'POST' - viewsets.ReadOnlyModelViewSet
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):  # todo Can't remember for why i need this code
        """"Allows to change Serializer according to the request method"""
        if self.request.method in ['POST', 'PUT']:
            return ClientSerializerPutPost
        return self.serializer_class
