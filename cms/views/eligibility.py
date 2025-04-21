from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Customer
from cms.serializers import (
    CampaignEligibilitySerializer,
    CampaignResponseSerializer,
)
from utils.campaign_fetcher_util import CacheKeysService, CampaignsCacheService


class EligibleCampaignsView(APIView):
    def _is_eligible(
        self,
        campaign_data,
        customer,
        cart_value,
        payment_method,
        delivery_fee,
        location_tier,
        user_priority,
    ):
        if (
            campaign_data["rules"]["min_cart_value"]
            and cart_value < campaign_data["rules"]["min_cart_value"]
        ):
            return False

        if (
            campaign_data["rules"]["payment_methods"]
            and payment_method not in campaign_data["rules"]["payment_methods"]
        ):
            return False

        if (
            campaign_data["rules"]["location_tiers"]
            and location_tier
            and location_tier not in campaign_data["rules"]["location_tiers"]
        ):
            return False

        if (
            campaign_data["rules"]["priorities"]
            and user_priority
            and user_priority not in campaign_data["rules"]["priorities"]
        ):
            return False

        if (
            campaign_data["target_group_ids"]
            and not customer.groups.filter(
                id__in=campaign_data["target_group_ids"]
            ).exists()
        ):
            return False

        budget_used = cache.get(
            CacheKeysService.campaign_current_usage_key(campaign_data["id"])
        )
        if (
            budget_used
            and campaign_data["total_budget"]
            and budget_used >= campaign_data["total_budget"]
        ):
            return False

        current_total_count = cache.get(
            CacheKeysService.campaign_current_count_key(campaign_data["id"])
        )
        if (
            current_total_count
            and current_total_count >= campaign_data["max_uses_total"]
        ):
            return False

        customer_usage_for_day = cache.get(
            CacheKeysService.campaign_user_current_count_key(
                campaign_data["id"], customer.id
            )
        )
        if (
            customer_usage_for_day
            and customer_usage_for_day
            >= campaign_data["max_uses_per_customer"]
        ):
            return False
        return True

    def get_customer(self, id):
        return Customer.objects.get(id=id)

    @swagger_auto_schema(
        manual_parameters=[],
        query_serializer=CampaignEligibilitySerializer,
        responses={200: CampaignResponseSerializer(many=True)},
    )
    def get(self, request):
        serializer = CampaignEligibilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        customer = self.get_customer(serializer.validated_data["user_id"])

        cached_campaigns = CampaignsCacheService.get_all_campaigns()

        eligible = []
        for campaign_data in cached_campaigns:
            if self._is_eligible(
                campaign_data,
                customer=customer,
                cart_value=serializer.validated_data["cart_value"],
                payment_method=serializer.validated_data["payment_method"],
                delivery_fee=serializer.validated_data["delivery_fee"],
                location_tier=serializer.validated_data.get("location_tier"),
                user_priority=serializer.validated_data.get("user_priority"),
            ):
                eligible.append(campaign_data)

        serializer = CampaignResponseSerializer(data=eligible, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
