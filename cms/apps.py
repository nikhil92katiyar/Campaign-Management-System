from django.apps import AppConfig


class CmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cms"

    def ready(self):
        self.refresh_cache_on_start()

    def refresh_cache_on_start(self):
        from utils.campaign_fetcher_util import CampaignsCacheService

        campaign_ids = CampaignsCacheService.refresh_cache()
        if campaign_ids:
            print(f"Cache refreshed with {len(campaign_ids)} campaigns.")
        else:
            print("No active campaigns found to refresh cache.")
