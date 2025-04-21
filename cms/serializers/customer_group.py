from rest_framework import serializers

from cms.models import CustomerGroup


class CustomerGroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text="List of customer IDs in this group",
    )

    class Meta:
        model = CustomerGroup
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def get_member_count(self, obj):
        return obj.members.count()
