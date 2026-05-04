from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables
load_dotenv()

# Get DB connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to Postgres
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Create DOCUMENTS table (your first real table)
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Insert test data
cur.execute(
    "INSERT INTO documents (content) VALUES (%s)",
    ("hello world",)
)

conn.commit()

# Query data
cur.execute("SELECT * FROM documents;")
rows = cur.fetchall()

for row in rows:
    print(row)

# Clean up
cur.close()
conn.close()