from rest_framework import generics

from cms.models import (
    Campaign,
    CampaignRules,
    LocationTierRule,
    MinCartValueRule,
    PaymentMethodRule,
    UserPriorityRule,
)
from cms.serializers import (
    CampaignRulesSerializer,
    CampaignSerializer,
    LocationTierRuleSerializer,
    MinCartValueRuleSerializer,
    PaymentMethodRuleSerializer,
    UserPriorityRuleSerializer,
)


class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class CampaignRulesListCreateView(generics.ListCreateAPIView):
    queryset = CampaignRules.objects.all()
    serializer_class = CampaignRulesSerializer


class CampaignRulesRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = CampaignRules.objects.all()
    serializer_class = CampaignRulesSerializer


class PaymentMethodRuleListCreateView(generics.ListCreateAPIView):
    queryset = PaymentMethodRule.objects.all()
    serializer_class = PaymentMethodRuleSerializer


class PaymentMethodRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentMethodRule.objects.all()
    serializer_class = PaymentMethodRuleSerializer


class LocationTierRuleListCreateView(generics.ListCreateAPIView):
    queryset = LocationTierRule.objects.all()
    serializer_class = LocationTierRuleSerializer


class LocationTierRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationTierRule.objects.all()
    serializer_class = LocationTierRuleSerializer


class UserPriorityRuleListCreateView(generics.ListCreateAPIView):
    queryset = UserPriorityRule.objects.all()
    serializer_class = UserPriorityRuleSerializer


class UserPriorityRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPriorityRule.objects.all()
    serializer_class = UserPriorityRuleSerializer


class MinCartValueRuleListCreateView(generics.ListCreateAPIView):
    queryset = MinCartValueRule.objects.all()
    serializer_class = MinCartValueRuleSerializer


class MinCartValueRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MinCartValueRule.objects.all()
    serializer_class = MinCartValueRuleSerializer
