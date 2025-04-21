from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone

from cms.models import Campaign
from cms.models.campaign import CampaignUsage


class CacheKeysService:
    ACTIVE_CAMPAIGNS = "active_campaigns"

    @classmethod
    def active_campaigns(cls):
        return cls.ACTIVE_CAMPAIGNS

    @classmethod
    def campaign_key(cls, camp_id):
        return f"campaign:{camp_id}"

    @classmethod
    def campaign_total_allowed_usage_key(cls, camp_id):
        return f"campaign:{camp_id}:total_allowed_usage"

    @classmethod
    def campaign_total_allowed_count_key(cls, camp_id):
        return f"campaign:{camp_id}:total_allowed_count"

    @classmethod
    def campaign_current_usage_key(cls, camp_id):
        return f"campaign:{camp_id}:current_usage"

    @classmethod
    def campaign_current_count_key(cls, camp_id):
        return f"campaign:{camp_id}:current_count"

    @classmethod
    def campaign_user_current_count_key(cls, camp_id, user_id):
        return f"campaign:{camp_id}:{user_id}:current_count"

    @classmethod
    def campaign_user_max_allowed_count_key(cls, camp_id):
        return f"campaign:{camp_id}:max_uses_per_day_customer"

    @classmethod
    def idempotent_discount_key(cls, customer_id, idempotent_key):
        return f"idempotent:{customer_id}:{idempotent_key}"


class CampaignsCacheService:
    BUDGET_CONSUMPTION_PERCENTAGE = 0.99

    @classmethod
    def add_max_allowed_params_to_cache(cls, campaign, timeout):
        cache.set(
            CacheKeysService.campaign_total_allowed_usage_key(campaign.id),
            campaign.total_budget,
            timeout,
        )

        cache.set(
            CacheKeysService.campaign_user_max_allowed_count_key(campaign.id),
            campaign.max_uses_per_customer,
            timeout,
        )

        cache.set(
            CacheKeysService.campaign_total_allowed_count_key(campaign.id),
            campaign.max_uses_total,
            timeout,
        )

    @classmethod
    def process_single_campaign(cls, campaign):
        total_discount = (
            campaign.usages.all()
            .aggregate(Sum("discount_amount"))
            .get("discount_amount__sum", 0)
        )
        # stopping at 99% of total budget
        if isinstance(total_discount, (int, float)) and total_discount >= (
            campaign.total_budget * cls.BUDGET_CONSUMPTION_PERCENTAGE
        ):
            return None

        if (
            CampaignUsage.objects.filter(campaign=campaign).count()
            >= campaign.max_uses_total
        ):
            return None

        timeout = cls._calculate_timeout_with_grace(campaign.end_date)
        cls.add_max_allowed_params_to_cache(campaign, timeout)

        new_data = cls._serialize_campaign(campaign)

        cache.set(
            CacheKeysService.campaign_key(camp_id=campaign.id),
            new_data,
            timeout,
        )
        return str(campaign.id)

    @classmethod
    def refresh_single_campaign(cls, campaign_id):
        try:
            campaign = (
                Campaign.objects.select_related(
                    "rules",
                    "rules__payment_rules",
                    "rules__location_rules",
                    "rules__priority_rules",
                )
                .prefetch_related("target_groups")
                .get(id=campaign_id)
            )

            return cls.process_single_campaign(campaign)
        except Campaign.DoesNotExist:
            return None

    @classmethod
    def refresh_cache(cls):
        now = timezone.now()
        active_campaigns = (
            Campaign.objects.filter(
                is_active=True, start_date__lte=now, end_date__gte=now
            )
            .select_related(
                "rules",
                "rules__payment_rules",
                "rules__location_rules",
                "rules__priority_rules",
            )
            .prefetch_related("target_groups")
        )

        campaign_ids = []
        for campaign in active_campaigns:
            id = cls.process_single_campaign(campaign)
            if id:
                campaign_ids.append(id)
        cache.set(
            CacheKeysService.active_campaigns(), campaign_ids, 24 * 60 * 60
        )
        return campaign_ids

    @classmethod
    def _calculate_timeout_with_grace(cls, end_date):
        remaining = (end_date - timezone.now()).total_seconds() + (
            10 * 60
        )  # grace of 10mins
        return int(remaining)

    @classmethod
    def get_all_campaigns(cls):
        campaign_ids = cache.get(CacheKeysService.active_campaigns())
        if not campaign_ids:
            campaign_ids = cls.refresh_cache()

        campaigns = []
        for cid in campaign_ids:
            campaign = cls.get_campaign(cid)
            if campaign:
                campaigns.append(campaign)

        return campaigns

    @classmethod
    def _serialize_campaign(cls, campaign):
        return {
            "id": str(campaign.id),
            "name": campaign.name,
            "discount_type": campaign.discount_type,
            "discount_value": campaign.discount_value,
            "discount_target": campaign.discount_target,
            "rules": cls._serialize_rules(campaign.rules),
            "target_group_ids": [
                str(g.id) for g in campaign.target_groups.all()
            ],
            "max_uses_per_customer": campaign.max_uses_per_customer,
            "max_uses_total": campaign.max_uses_total,
            "total_budget": campaign.total_budget,
            "max_discount_amount": campaign.max_discount_amount,
        }

    @classmethod
    def _serialize_rules(cls, rules):
        payment_methods = (
            rules.payment_rules.methods if rules.payment_rules.methods else []
        )
        location_tiers = (
            rules.location_rules.tiers if rules.location_rules.tiers else []
        )
        priorities = (
            rules.priority_rules.priorities
            if rules.priority_rules.priorities
            else []
        )
        min_cart_value = (
            rules.min_cart_rule.min_value if rules.min_cart_rule else None
        )
        max_discount = (
            rules.min_cart_rule.max_discount if rules.min_cart_rule else None
        )
        return {
            "payment_methods": payment_methods,
            "location_tiers": location_tiers,
            "priorities": priorities,
            "min_cart_value": min_cart_value,
            "max_discount": max_discount,
        }

    @classmethod
    def get_campaign(cls, campaign_id):
        return cache.get(CacheKeysService.campaign_key(campaign_id))
