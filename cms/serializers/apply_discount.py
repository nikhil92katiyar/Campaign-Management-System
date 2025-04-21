from rest_framework import serializers


class DiscountRequestSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField()
    idempotent_key = serializers.UUIDField()
    discount = serializers.FloatField()
    campaign_id = serializers.UUIDField()
