from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Request, Response

from . import crud, models, schemas
from .database import SessionLocal, engine
from .logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    logger.debug("Processing request for endpoint: %s | %s", request.method, request.url)

    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    logger.debug("Request processed: %s", request.headers.items())
    return response


# Dependency, with middleware
def get_db(request: Request):
    return request.state.db


# # Dependency, without middleware
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.error("Email already registered: %s", db_user.email)
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(db=db, user=user)
    logger.debug("User created: %s", user.__dict__)
    logger.info("User created: %s", user.email)
    return user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    user_item = crud.create_user_item(db=db, item=item, user_id=user_id)
    logger.debug("User item created: %s", user_item)
    logger.info("User item created: %s", user_item.title)
    return user_item


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# basic
def sum(val1: int, val2: int):
    return val1 + val2


@app.get("/sum")
async def foobar(val1: int, val2: int):
    return {"sum": sum(val1, val2)}
