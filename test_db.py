from app.database import engine

try:
    with engine.connect() as conn:
        print("✅ Successfully connected to PostgreSQL!")
except Exception as e:
    print("❌ Database connection failed:", str(e))
