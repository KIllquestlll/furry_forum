# Connection main library
from datetime import datetime,timedelta
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext

# Import package
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Checked password with hash_password
def verify_password(plain_password:str,hashed_password:str) -> str:
    return pwd_context.verify(plain_password,hashed_password)

# Change password in hash_password
def get_password_hash(password: str) -> str:
    if hasattr(password, "get_secret_value"):
        password = password.get_secret_value()
    
    return pwd_context.hash(str(password))


# Function for work with token
# Generate JWT token
def create_access_token(data:dict,
                        expire_delta:Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM,
                             )

    return encoded_jwt

# Checked token 'n return data (payload)
def decode_access_token(token:str) -> Optional[dict]:
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
