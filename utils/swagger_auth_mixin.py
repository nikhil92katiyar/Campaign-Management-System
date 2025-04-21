from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class APIKeySchemaMixin:
    api_key_header = "X-API-KEY"
    api_key_required = True
    api_key_description = "Your API key in the X-API-KEY header"

    @classmethod
    def get_swagger_auth_parameters(cls):
        return [
            openapi.Parameter(
                name=cls.api_key_header,
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=cls.api_key_description,
                required=cls.api_key_required,
            )
        ]

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)  # type: ignore
        http_methods = [
            "get",
            "post",
            "put",
            "patch",
            "delete",
            "head",
            "options",
        ]
        for method in http_methods:
            if hasattr(cls, method):
                view = swagger_auto_schema(
                    method=method,
                    manual_parameters=cls.get_swagger_auth_parameters(),
                    security=[{"ApiKeyAuth": []}],
                )(view)

        return view
