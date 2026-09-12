#!/bin/sh
set -e

echo "==> Starting Gayatri E-Commerce service..."

# Verify that DATABASE_URL is set in the container environment
if [ -z "$DATABASE_URL" ] && [ -z "$POSTGRES_URI" ]; then
    echo ""
    echo "========================================================================"
    echo "==> CRITICAL ERROR: DATABASE_URL is not set in Northflank!"
    echo "==>"
    echo "==> Your container is trying to fall back to SQLite, but production"
    echo "==> requires your external Neon PostgreSQL connection string."
    echo "==>"
    echo "==> HOW TO FIX:"
    echo "==> 1. Go to Northflank Dashboard -> Services -> gayatri-web"
    echo "==> 2. Click on 'Environment Variables'"
    echo "==> 3. Add key: DATABASE_URL"
    echo "==> 4. Value: postgresql://neondb_owner:YOUR_PASSWORD@ep-autumn-night-axw2pw48.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"
    echo "==> 5. Click Save & Restart"
    echo "========================================================================"
    echo ""
    exit 1
fi

# Verify database reachability using Django database engine (handles Neon SSL, connection pooling, etc.)
python - << 'EOF'
import os, sys, time

try:
    import django
    from django.db import connections
    from django.db.utils import OperationalError

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gayatri_ecommerce.settings')
    django.setup()

    print("==> Checking database connection to Neon PostgreSQL...")
    for i in range(1, 31):
        try:
            connections['default'].ensure_connection()
            print(f"==> Database connection established (attempt {i}).")
            break
        except OperationalError as err:
            print(f"==> Waiting for database ({i}/30)... ({err})")
            time.sleep(2)
        except Exception as err:
            print(f"==> Unexpected database check error: {err}")
            break
except Exception as e:
    print(f"==> Database pre-check skipped: {e}")
EOF

# Run database migrations
echo "==> Applying database migrations..."
python manage.py migrate --noinput

echo "==> Starting application server..."
exec "$@"
