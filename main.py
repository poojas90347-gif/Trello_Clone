from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import database, models, schemas


app= FastAPI(title="Trello_clone")

models.Base.metadata.create_all(bind=database.engine)

# Database session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def create(user: schemas.UserCreate, db: Session=Depends(get_db)):
    new_user = models.User(username=user.username, email= user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"id":new_user.id, "username": new_user.username, "email": new_user.email}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm =Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username==  form_data.username).first()
    if not user  or user.password!= form_data.password:
        return{"error" : "invalid username and password"}
    return{
            "message": "login successful",
            "user_id" : user.id,
            "username" : user.username,
            "email": user.email
    }
