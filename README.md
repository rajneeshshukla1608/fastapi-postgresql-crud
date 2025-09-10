# FastAPI CRUD Service

A FastAPI application with CRUD operations for an Item resource using PostgreSQL and Prisma ORM.

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Installation

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Install Prisma and generate client:
```bash
npm install
npx prisma generate
```

3. Setup database:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/prisma
npx prisma migrate dev --name init
```

4. Seed with sample data:
```bash
python -m app.seed --count 15 --truncate
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for API documentation.

### Docker

```bash
docker-compose up --build
```

## API Endpoints

- `POST /items/` - Create item
- `GET /items/` - List items (with pagination and title filter)
- `GET /items/{id}` - Get single item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Sample Data

The database comes pre-seeded with 15 realistic items including:
- Project Alpha: Main project for Q1 development
- Code Review: Review pull requests for backend changes
- Database Migration: Update schema for new user features
- API Documentation: Update Swagger docs for new endpoints
- Bug Fix #123: Fix authentication issue in login flow
- Performance Testing: Load test the new payment system
- Security Audit: Review security vulnerabilities
- And more...

## Testing

```bash
pytest
```

## Database Schema

```sql
CREATE TABLE "Item" (
    "id" SERIAL PRIMARY KEY,
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Seeding

```bash
python -m app.seed --count 50 --truncate
```
