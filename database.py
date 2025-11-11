from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqllite:///./tst.db")
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False })

# SessionLocal = sssionmakr(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()