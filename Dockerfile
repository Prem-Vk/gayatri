# ==============================================================================
# Multi-stage optimized Dockerfile for Gayatri E-Commerce (Django on Python 3.12)
# Optimized for Northflank / production container deployment
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build virtual environment and wheels
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install compiler and headers needed for native C extensions (psycopg2, rcssmin, rjsmin, pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install python dependencies into virtualenv
WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Prune unneeded files from site-packages to reduce final image size
RUN find /opt/venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -name "*.c" -delete && \
    find /opt/venv -name "*.o" -delete

# Byte-compile python modules in virtualenv for faster runtime startup
RUN python -m compileall -q /opt/venv

# ------------------------------------------------------------------------------
# Stage 2: Final minimal runtime image
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1 \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install only minimal runtime shared libraries (libpq5 for postgres, curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create a non-root system user and group for security
RUN addgroup --system --gid 10001 appgroup && \
    adduser --system --uid 10001 --ingroup appgroup --no-create-home appuser

# Copy application source code
COPY --chown=appuser:appgroup . /app

# Ensure entrypoint is executable and pre-collect static assets during build
RUN chmod +x /app/entrypoint.sh && \
    mkdir -p /app/staticfiles /app/media && \
    python manage.py collectstatic --noinput && \
    chown -R appuser:appgroup /app/staticfiles /app/media

# Switch to non-root user
USER appuser

# Expose application port (Northflank detects exposed port automatically)
EXPOSE 8000

# Container healthcheck (probes root URL)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Entrypoint runs database migrations and starts WSGI server
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command: production Gunicorn server with worker and thread tuning
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "gayatri_ecommerce.wsgi:application"]
