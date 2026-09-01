import sqlite3
import os

db_path = "skillbridge.db"

if not os.path.exists(db_path):
    print("❌ skillbridge.db not found. Creating fresh database...")
    from database import engine, Base
    import models
    Base.metadata.create_all(bind=engine)
    print("✅ Created new skillbridge.db successfully.")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall() if not t[0].startswith('sqlite_')]

print("📊 Database Status:")
for t in sorted(tables):
    cursor.execute(f"SELECT COUNT(*) FROM {t};")
    count = cursor.fetchone()[0]
    print(f"  • {t:<22} : {count} records")

conn.close()
print("\n✅ Database is clean, connected, and ready for real data storage.")
