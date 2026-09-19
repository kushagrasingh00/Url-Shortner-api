from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_url="DATABASE_URL"
engine = create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

print(f"DB URL VALUE: {db_url}")
print(f"DB URL TYPE: {type(db_url)}")

# dependency
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

