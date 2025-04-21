from rest_framework import serializers

from cms.models import Campaign
from cms.serializers import CampaignRulesReadOnlySerializer


class CampaignSerializer(serializers.ModelSerializer):
    rules = CampaignRulesReadOnlySerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
