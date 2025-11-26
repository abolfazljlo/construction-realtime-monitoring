# Backend Services

Microservices architecture for the Construction Realtime Monitoring system.

## Services Overview

### 1. Account Service
User management, authentication, and identity validation.

**Port**: 8001  
**Features**:
- User registration with OTP verification
- JWT-based authentication
- Identity validation via s.api.ir
- Password management

**Documentation**: [Account Service README](./services/account/README.md)

### 2. Notification Service
Multi-provider notification service for SMS and Email.

**Port**: 8000 (HTTP), 50052 (gRPC)  
**Features**:
- SMS via Kavenegar, Ghasedak, Twilio
- Email via SMTP, SendGrid
- Automatic provider fallback
- gRPC and RabbitMQ consumers

**Documentation**: [Notification Service README](./services/notification/README.md)

## Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR individual installations:
  - Python 3.13+
  - PostgreSQL 12+
  - Redis 6+
  - RabbitMQ 3.12+ (optional, for notification service)

## Quick Start with Docker Compose

The easiest way to run all services together:

1. **Clone the repository** (if not already done)

2. **Navigate to project root**:
   ```bash
   cd construction-realtime-monitoring
   ```

3. **Set up environment variables**:
   ```bash
   # Option 1: Use the script (recommended)
   ./scripts/create-env-files.sh  # Linux/Mac
   # OR
   .\scripts\create-env-files.ps1  # Windows PowerShell
   
   # Option 2: Manual copy
   cp .env.sample .env  # Root .env (if exists)
   cp backend/services/account/ENV_SAMPLE.txt backend/services/account/.env
   cp backend/services/notification/ENV_SAMPLE.txt backend/services/notification/.env
   cp frontend/ENV_SAMPLE.txt frontend/.env
   
   # Edit .env files with your actual configuration
   ```

4. **Start all services**:
   ```bash
   docker-compose up -d
   ```

5. **Check service status**:
   ```bash
   docker-compose ps
   ```

6. **View logs**:
   ```bash
   docker-compose logs -f
   ```

## Running Services Individually

### Account Service

```bash
cd backend/services/account

# Set up environment
cp .env.sample .env
# Edit .env

# Run with Docker
docker build -t account-service .
docker run -p 8001:8001 --env-file .env account-service

# OR run directly
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Notification Service

```bash
cd backend/services/notification

# Set up environment
cp .env.sample .env
# Edit .env

# Run with Docker
docker build -t notification-service .
docker run -p 8000:8000 -p 50052:50052 --env-file .env notification-service

# OR run directly
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

Create a `.env` file in the project root with all required variables. See `.env.sample` for reference.

### Required Variables

**Account Service:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection URL
- `JWT_SECRET` - JWT secret key
- `API_IR_API_KEY` - s.api.ir API key

**Notification Service:**
- `KAVEHNEGAR_API_KEY` - Kavenegar SMS API key
- `KAVEHNEGAR_SENDER` - Kavenegar sender number
- `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD` - SMTP configuration

## Service Communication

### gRPC
Notification service exposes gRPC server on port `50052` for other services to send notifications.

### HTTP REST APIs
- Account Service: `http://localhost:8001`
- Notification Service: `http://localhost:8000`

### Message Queue (Optional)
RabbitMQ can be used for async notification processing.

## Database Setup

### PostgreSQL

Create databases for each service:

```sql
-- Account service database
CREATE DATABASE account_db;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE account_db TO postgres;
```

The services will automatically create tables on first run.

## Development

### Project Structure
```
backend/
├── services/
│   ├── account/        # Account service
│   └── notification/   # Notification service
└── README.md          # This file
```

### Running in Development Mode

1. **Start dependencies** (PostgreSQL, Redis, RabbitMQ):
   ```bash
   docker-compose up -d postgres redis rabbitmq
   ```

2. **Run services individually** with hot reload:
   ```bash
   # Terminal 1 - Account Service
   cd backend/services/account
   uvicorn app.main:app --reload --port 8001

   # Terminal 2 - Notification Service
   cd backend/services/notification
   uvicorn app.main:app --reload --port 8000
   ```

## Health Checks

Check service health:

```bash
# Account Service
curl http://localhost:8001/health

# Notification Service
curl http://localhost:8000/health
```

## Troubleshooting

### Port Conflicts
- Account Service uses port `8001`
- Notification Service uses port `8000` (HTTP) and `50052` (gRPC)
- Change ports in `docker-compose.yml` or service configuration if needed

### Database Connection Issues
- Verify PostgreSQL is running: `docker-compose ps postgres`
- Check connection string in `.env`
- Ensure database exists

### Redis Connection Issues
- Verify Redis is running: `docker-compose ps redis`
- Check `REDIS_URL` in `.env`
- Test: `docker-compose exec redis redis-cli ping`

### Service Communication Issues
- Verify all services are running
- Check network connectivity in Docker
- Review service logs: `docker-compose logs <service-name>`

## Production Deployment

### Recommendations

1. **Use environment variables** for all sensitive data
2. **Set strong JWT secrets** and rotate regularly
3. **Enable connection pooling** for databases
4. **Use managed databases** (RDS, Cloud SQL, etc.)
5. **Set up monitoring** and logging
6. **Use reverse proxy** (nginx, Traefik) for routing
7. **Enable HTTPS** with SSL certificates
8. **Set resource limits** in docker-compose

### Scaling

Services can be scaled independently:

```bash
# Scale account service
docker-compose up -d --scale account=3

# Scale notification service
docker-compose up -d --scale notification=2
```

## License

Part of the Construction Realtime Monitoring system.

