# Fake Profile Generator API

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from faker import Faker
import random
import redis
import pymysql
import secrets
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize FastAPI app
app = FastAPI()

# Faker instance for generating fake data
fake = Faker()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate Limiter: 5 requests per minute per IP
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Redis Cache (for performance)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# MySQL Connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="api_service",
    cursorclass=pymysql.cursors.DictCursor
)


# 🔹 Hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 🔹 Verify password function
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🔹 Generate a unique API key
def generate_api_key() -> str:
    return secrets.token_hex(32)


# 🔹 Validate API Key from database
def validate_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key missing")
    
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM api_keys WHERE api_key = %s AND active = TRUE", (api_key,))
        key_data = cursor.fetchone()
    
    if not key_data:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return key_data["user_id"]


# 🔹 Register User
@app.post("/register")
def register_user(username: str, password: str):
    """Register a new user"""
    hashed_password = hash_password(password)
    
    with db.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            db.commit()
            return {"message": "User registered successfully"}
        except pymysql.err.IntegrityError:
            raise HTTPException(status_code=400, detail="Username already exists")


# 🔹 Generate New API Key for User
@app.post("/generate-api-key")
def create_api_key(username: str, password: str):
    """Generate an API key after verifying credentials"""
    with db.cursor() as cursor:
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    new_api_key = generate_api_key()
    
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO api_keys (user_id, api_key) VALUES (%s, %s)", (user["id"], new_api_key))
        db.commit()

    return {"api_key": new_api_key}


# 🔹 Get List of API Keys for User
@app.get("/list-api-keys", dependencies=[Depends(validate_api_key)])
def list_api_keys(user_id: int = Depends(validate_api_key)):
    """Retrieve all active API keys for the authenticated user"""
    with db.cursor() as cursor:
        cursor.execute("SELECT api_key, created_at FROM api_keys WHERE user_id = %s AND active = TRUE", (user_id,))
        keys = cursor.fetchall()
    
    return {"api_keys": keys}


# 🔹 Revoke API Key
@app.delete("/revoke-api-key", dependencies=[Depends(validate_api_key)])
def revoke_api_key(api_key: str, user_id: int = Depends(validate_api_key)):
    """Revoke an API key"""
    with db.cursor() as cursor:
        cursor.execute("UPDATE api_keys SET active = FALSE WHERE api_key = %s AND user_id = %s", (api_key, user_id))
        db.commit()
    
    return {"message": "API key revoked successfully"}


# 🔹 Generate Fake Profile
@app.get("/generate", dependencies=[Depends(validate_api_key)])
@limiter.limit("5/minute")
async def generate_fake_profile(
    request: Request,
    age: int = Query(None),
    gender: str = Query(None),
    country: str = Query(None)
):
    """Generate a single fake profile"""
    cache_key = f"profile:{age}:{gender}:{country}"
    
    cached_profile = redis_client.get(cache_key)
    if cached_profile:
        return eval(cached_profile)

    profile = {
        "name": fake.name_male() if gender == "male" else fake.name_female(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": {"street": fake.street_address(), "city": fake.city(), "state": fake.state(), "zip": fake.zipcode(), "country": country if country else fake.country()},
        "geo": {"lat": float(fake.latitude()), "lng": float(fake.longitude())},
        "dob": fake.date_of_birth(minimum_age=age if age else 18).isoformat(),
        "gender": gender if gender else random.choice(["male", "female"]),
        "education": random.choice(["High School", "Bachelor's", "Master's", "PhD"]),
        "family": {"spouse": fake.name(), "children": [fake.first_name(), fake.first_name()]}
    }

    redis_client.setex(cache_key, 60, str(profile))
    
    return profile


# 🔹 Bulk Generate Fake Profiles
@app.get("/bulk-generate", dependencies=[Depends(validate_api_key)])
@limiter.limit("3/minute")
async def bulk_generate(request: Request, count: int = Query(1, le=100)):
    """Generate multiple fake profiles"""
    profiles = [await generate_fake_profile(request) for _ in range(count)]
    return profiles


# 🔹 Get API Stats
@app.get("/stats", dependencies=[Depends(validate_api_key)])
async def get_api_stats():
    """Retrieve API usage stats"""
    with db.cursor() as cursor:
        cursor.execute("SELECT endpoint, COUNT(*) AS count FROM api_logs GROUP BY endpoint")
        stats = cursor.fetchall()
    return stats


# 🔹 List of Supported Countries
@app.get("/countries")
async def get_countries():
    """Return a list of supported countries"""
    return {"countries": ["US", "IN", "UK", "CA", "AU"]}


# Run API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
