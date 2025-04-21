from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from cms.models import Campaign
from utils import CacheKeysService, CampaignsCacheService


@receiver(post_save, sender=Campaign)
def refresh_campaign_cache_on_save(sender, instance, **kwargs):
    CampaignsCacheService.refresh_single_campaign(instance.id)


@receiver(post_delete, sender=Campaign)
def clear_campaign_cache_on_delete(sender, instance, **kwargs):
    campaign_id = instance.id

    cache.delete_many(
        [
            CacheKeysService.campaign_key(campaign_id),
            CacheKeysService.campaign_total_allowed_usage_key(campaign_id),
            CacheKeysService.campaign_total_allowed_count_key(campaign_id),
            CacheKeysService.campaign_current_usage_key(campaign_id),
            CacheKeysService.campaign_current_count_key(campaign_id),
            CacheKeysService.campaign_user_max_allowed_count_key(campaign_id),
        ]
    )

    active_campaign_ids = cache.get(CacheKeysService.active_campaigns(), [])
    if str(campaign_id) in active_campaign_ids:
        active_campaign_ids.remove(str(campaign_id))
        cache.set(
            CacheKeysService.active_campaigns(),
            active_campaign_ids,
            24 * 60 * 60,
        )
