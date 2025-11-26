# Account Service

Microservice for user account management, authentication, and identity validation.

## Features

- **User Registration**: Signup with OTP verification via SMS
- **Identity Validation**: Integration with s.api.ir for national code and mobile verification
- **Authentication**: JWT-based authentication with access and refresh tokens
- **Password Management**: Secure password hashing and management
- **User Management**: CRUD operations for user accounts

## Tech Stack

- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **JWT** - Token-based authentication
- **s.api.ir** - Identity validation service

## Prerequisites

- Python 3.13+
- PostgreSQL 12+
- Redis 6+
- s.api.ir API key

## Installation

1. **Clone the repository** (if not already done)

2. **Navigate to the service directory**:
   ```bash
   cd backend/services/account
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp ENV_SAMPLE.txt .env
   # Edit .env with your configuration
   ```

6. **Configure the service**:
   - Copy `.env.sample` to `.env`
   - Update `config.yml` or use environment variables
   - Ensure PostgreSQL and Redis are running

## Configuration

The service uses `config.yml` with environment variable substitution. Key configurations:

- **Database**: PostgreSQL connection string
- **Redis**: Redis connection URL
- **JWT**: Secret key and token expiration settings
- **API.IR**: s.api.ir service configuration

See `ENV_SAMPLE.txt` for all required environment variables.

## Running the Service

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

### Using Docker

```bash
docker build -t account-service .
docker run -p 8001:8001 --env-file .env account-service
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Signup
- `POST /api/v1/signup` - Request signup OTP
  - Body: `{ mobile, password, national_code, birthday }`
  - Returns: `{ key }` (OTP verification key)
  
- `POST /api/v1/signup/verify` - Verify OTP and create account
  - Body: `{ key, code }`
  - Returns: `{ user, access_token, refresh_token }`

### Authentication
- `POST /api/v1/auth/login` - User login
  - Body: `{ national_code, password }`
  - Returns: `{ user, access_token, refresh_token }`

- `POST /api/v1/auth/refresh` - Refresh access token
  - Body: `{ refresh_token }`
  - Returns: `{ access_token }`

- `GET /api/v1/auth/me` - Get current user
  - Headers: `Authorization: Bearer <access_token>`
  - Returns: `{ user }`

### Password
- `POST /api/v1/password/change` - Change password
  - Headers: `Authorization: Bearer <access_token>`
  - Body: `{ old_password, new_password }`

## Environment Variables

Required environment variables (see `.env.sample`):

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection URL
- `JWT_SECRET` - Secret key for JWT tokens
- `API_IR_API_KEY` - s.api.ir API key

## Database Schema

### Users Table
- `id` - Primary key
- `mobile` - Unique mobile number (normalized)
- `national_code` - Unique 10-digit Iranian national code
- `birthday_date` - Date of birth
- `first_name` - First name
- `last_name` - Last name
- `password_hash` - Bcrypt hashed password
- `is_active` - Account status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Identity Validation

The service integrates with s.api.ir for:
- National code and birthday validation
- Mobile number ownership verification
- Personal information retrieval (name, gender)

## Development

### Project Structure
```
account/
├── app/
│   ├── api/           # API routes
│   ├── config/        # Configuration classes
│   ├── crud/          # Database operations
│   ├── models/        # Pydantic and SQLAlchemy models
│   ├── resources/     # External resource managers
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── config.yml         # Service configuration
├── Dockerfile         # Docker image definition
└── requirements.txt  # Python dependencies
```

### Running Tests
```bash
# Add tests when implemented
pytest
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists

### Redis Connection Issues
- Verify Redis is running
- Check `REDIS_URL` in `.env`
- Test connection: `redis-cli ping`

### Identity Validation Fails
- Verify `API_IR_API_KEY` is set correctly
- Check s.api.ir service status
- Review API logs for error details

## License

Part of the Construction Realtime Monitoring system.

