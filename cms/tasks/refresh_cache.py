from celery import shared_task

from utils import CampaignsCacheService


@shared_task
def refresh_all_campaign_cache():
    return CampaignsCacheService.refresh_cache()
