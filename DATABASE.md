# Database Persistence Implementation

This implementation adds persistent database storage to the Mergington High School Management System.

## Features Implemented

- ✅ SQLAlchemy ORM integration
- ✅ SQLite database (easily switchable to PostgreSQL/MySQL)
- ✅ Database models for Activities and Participants
- ✅ Automatic database initialization on startup
- ✅ Data seeding with initial activities
- ✅ Timestamps (created_at, updated_at)
- ✅ Many-to-many relationship for activity participants
- ✅ All original API endpoints maintained

## Database Schema

### Activities Table
- `id` (Primary Key)
- `name` (Unique, Indexed)
- `description`
- `schedule`
- `max_participants`
- `created_at`
- `updated_at`

### Activity Participants Table (Association Table)
- `activity_id` (Foreign Key)
- `participant_email` (Primary Key)
- `signed_up_at`

## Configuration

The database URL can be configured via environment variable:

```bash
# SQLite (default)
DATABASE_URL=sqlite:///./mergington_school.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/mergington_school

# MySQL
DATABASE_URL=mysql://user:password@localhost/mergington_school
```

## Database Initialization

The database is automatically initialized on application startup:
1. Tables are created if they don't exist
2. Initial data is seeded if the database is empty

To manually initialize the database:
```bash
python -m src.init_db
```

## Migration Support

For future migrations, consider using Alembic:
```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Benefits

1. **Data Persistence**: Data survives server restarts
2. **Scalability**: Easy to switch to PostgreSQL/MySQL for production
3. **Data Integrity**: Proper relationships and constraints
4. **Audit Trail**: Timestamps track when records are created/updated
5. **Foundation**: Ready for future features (authentication, RBAC, etc.)
