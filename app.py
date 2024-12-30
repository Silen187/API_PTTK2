from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_user

app = FastAPI()

# Mô phỏng database người dùng
users_db = {
    "admin": {"username": "admin", "password": "1234"}
}

@app.get("/")
def root():
    return {"message": "Duong Cong Thai xin chao"}

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = authenticate_user(users_db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Tạo token
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected/")
def protected_data(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This is protected data."}
