import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

print("COnnecting to :", DB_URL.replace(os.getenv("DB_PASSWORD"),"******"))

engine = create_engine(DB_URL, echo=True)

try:
    with engine.connect() as conn:
        result = conn.execute(text("Select 1"))
        print("DATABASE CONNECTED SUCCESSFULLY")
        print("Result :", result.fetchone())
except Exception as e:
    print("DATABASE CONNECTION FAILED")
    print(e)


SessionLocal = sessionmaker(bind=engine)