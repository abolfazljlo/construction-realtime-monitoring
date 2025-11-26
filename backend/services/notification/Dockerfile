# ============================================================
# 1. Base image
# ============================================================
FROM python:3.13-slim AS base

# Avoid Python writing .pyc files, enable buffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ============================================================
# 2. Install system dependencies
# ============================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# ============================================================
# 3. Set working directory
# ============================================================
WORKDIR /app


# ============================================================
# 4. Install Python dependencies
# ============================================================
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ============================================================
# 5. Copy application code
# ============================================================
COPY . .


# ============================================================
# 6. Runtime environment
# ============================================================
ENV APP_ENV=production


# ============================================================
# 7. Expose default FastAPI port (optional)
# ============================================================
EXPOSE 8000


# ============================================================
# 8. Entrypoint
#    - If your service is *only* consumers: use python main
#    - If you expose FastAPI health API: use uvicorn
# ============================================================

# For FastAPI health endpoint + background consumers:
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
