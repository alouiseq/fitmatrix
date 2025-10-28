#!/bin/bash

# My Fit Week Backend Setup Script

echo "🏋️ Setting up My Fit Week Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install PostgreSQL."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your database credentials before continuing."
    echo "   Database URL format: postgresql://username:password@localhost:5432/myfitweek"
    read -p "Press Enter after updating .env file..."
fi

# Initialize Alembic
echo "🗄️ Setting up database migrations..."
alembic init alembic

# Create initial migration
echo "📊 Creating initial migration..."
alembic revision --autogenerate -m "Initial migration"

# Run migrations
echo "🚀 Running database migrations..."
alembic upgrade head

# Seed database
echo "🌱 Seeding database with initial data..."
python scripts/seed_data.py

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the server, run:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "📚 API documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "🔧 To use Docker instead:"
echo "   docker-compose up --build"