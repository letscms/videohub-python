import asyncio
from typing import Optional

import httpx

from .constants import API_BASE, SDK_NAME, SDK_VERSION
from .exceptions import APIRequestError
from .utils.validators import RequestValidator


class HTTPClient:

    def __init__(self, config):
        self.config = config
        self.validator = RequestValidator(config)

        # lazy client
        self._client: Optional[httpx.AsyncClient] = None


    def _get_client(self):

        if self._client is None:

            limits = httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            )

            self._client = httpx.AsyncClient(
                base_url=API_BASE,
                timeout=self.config.timeout,
                limits=limits
            )

        return self._client

    

    def _build_headers(self, auth_required: bool):

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"{SDK_NAME}/{SDK_VERSION}",
            "X-SDK-Version": SDK_VERSION,
        }

        if auth_required:
            headers.update(self.validator.build_headers())

        return headers

    

    async def _request(self, method: str, endpoint: str, **kwargs):

        retries = 3
        response = None

        client = self._get_client()

        for attempt in range(retries):
            try:

                response = await client.request(
                    method,
                    endpoint,
                    **kwargs
                )

                if response.status_code < 500:
                    break

            except httpx.RequestError as e:

                if attempt == retries - 1:
                    raise APIRequestError(f"Network error: {str(e)}")

                await asyncio.sleep(2 ** attempt * 0.2)

        if response is None:
            raise APIRequestError("No response from server")

        if response.status_code >= 400:
            try:
                error = response.json()
                message = error.get("error") or error.get("message") or str(error)
                raise APIRequestError(message)
            except Exception:
                raise APIRequestError(response.text)

        try:
            return response.json()
        except Exception:
            return response.text

    

    async def post(self, endpoint: str, payload: dict, auth_required: bool = True):

        headers = self._build_headers(auth_required)

        if getattr(self.config, "debug", False):
            print(f"[VideoHub SDK] POST {endpoint}")
            print("Payload:", payload)

        return await self._request(
            "POST",
            endpoint,
            json=payload,
            headers=headers
        )

    async def get(self, endpoint: str, params: Optional[dict] = None, auth_required: bool = True):

        headers = self._build_headers(auth_required)

        if getattr(self.config, "debug", False):
            print(f"[VideoHub SDK] GET {endpoint}")
            print("Params:", params)

        return await self._request(
            "GET",
            endpoint,
            params=params,
            headers=headers
        )

    

    async def close(self):

        if self._client:
            await self._client.aclose()
            self._client = None