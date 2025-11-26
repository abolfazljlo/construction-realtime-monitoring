# Notification Service

Microservice for sending notifications via SMS and Email with multiple provider support and fallback mechanisms.

## Features

- **Multi-Provider Support**: SMS (Kavenegar, Ghasedak, Twilio) and Email (SMTP, SendGrid)
- **Fallback Mechanism**: Automatic failover to next provider if one fails
- **Multiple Consumers**: gRPC and RabbitMQ support
- **Async Processing**: Non-blocking notification delivery
- **Provider Abstraction**: Easy to add new notification providers

## Tech Stack

- **FastAPI** - Web framework for health endpoints
- **gRPC** - High-performance RPC for service-to-service communication
- **RabbitMQ** - Message queue for async notification processing
- **aio-pika** - Async RabbitMQ client
- **Multiple Providers** - SMS and Email service integrations

## Prerequisites

- Python 3.13+
- RabbitMQ (optional, if RabbitMQ consumer is enabled)
- Provider API keys (Kavenegar, SendGrid, etc.)

## Installation

1. **Navigate to the service directory**:
   ```bash
   cd backend/services/notification
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp ENV_SAMPLE.txt .env
   # Edit .env with your provider API keys
   ```

5. **Configure the service**:
   - Update `config.yml` with your provider settings
   - Enable/disable providers as needed
   - Configure consumers (gRPC, RabbitMQ)

## Configuration

The service uses `config.yml` with environment variable substitution. Key configurations:

### Consumers
- **gRPC**: Enable/disable gRPC server
- **RabbitMQ**: Enable/disable RabbitMQ consumer

### SMS Providers
- **Kavenegar**: Iranian SMS provider
- **Ghasedak**: Iranian SMS provider
- **Twilio**: International SMS provider

### Email Providers
- **SMTP**: Standard SMTP server
- **SendGrid**: Cloud email service

See `ENV_SAMPLE.txt` for all required environment variables.

## Running the Service

### Development Mode

```bash
python -m app.main
```

Or with uvicorn for health endpoint:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### Using Docker

```bash
docker build -t notification-service .
docker run -p 8000:8000 -p 50052:50052 --env-file .env notification-service
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

## gRPC API

The service exposes a gRPC server for receiving notification requests:

### SendNotification
```protobuf
rpc SendNotification(NotificationRequest) returns (Ack);
```

**Request:**
```json
{
  "type": "sms",
  "payload_json": "{\"to\": \"09123456789\", \"message\": \"Hello\"}"
}
```

## Message Types

### SMS Notification
```json
{
  "type": "sms",
  "to": "09123456789",
  "message": "Your OTP code is 123456"
}
```

### Email Notification
```json
{
  "type": "email",
  "to": "user@example.com",
  "subject": "Welcome",
  "body": "Welcome to our service!"
}
```

## Environment Variables

Required environment variables (see `.env.sample`):

### SMS Providers
- `KAVEHNEGAR_API_KEY` - Kavenegar API key
- `KAVEHNEGAR_SENDER` - Kavenegar sender number
- `GHASEDAK_API_KEY` - Ghasedak API key (optional)
- `TWILIO_ACCOUNT_SID` - Twilio account SID (optional)
- `TWILIO_AUTH_TOKEN` - Twilio auth token (optional)

### Email Providers
- `SMTP_HOST` - SMTP server host
- `SMTP_PORT` - SMTP server port
- `SMTP_USERNAME` - SMTP username
- `SMTP_PASSWORD` - SMTP password
- `SENDGRID_API_KEY` - SendGrid API key (optional)

### Service Configuration
- `SERVICE_NAME` - Service name
- `SERVICE_VERSION` - Service version
- `LOG_LEVEL` - Logging level

## Provider Configuration

### Enable/Disable Providers

Edit `config.yml` to enable or disable providers:

```yaml
providers:
  sms:
    enabled: true
    kavenegar:
      enabled: true
    ghasedak:
      enabled: false
    twilio:
      enabled: false
  
  email:
    enabled: true
    smtp:
      enabled: true
    sendgrid:
      enabled: false
```

## Development

### Project Structure
```
notification/
├── app/
│   ├── config/        # Configuration classes
│   ├── consumer/      # Message consumers (gRPC, RabbitMQ)
│   ├── dispatcher/    # Notification dispatcher and handlers
│   ├── models/        # Data models
│   ├── proto/         # gRPC protocol definitions
│   └── utils/         # Utility functions
├── config.yml         # Service configuration
├── Dockerfile         # Docker image definition
└── requirements.txt   # Python dependencies
```

### Adding a New Provider

1. Create provider class in `app/dispatcher/providers/sms/` or `app/dispatcher/providers/email/`
2. Implement `ProviderInterface`
3. Add configuration in `config.yml`
4. Register in `app/dispatcher/registry.py`

## Troubleshooting

### Provider Failures
- Check API keys in `.env`
- Verify provider service status
- Review logs for specific error messages
- Service automatically falls back to next provider

### gRPC Connection Issues
- Verify gRPC port (default: 50052) is accessible
- Check firewall settings
- Review gRPC server logs

### RabbitMQ Connection Issues
- Verify RabbitMQ is running
- Check connection settings in `config.yml`
- Test connection: `rabbitmqctl status`

## License

Part of the Construction Realtime Monitoring system.

