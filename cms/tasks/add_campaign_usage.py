from celery import shared_task

from cms.models import CampaignUsage


@shared_task
def create_campaign_usage_async(
    customer_id, campaign_id, discount, idempotent_key
):
    campaign_usage = CampaignUsage.objects.create(
        idempotent_key=idempotent_key,
        customer_id=customer_id,
        campaign_id=campaign_id,
        discount_amount=discount,
    )
    return campaign_usage.idempotent_key
