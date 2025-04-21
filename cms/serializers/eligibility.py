from rest_framework import serializers

from cms.models.campaign_rules import (
    LocationTierRule,
    PaymentMethodRule,
    UserPriorityRule,
)


class CampaignEligibilitySerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    cart_value = serializers.FloatField(required=True)
    delivery_fee = serializers.FloatField(required=True)
    payment_method = serializers.ChoiceField(
        choices=PaymentMethodRule.METHODS, required=True
    )
    user_priority = serializers.ChoiceField(
        choices=UserPriorityRule.PRIORITIES, required=False
    )
    location_tier = serializers.ChoiceField(
        choices=LocationTierRule.TIERS, required=False
    )


class CampaignResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    discount_value = serializers.FloatField()
    discount_type = serializers.CharField(max_length=50)
    discount_target = serializers.CharField(max_length=50)
    max_discount_amount = serializers.FloatField()
