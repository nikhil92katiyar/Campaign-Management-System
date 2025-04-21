import uuid

from django.core.validators import MinValueValidator
from django.db import models

from cms.models import Customer, CustomerGroup


class Campaign(models.Model):
    DISCOUNT_TARGET_CHOICES = [
        ("CART", "Cart Value Discount"),
        ("DELIVERY", "Delivery Fee Discount"),
    ]

    DISCOUNT_CALCULATION_TYPE = [
        ("PERCENTAGE", "Discount as percentage of value"),
        ("FIXED", "Discount as fixed amount"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    discount_target = models.CharField(
        max_length=10, choices=DISCOUNT_TARGET_CHOICES
    )
    discount_value = models.FloatField(validators=[MinValueValidator(0)])
    discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_CALCULATION_TYPE
    )

    min_cart_value = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )
    max_discount_amount = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )

    total_budget = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True
    )

    max_uses_per_customer = models.PositiveIntegerField(null=True, blank=True)
    max_uses_total = models.PositiveIntegerField(null=True, blank=True)

    target_groups = models.ManyToManyField(CustomerGroup, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "start_date", "end_date"]),
        ]


class CampaignUsage(models.Model):
    idempotent_key = models.UUIDField(primary_key=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="usages"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="campaign_usages"
    )
    used_at = models.DateTimeField(auto_now_add=True)
    discount_amount = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["campaign", "customer"]),
        ]
