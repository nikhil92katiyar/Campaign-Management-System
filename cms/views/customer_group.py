from rest_framework import generics

from cms.models import CustomerGroup
from cms.serializers import CustomerGroupSerializer


class CustomerGroupList(generics.ListAPIView):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer


class CustomerGroupDetail(generics.RetrieveAPIView):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer
    lookup_field = "id"
