#!/bin/bash

# Reset Database Script
# This script deletes the existing database, recreates tables, and seeds initial data

cd "$(dirname "$0")"

echo "🗑️  Deleting existing database..."
rm -f myfitweek.db

echo "📊 Creating new database tables..."
source venv/bin/activate
python -c "from app.core.database import Base, engine; Base.metadata.create_all(engine)"

echo "🌱 Seeding initial data..."
python scripts/seed_data.py

echo "✅ Database reset complete!"
echo ""
echo "📊 Database is now fresh with all initial exercises and muscle groups."
