from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_url="DATABASE_URL"
engine = create_engine(db_url)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

# dependency
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

