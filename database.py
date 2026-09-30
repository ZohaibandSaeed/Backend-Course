import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# Yahan apni Neon DB ki connection string set karein.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://user:password@ep-your-neon-endpoint.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

# SQLModel engine banayen
engine = create_engine(DATABASE_URL)

# FastAPI dependency database connection get karne ke liye
def get_db():
    with Session(engine) as session:
        yield session
