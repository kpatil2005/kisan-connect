# How to Keep Your Database Synced Between Local and Production

## Problem
Your local SQLite database and Render's PostgreSQL database are separate. Products added locally don't appear on the hosted site.

## Solution: Connect to Render's Database Locally

### Step 1: Get Database URL from Render
1. Go to your Render Dashboard
2. Click on your PostgreSQL database (not the web service)
3. Copy the "External Database URL" (starts with `postgres://`)
4. It looks like: `postgres://user:password@host/database`

### Step 2: Update Local Settings
Create a `.env` file in your project root with:

```
DATABASE_URL=postgres://your-database-url-from-render
```

### Step 3: Install PostgreSQL Adapter
```bash
pip install psycopg2-binary
```

### Step 4: Use Same Database Locally
When running locally, use:
```bash
python manage.py runserver
```

Now your local and production will use the SAME database!

## Alternative: Export/Import Data

If you want to keep SQLite locally but sync data:

### Export from Local
```bash
python manage.py dumpdata app.Product --indent 2 > products.json
```

### Import to Production (via Render Shell)
1. Upload `products.json` to your repo
2. In Render Shell, run:
```bash
python manage.py loaddata products.json
```

## Best Practice
Use the same database type (PostgreSQL) for both local and production to avoid issues.
