from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate
from app.schemas.token import Token
from app.models.user import User
from app.dependencies.auth import create_access_token, oauth2_scheme, get_password_hash, verify_password
from fastapi import status

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)

        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            firstName=user.firstName,
            lastName=user.lastName
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error deleting user: {str(e)}")

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    print("User model details:", User.__dict__)
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, str(db_user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/users', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def getAllUser(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.patch('/users/{user_id}', response_model=UserUpdate, status_code=status.HTTP_200_OK)
def updateUser(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    
        user_data = user.dict(exclude_unset=True)
    
        if 'password' in user_data:
            user_data['hashed_password'] = get_password_hash(user_data.pop('password'))
    
        for field, value in user_data.items():
            setattr(db_user, field, value)
    
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error deleting user: {str(e)}")


@router.delete('/users/{user_id}',response_model=UserResponse,status_code=status.HTTP_200_OK)
def deleteUser(user_id:int,db: Session = Depends(get_db)):
    try:
        find_user = db.query(User).filter(User.id == user_id).first()
        if find_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.delete(find_user)
        db.commit()
        return find_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error deleting user: {str(e)}")
    




    