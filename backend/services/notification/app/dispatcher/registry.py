from typing import Dict, Type

from .handlers.email import EmailHandler
from .handlers.sms import SMSHandler
from .handlers.base import HandlerInterface

from .providers.sms.kavenegar import KavenegarProvider
# from .providers.sms.ghasedak import GhasedakProvider
# from .providers.sms.twilio import TwilioProvider    

from .providers.email.smtp import SMTPProvider
# from .providers.email.sendgrid import SendGridProvider

from ..models.notification_message.email.message import EmailNotificationMessage
from ..models.notification_message.sms.message import SMSNotificationMessage
from ..models.notification_message.union import NotificationMessage

from ..config.loader import ServiceConfig
from ..config.providers.sms.main import SMSProvidersConfig
from ..config.providers.email.main import EmailProvidersConfig

from ..utils.log import Log


# ============================================================
# Provider Factories
# ============================================================

def build_sms_providers(sms_config: SMSProvidersConfig) -> list:
    providers = []

    if not sms_config.enabled:
        Log.info("SMS notifications disabled via config.")
        return providers

    # Kavenegar
    if sms_config.kavenegar.enabled:
        try:
            providers.append(KavenegarProvider())
            Log.info("🟢 SMS Provider Enabled: Kavenegar")
        except Exception as e:
            Log.error(f"❌ Failed to init KavenegarProvider: {e}")

    # Ghasedak
    if sms_config.ghasedak.enabled:
        try:
            # providers.append(GhasedakProvider())
            Log.info("🟢 SMS Provider Enabled: Ghasedak")
        except Exception as e:
            Log.error(f"❌ Failed to init GhasedakProvider: {e}")

    # Twilio
    if sms_config.twilio.enabled:
        try:
            # providers.append(TwilioProvider())
            Log.info("🟢 SMS Provider Enabled: Twilio")
        except Exception as e:
            Log.error(f"❌ Failed to init TwilioProvider: {e}")

    return providers



def build_email_providers(email_config: EmailProvidersConfig) -> list:
    providers = []

    if not email_config.enabled:
        Log.info("Email notifications disabled via config.")
        return providers

    # SMTP
    if email_config.smtp.enabled:
        try:
            providers.append(SMTPProvider())
            Log.info("🟢 Email Provider Enabled: SMTP")
        except Exception as e:
            Log.error(f"❌ Failed to init SMTPProvider: {e}")

    # SendGrid
    if email_config.sendgrid.enabled:
        try:
            # providers.append(SendGridProvider())
            Log.info("🟢 Email Provider Enabled: SendGrid")
        except Exception as e:
            Log.error(f"❌ Failed to init SendGridProvider: {e}")

    return providers



# ============================================================
# Main Handler Registry Builder
# ============================================================

def create_handler_registry(config: ServiceConfig):
    """
    Builds a dynamic registry:
        { NotificationMessage → HandlerInstance }
    based on YAML configuration.
    """

    # -------------------------------
    # 1. Build SMS Handler
    # -------------------------------
    sms_providers = build_sms_providers(config.providers.sms)
    if sms_providers:
        sms_handler = SMSHandler(
            providers=sms_providers
        )
    else:
        sms_handler = None
        Log.info("⚠️  No SMS providers enabled")

    # -------------------------------
    # 2. Build Email Handler
    # -------------------------------
    email_providers = build_email_providers(config.providers.email)
    if email_providers:
        email_handler = EmailHandler(
            providers=email_providers
        )
    else:
        email_handler = None
        Log.info("⚠️  No Email providers enabled")

    # -------------------------------
    # 3. Build Registry
    # -------------------------------
    registry: dict[NotificationMessage, HandlerInterface] = {}

    if email_handler:
        registry[EmailNotificationMessage] = email_handler

    if sms_handler:
        registry[SMSNotificationMessage] = sms_handler

    if not registry:
        raise RuntimeError(
            "❌ No handlers available. Enable at least one provider in config.yml."
        )

    Log.success("🔧 Handler Registry created successfully")

    return registry
