"""Utilities for use in API tests."""

import json
from typing import Any, Union

from django.http import JsonResponse


class JSONRequestMixin:
    """Mixin for adding a `post` method specifically for JSON."""

    def post(
        self: Any,
        path: str,
        data: Union[dict, list, str]
    ) -> JsonResponse:
        """
        Do a POST request with content_type='application/json'.

        Also decode the resulting JsonResponse and return it
        alongside status_code.
        """
        response = self.client.post(
            path, data=data, content_type='application/json'
        )
        return (
            response.status_code,
            json.loads(response.content.decode())
        )
