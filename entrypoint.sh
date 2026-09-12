#!/bin/sh
set -e

echo "==> Starting Gayatri E-Commerce service..."

# Verify database reachability using Django database engine (handles Neon SSL, connection pooling, etc.)
python - << 'EOF'
import os, sys, time

try:
    import django
    from django.db import connections
    from django.db.utils import OperationalError

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gayatri_ecommerce.settings')
    django.setup()

    print("==> Checking database connection...")
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
