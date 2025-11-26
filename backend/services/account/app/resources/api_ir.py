import httpx
from .base import ResourceInterface
from ..config.api_ir import ApiIrConfig
from ..utils.log import Log

# -------------------------------------------------------------
# API.IR Resource
# -------------------------------------------------------------
class ApiIrResource(ResourceInterface[ApiIrConfig]):

    def __init__(self, settings):
        super().__init__(settings)
        self.client = None

    async def initialize(self):
        # NOTE: Authentication header format may need adjustment based on s.api.ir requirements
        # Common alternatives: "Authorization": f"Bearer {api_key}" or "Authorization": api_key
        self.client = httpx.AsyncClient(
            base_url=self.settings.base_url,
            headers={
                "X-API-Key": self.settings.api_key,
                "Content-Type": "application/json",
            },
            timeout=self.settings.timeout_seconds,
        )
        Log.info("[ApiIrResource] API client initialized successfully.")

    async def close(self):
        if self.client:
            await self.client.aclose()
            Log.info("[ApiIrResource] API client closed successfully.")

    async def get(self, endpoint: str, params: dict = None):
        """Make a GET request to the API"""
        try:
            response = await self.client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            Log.error(f"[ApiIrResource] API error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            Log.error(f"[ApiIrResource] Request error: {e}")
            raise

    async def post(self, endpoint: str, json: dict = None):
        """Make a POST request to the API"""
        try:
            response = await self.client.post(endpoint, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            Log.error(f"[ApiIrResource] API error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            Log.error(f"[ApiIrResource] Request error: {e}")
            raise

