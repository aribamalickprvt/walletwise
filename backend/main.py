from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

import models
import schemas
import auth
from database import engine, get_db

# Initialize FastAPI App
app = FastAPI(title="WalletWise API", version="1.0")

# Crucial CORS Settings: Allows your CDN/Live Server frontend to talk to this API safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, DELETE, etc.
    allow_headers=["*"],  # Allows Authorization headers
)

# Tell SQLAlchemy to automatically build your MySQL tables if they don't exist yet
models.Base.metadata.create_all(bind=engine)

# Security config: tells FastAPI to look for an "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ==========================================
# SECURITY DEPENDENCY Authentication Guard
# ==========================================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Intercepts requests, extracts the JWT token, and returns the current logged-in User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # FIX: was HTTP_101_UNAUTHORIZED (101 = "Switching Protocols", doesn't exist on status)
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ==========================================
# USER ROUTE ENDPOINTS
# ==========================================

@app.post("/register", response_model=schemas.Token)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already taken")
    
    # Securely hash password and save to MySQL
    hashed_pwd = auth.hash_password(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Auto-login upon registration by returning a token
    access_token = auth.create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Find user
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Generate and hand out identity token
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ==========================================
# EXPENSE MANAGEMENT ENDPOINTS  
# ==========================================

@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Saves a new expense entry explicitly mapped to the authenticated user."""
    db_expense = models.Expense(**expense.model_dump(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses/", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Retrieves ONLY the expenses belonging to the currently logged-in user."""
    return db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Safely removes an expense entry if it exists and belongs to the active user."""
    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id, 
        models.Expense.user_id == current_user.id
    ).first()
    
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found or unauthorized")
        
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense successfully deleted"}