# FitMatrix Backend API

A FastAPI-based backend for the My Fit Week fitness application, built with Python, FastAPI, and PostgreSQL.

## Features

- **User Management**: Registration, authentication, and user profiles
- **Exercise Library**: Comprehensive exercise database with muscle targeting
- **Workout Management**: Create, track, and manage workouts
- **User Setup**: Guided setup process for workout preferences
- **Muscle Groups**: Muscle group management and targeting
- **Progress Tracking**: Workout completion and statistics

## Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **JWT** - Authentication tokens
- **Bcrypt** - Password hashing

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API route handlers
│   │       └── api.py         # API router configuration
│   ├── core/
│   │   ├── auth.py           # Authentication utilities
│   │   ├── config.py         # Configuration settings
│   │   └── database.py       # Database connection
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
├── scripts/                 # Utility scripts
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip or pipenv

### 2. Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a PostgreSQL database:
```sql
CREATE DATABASE myfitweek;
```

2. Copy the environment file and configure:
```bash
cp .env.example .env
```

3. Update `.env` with your database credentials:
```
DATABASE_URL=postgresql://username:password@localhost:5432/myfitweek
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Seed the database with initial data:
```bash
python scripts/seed_data.py
```

### 4. Running the Application

Start the development server:
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user

### Exercises
- `GET /api/v1/exercises/library` - Get exercise library
- `GET /api/v1/exercises/library/{id}` - Get specific exercise
- `POST /api/v1/exercises/library` - Create new exercise
- `GET /api/v1/exercises/` - Get user exercises
- `POST /api/v1/exercises/` - Create user exercise

### Workouts
- `GET /api/v1/workouts/` - Get user workouts
- `GET /api/v1/workouts/{id}` - Get specific workout
- `POST /api/v1/workouts/` - Create new workout
- `PUT /api/v1/workouts/{id}/complete` - Complete workout
- `DELETE /api/v1/workouts/{id}` - Delete workout

### Muscle Groups
- `GET /api/v1/muscle-groups/` - Get muscle groups
- `GET /api/v1/muscle-groups/{id}` - Get specific muscle group
- `POST /api/v1/muscle-groups/` - Create muscle group

### User Setup
- `GET /api/v1/user-setup/` - Get user setup
- `POST /api/v1/user-setup/` - Create user setup
- `PUT /api/v1/user-setup/` - Update user setup
- `PUT /api/v1/user-setup/complete` - Complete setup

## Database Models

### Core Models
- **User**: User accounts and authentication
- **MuscleGroup**: Muscle groups and targeting
- **LibraryExercise**: Exercise library entries
- **Exercise**: User-specific exercises
- **Workout**: Workout sessions
- **WorkoutExercise**: Exercises within workouts
- **UserSetupConfig**: User workout preferences

## Development

### Running Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

### Testing

Run tests (when implemented):
```bash
pytest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.