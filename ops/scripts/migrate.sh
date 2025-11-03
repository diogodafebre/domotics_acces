#!/bin/bash
# Database migration script

set -e

echo "🔄 Running database migrations..."

# Check if alembic is available
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic not found. Please install it first."
    exit 1
fi

# Run migrations
alembic upgrade head

echo "✅ Migrations completed successfully!"
