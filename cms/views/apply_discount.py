from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
import redis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.serializers.apply_discount import DiscountRequestSerializer
from cms.tasks.add_campaign_usage import create_campaign_usage_async
from utils.campaign_fetcher_util import CacheKeysService

redis_client = cache.client.get_client(write=True)


def attempt_apply_discount(
    campaign_id, customer_id, discount_amount, max_retries=3
):
    user_count_key = CacheKeysService.campaign_user_current_count_key(
        campaign_id, customer_id
    )
    user_max_key = CacheKeysService.campaign_user_max_allowed_count_key(
        campaign_id
    )
    total_usage_key = CacheKeysService.campaign_total_allowed_usage_key(
        campaign_id
    )
    total_count_key = CacheKeysService.campaign_total_allowed_count_key(
        campaign_id
    )
    current_usage_key = CacheKeysService.campaign_current_usage_key(
        campaign_id
    )
    current_count_key = CacheKeysService.campaign_current_count_key(
        campaign_id
    )

    total_allowed_usage = float(cache.get(total_usage_key) or 0)
    total_allowed_count = int(cache.get(total_count_key) or 0)
    max_user_count = int(cache.get(user_max_key) or 0)

    for attempt in range(1, max_retries + 1):
        try:
            with redis_client.pipeline() as pipe:
                pipe.watch(
                    user_count_key, current_usage_key, current_count_key
                )
                current_usage = float(redis_client.get(current_usage_key) or 0)
                current_total_count = int(
                    redis_client.get(current_count_key) or 0
                )
                user_count = int(redis_client.get(user_count_key) or 0)

                if max_user_count and user_count + 1 > max_user_count:
                    return False, "User limit exceeded"

                if (
                    total_allowed_usage
                    and current_usage + discount_amount > total_allowed_usage
                ):
                    return False, "Budget limit exceeded"

                if (
                    total_allowed_count
                    and current_total_count + 1 > total_allowed_count
                ):
                    return False, "Max count exceeded"

                pipe.multi()
                pipe.incr(user_count_key)
                pipe.incr(current_count_key)
                pipe.incrbyfloat(current_usage_key, discount_amount)
                pipe.execute()
                return True, "Discount applied"

        except redis.WatchError as e:
            if attempt == max_retries:
                return False, f"Error after {max_retries} attempts: {str(e)}"


class ApplyDiscountView(APIView):
    @swagger_auto_schema(
        request_body=DiscountRequestSerializer,
        responses={
            202: "Accepted: Discount applied successfully.",
            200: "Duplicate: Discount already applied with this key.",
            400: "Rejected: Validation failed or campaign limits exceeded.",
        },
    )
    def post(self, request):
        serializer = DiscountRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        customer_id = data["customer_id"]
        campaign_id = data["campaign_id"]
        discount = data["discount"]
        idempotent_key = data["idempotent_key"]
        dup_key = CacheKeysService.idempotent_discount_key(
            customer_id, idempotent_key
        )

        if redis_client.exists(dup_key):
            return Response(
                {"status": "Rejected", "reason": "Duplicate idempotent key"},
                status=status.HTTP_200_OK,
            )

        redis_client.set(dup_key, "1", ex=600)
        success, message = attempt_apply_discount(
            campaign_id=campaign_id,
            customer_id=customer_id,
            discount_amount=discount,
        )

        if success:
            # below is to be used with celery, some issue in redis so getting
            # connection refused, hence removing delay and doing it in async,
            # Future Enhancements - kafka can be used and bulk requests can be
            # processed instead of processing single every time.

            # create_campaign_usage_async.delay(
            #     customer_id, campaign_id, discount, idempotent_key
            # )
            create_campaign_usage_async(
                customer_id, campaign_id, discount, idempotent_key
            )

            return Response(
                {"status": "Accepted", "message": message},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"status": "Rejected", "reason": message},
                status=status.HTTP_400_BAD_REQUEST,
            )
