from rest_framework import serializers

from cms.models import (
    CampaignRules,
    LocationTierRule,
    MinCartValueRule,
    PaymentMethodRule,
    UserPriorityRule,
)


class PaymentMethodRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodRule
        fields = "__all__"


class LocationTierRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationTierRule
        fields = "__all__"


class UserPriorityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPriorityRule
        fields = "__all__"


class MinCartValueRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinCartValueRule
        fields = "__all__"


class CampaignRulesReadOnlySerializer(serializers.ModelSerializer):
    payment_rules = PaymentMethodRuleSerializer(read_only=True)
    location_rules = LocationTierRuleSerializer(read_only=True)
    priority_rules = UserPriorityRuleSerializer(read_only=True)
    min_cart_rule = MinCartValueRuleSerializer(read_only=True)

    class Meta:
        model = CampaignRules
        fields = "__all__"


class CampaignRulesSerializer(serializers.ModelSerializer):
    payment_rules = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethodRule.objects.all(),
        required=False,
        allow_null=True,
    )
    location_rules = serializers.PrimaryKeyRelatedField(
        queryset=LocationTierRule.objects.all(),
        required=False,
        allow_null=True,
    )
    priority_rules = serializers.PrimaryKeyRelatedField(
        queryset=UserPriorityRule.objects.all(),
        required=False,
        allow_null=True,
    )
    min_cart_rule = serializers.PrimaryKeyRelatedField(
        queryset=MinCartValueRule.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CampaignRules
        fields = "__all__"
        extra_kwargs = {
            "payment_rules": {"required": False},
            "location_rules": {"required": False},
            "priority_rules": {"required": False},
            "min_cart_rule": {"required": False},
        }

    def create(self, validated_data):
        payment_rule_id = validated_data.pop("payment_rules", None)
        location_rule_id = validated_data.pop("location_rules", None)
        priority_rule_id = validated_data.pop("priority_rules", None)
        min_cart_rule_id = validated_data.pop("min_cart_rule", None)

        campaign_rules = CampaignRules.objects.create(**validated_data)

        if payment_rule_id:
            campaign_rules.payment_rules = payment_rule_id
        if location_rule_id:
            campaign_rules.location_rules = location_rule_id
        if priority_rule_id:
            campaign_rules.priority_rules = priority_rule_id
        if min_cart_rule_id:
            campaign_rules.min_cart_rule = min_cart_rule_id

        campaign_rules.save()
        return campaign_rules

    def update(self, instance, validated_data):
        payment_rule_id = validated_data.pop("payment_rules", None)
        location_rule_id = validated_data.pop("location_rules", None)
        priority_rule_id = validated_data.pop("priority_rules", None)
        min_cart_rule_id = validated_data.pop("min_cart_rule", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if payment_rule_id is not None:
            instance.payment_rules = payment_rule_id
        if location_rule_id is not None:
            instance.location_rules = location_rule_id
        if priority_rule_id is not None:
            instance.priority_rules = priority_rule_id
        if min_cart_rule_id is not None:
            instance.min_cart_rule = min_cart_rule_id

        instance.save()
        return instance
