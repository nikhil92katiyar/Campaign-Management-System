from django.contrib.postgres.fields import ArrayField
from django.db import models

from cms.models import Campaign


class PaymentMethodRule(models.Model):
    METHODS = [
        ("CC", "Credit Card"),
        ("DC", "Debit Card"),
        ("UPI", "UPI"),
        ("COD", "Cash on Delivery"),
    ]
    name = models.CharField(max_length=100)
    methods = ArrayField(models.CharField(max_length=5, choices=METHODS))
    created_at = models.DateTimeField(auto_now_add=True)


class LocationTierRule(models.Model):
    TIERS = [("TIER1", "TIER1"), ("TIER2", "TIER2"), ("TIER3", "TIER3")]
    name = models.CharField(max_length=100)
    tiers = ArrayField(models.CharField(max_length=5, choices=TIERS))
    created_at = models.DateTimeField(auto_now_add=True)


class UserPriorityRule(models.Model):
    PRIORITIES = [(1, "Platinum"), (2, "Gold"), (3, "Silver")]
    name = models.CharField(max_length=100)
    priorities = ArrayField(models.IntegerField(choices=PRIORITIES))
    created_at = models.DateTimeField(auto_now_add=True)


class MinCartValueRule(models.Model):
    name = models.CharField(max_length=100)
    min_value = models.FloatField()
    max_discount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class CampaignRules(models.Model):
    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name="rules",
        verbose_name="Associated Campaign",
    )
    payment_rules = models.ForeignKey(
        PaymentMethodRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_campaigns",
    )

    location_rules = models.ForeignKey(
        LocationTierRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="location_campaigns",
    )

    priority_rules = models.ForeignKey(
        UserPriorityRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="priority_campaigns",
    )

    min_cart_rule = models.OneToOneField(
        MinCartValueRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mincart_campaigns",
    )
