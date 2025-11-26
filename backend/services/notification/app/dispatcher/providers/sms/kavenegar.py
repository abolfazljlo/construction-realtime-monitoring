import os
import httpx

from ..base import ProviderInterface
from ....models.notification_message.sms.message import SMSNotificationMessage
from ....utils.log import Log


class KavenegarProvider(ProviderInterface[SMSNotificationMessage]):
    """
    Async Kavenegar SMS provider.

    Environment Variables:
        KAVEHNEGAR_API_KEY   = required
        KAVEHNEGAR_SENDER    = required
        KAVEHNEGAR_TIMEOUT   = optional (default: 10)
    """

    BASE_URL = "https://api.kavenegar.com/v1/{api_key}/sms/send.json"

    def __init__(self):
        self.api_key = os.getenv("KAVEHNEGAR_API_KEY")
        self.sender = os.getenv("KAVEHNEGAR_SENDER")
        self.timeout = int(os.getenv("KAVEHNEGAR_TIMEOUT", "10"))

        if not self.api_key:
            raise RuntimeError("KAVEHNEGAR_API_KEY is not configured")
        if not self.sender:
            raise RuntimeError("KAVEHNEGAR_SENDER is not configured")

        self.url = self.BASE_URL.format(api_key=self.api_key)

    async def send(self, message: SMSNotificationMessage) -> None:
        phone = message.data.phone
        body = message.data.message

        payload = {
            "receptor": phone,
            "sender": self.sender,
            "message": body,
        }

        Log.info(f"[KavenegarProvider] Sending SMS → {phone}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.url, data=payload)

            if response.status_code != 200:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            resp = response.json()

            # According to Kavenegar docs:
            # resp["return"]["status"] == 200 → success
            status = resp.get("return", {}).get("status")
            if status != 200:
                raise RuntimeError(f"Kavenegar API error: {resp}")

            Log.success(f"[KavenegarProvider] SMS sent → {phone}")

        except Exception as e:
            Log.error(f"[KavenegarProvider] Failed to send SMS to {phone}: {e}")
            raise
