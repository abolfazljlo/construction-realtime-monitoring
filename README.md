# Construction Realtime Monitoring

A real-time construction project monitoring system that lets managers create projects, assign team roles, and track on-site status instantly. Built with a microservices architecture using FastAPI for the backend and React for the frontend.

## 🏗️ Architecture

This project follows a **microservices architecture** with the following components:

### Backend Services

- **Account Service** (`backend/services/account`)
  - User management and authentication
  - Identity validation via s.api.ir
  - JWT-based authentication
  - OTP verification for signup

- **Notification Service** (`backend/services/notification`)
  - Multi-provider SMS and Email notifications
  - Support for Kavenegar, Ghasedak, Twilio (SMS)
  - Support for SMTP, SendGrid (Email)
  - Automatic provider fallback
  - gRPC and RabbitMQ consumers

### Frontend

- **React Frontend** (`frontend`)
  - React 18 with TypeScript
  - Vite for fast development
  - Tailwind CSS for styling
  - Persian (Farsi) language support with RTL layout
  - TanStack Query for API state management
  - Zustand for global state

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR individual installations:
  - Python 3.13+
  - Node.js 20+
  - PostgreSQL 12+
  - Redis 6+
  - RabbitMQ 3.12+ (optional)

### Using Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abolfazlj00/construction-realtime-monitoring.git
   cd construction-realtime-monitoring
   ```

2. **Set up environment variables**:
   ```bash
   # Copy the sample file
   cp .env.sample .env
   
   # Edit .env with your actual values
   # Required: Database credentials, Redis URL, JWT secret, API keys
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Check service status**:
   ```bash
   docker-compose ps
   ```

5. **View logs**:
   ```bash
   docker-compose logs -f
   ```

6. **Access the application**:
   - Frontend: http://localhost:3000
   - Account Service API: http://localhost:8001
   - Notification Service API: http://localhost:8000
   - RabbitMQ Management: http://localhost:15672

### Manual Setup

#### Backend Services

See [backend/README.md](./backend/README.md) for detailed instructions on running backend services individually.

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
construction-realtime-monitoring/
├── backend/
│   ├── services/
│   │   ├── account/          # Account service
│   │   │   ├── app/          # Application code
│   │   │   ├── config.yml    # Service configuration
│   │   │   ├── Dockerfile   # Docker image
│   │   │   └── README.md     # Service documentation
│   │   └── notification/     # Notification service
│   │       ├── app/          # Application code
│   │       ├── config.yml    # Service configuration
│   │       ├── Dockerfile   # Docker image
│   │       └── README.md     # Service documentation
│   └── README.md             # Backend documentation
├── frontend/                  # React frontend
│   ├── src/                  # Source code
│   ├── Dockerfile            # Docker image
│   └── README.md            # Frontend documentation
├── docker-compose.yml        # Docker Compose configuration
├── .env.sample              # Environment variables template
└── scripts/                  # Utility scripts
    ├── create-env-files.sh  # Generate .env files (Linux/Mac)
    └── create-env-files.ps1 # Generate .env files (Windows)
```

## 🔧 Configuration

### Environment Variables

All services use environment variables for configuration. See `.env.sample` for a complete list of required variables.

**Key Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection URL
- `JWT_SECRET` - Secret key for JWT tokens
- `API_IR_API_KEY` - s.api.ir API key for identity validation
- `KAVEHNEGAR_API_KEY` - Kavenegar SMS API key
- `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD` - SMTP configuration

### Service Configuration

Each service has its own `config.yml` file that supports environment variable substitution using `${VAR}` or `${VAR:-default}` syntax.

## 📚 Documentation

- [Backend Services README](./backend/README.md) - How to run backend services
- [Account Service README](./backend/services/account/README.md) - Account service details
- [Notification Service README](./backend/services/notification/README.md) - Notification service details

## 🛠️ Development

### Running Services Individually

#### Account Service
```bash
cd backend/services/account
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

#### Notification Service
```bash
cd backend/services/notification
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Database Setup

The services will automatically create tables on first run. For manual setup:

```sql
CREATE DATABASE account_db;
GRANT ALL PRIVILEGES ON DATABASE account_db TO postgres;
```

## 🧪 Testing

### Health Checks

```bash
# Account Service
curl http://localhost:8001/health

# Notification Service
curl http://localhost:8000/health
```

## 🔐 Security

- All sensitive data should be stored in `.env` files (never commit `.env`)
- Use strong JWT secrets in production
- Rotate API keys regularly
- Enable HTTPS in production
- Use managed databases for production

## 📦 Deployment

### Production Recommendations

1. Use environment variables for all configuration
2. Set strong JWT secrets and rotate regularly
3. Enable connection pooling for databases
4. Use managed databases (RDS, Cloud SQL, etc.)
5. Set up monitoring and logging
6. Use reverse proxy (nginx, Traefik) for routing
7. Enable HTTPS with SSL certificates
8. Set resource limits in docker-compose

### Scaling

Services can be scaled independently:

```bash
# Scale account service
docker-compose up -d --scale account=3

# Scale notification service
docker-compose up -d --scale notification=2
```

## 🌐 API Endpoints

### Account Service (Port 8001)

- `GET /health` - Health check
- `POST /api/v1/signup` - Request signup OTP
- `POST /api/v1/signup/verify` - Verify OTP and create account
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/password/change` - Change password

### Notification Service (Port 8000)

- `GET /health` - Health check
- gRPC endpoint on port `50052` for service-to-service communication

## 🐛 Troubleshooting

### Port Conflicts
- Account Service: `8001`
- Notification Service: `8000` (HTTP), `50052` (gRPC)
- Frontend: `3000`
- PostgreSQL: `5432`
- Redis: `6379`
- RabbitMQ: `5672`, `15672` (management)

### Common Issues

**Database Connection Issues:**
- Verify PostgreSQL is running: `docker-compose ps postgres`
- Check `DATABASE_URL` in `.env`
- Ensure database exists

**Redis Connection Issues:**
- Verify Redis is running: `docker-compose ps redis`
- Check `REDIS_URL` in `.env`
- Test: `docker-compose exec redis redis-cli ping`

**Service Communication Issues:**
- Verify all services are running
- Check network connectivity in Docker
- Review service logs: `docker-compose logs <service-name>`

## 📝 License

This project is part of the Construction Realtime Monitoring system.

## 🤝 Contributing

1. Create a feature branch from `master`
2. Make your changes
3. Commit and push to your branch
4. Create a pull request

## 📞 Support

For issues and questions, please open an issue on GitHub.
