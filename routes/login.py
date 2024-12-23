from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from services.auth import create_access_token
from database import get_db
from models import User
# from schemas import GoogleSignInRequest, ResponseModel
from uuid import uuid4

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signin")
def send_otp(mobile_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile_number == mobile_number).first()
    
    if not user:
        user = User(mobile_number=mobile_number, otp=None, is_verified=False)
        db.add(user)
        db.commit()

    otp = "1234"  
    user.otp = otp
    db.commit()
    print(f"OTP for {mobile_number}: {otp}") 

    return {"message": "OTP sent successfully"}

@router.post("/verify_otp")
def verify_otp(mobile_number: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.mobile_number == mobile_number).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.otp != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")


    user.is_verified = True
    user.otp = None  
    db.commit()

    access_token = create_access_token(data={"sub": user.user_id})

    return {"message": "Login successful", "access_token": access_token}


# Google Sign-In endpoint
# @router.post("/google_signin", response_model=ResponseModel)
# async def google_signin(request: GoogleSignInRequest, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.device_id == request.device_id).first()
    
#     if existing_user:
#         access_token = create_access_token(data={"sub": existing_user.user_id})
#         return {"message": "Login successful", "data": {"access_token": access_token, "user_id": existing_user.user_id}}
    
#     user_id = str(uuid4())
#     new_user = User(
#         user_id=user_id,
#         device_id=request.device_id,
#         name=request.name,
#         email=request.email,
       
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     access_token = create_access_token(data={"sub": new_user.user_id})
    
#     return {"message": "User registered and login successful", "data": {"access_token": access_token, "user_id": new_user.user_id}}

