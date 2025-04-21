import os

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if (
            request.path.startswith("/swagger/")
            or request.path.startswith("/redoc/")
            or request.path.startswith("/swagger.")
        ):
            return None
        api_key = self.get_api_key(request)
        if not self.validate_key(api_key):
            raise AuthenticationFailed("Invalid API Key")
        return (None, None)

    def get_api_key(self, request):
        return request.headers.get("X-API-KEY")

    def validate_key(self, api_key):
        valid_keys = os.getenv("API_KEYS", "").split(",")
        return api_key in valid_keys
