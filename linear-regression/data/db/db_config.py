import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URl = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

print("Connecting to :", DB_URl.replace(os.getenv("DB_PASSWORD"), "******"))

engine = create_engine(DB_URl, echo=True)

try:
    with engine.connect() as connection:
        result = connection.execute(text("Select 1"))
        print("DATABASE CONNECTED SUCCESFULLY")
        print("Result:", result.fetchone())
except Exception as e:
    print("DATABASE CONNECTION FAILED")
    print(e)

SessionLocal = sessionmaker(bind=engine)
