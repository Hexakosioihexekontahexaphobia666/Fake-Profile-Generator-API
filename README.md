# 🚀 Fake Profile Generator API (FastAPI)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)

## 📖 Overview

The **Fake Profile Generator API** allows users to generate **random but realistic** fake profiles, including names, emails, phone numbers, addresses, educational background, and more. 

✅ **Features**
- 🔑 **User Registration & API Key Management** (Generate, List, Revoke)
- 🧑 **Generate Fake Profiles** (`/generate`)
- 📦 **Bulk Profile Generation** (`/bulk-generate`)
- 🌍 **Country Filtering** (`/countries`)
- 📊 **Usage Statistics** (`/stats`)
- 🔒 **Rate Limiting & API Security**
- ⚡ **Fast Performance with Redis Caching**
- 💾 **MySQL Database for API Logs & User Management**

---

## 🛠 **Installation & Setup**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/fake-profile-api.git
cd fake-profile-api
```

### **2️⃣ Install Dependencies**
Ensure you have Python **3.8+** and install required dependencies:
```sh
pip install fastapi uvicorn faker redis pymysql slowapi passlib bcrypt
```

### **3️⃣ Setup MySQL Database**
Run the following SQL script to create necessary tables:
```sql
CREATE DATABASE api_service;

USE api_service;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### **4️⃣ Start the FastAPI Server**
Run the API with:
```sh
uvicorn main:app --reload
```
Server should start at `http://127.0.0.1:8000`

---

## 🔥 **Usage Examples**

### 📝 **1️⃣ User Registration**
#### **Endpoint**: `POST /register`
```sh
curl -X POST "http://127.0.0.1:8000/register?username=johndoe&password=securepassword"
```
📌 **Response**:
```json
{
  "message": "User registered successfully"
}
```

---

### 🔑 **2️⃣ Generate an API Key**
#### **Endpoint**: `POST /generate-api-key`
```sh
curl -X POST "http://127.0.0.1:8000/generate-api-key?username=johndoe&password=securepassword"
```
📌 **Response**:
```json
{
  "api_key": "your-generated-api-key"
}
```

---

### 👤 **3️⃣ Generate Fake Profile**
#### **Endpoint**: `GET /generate`
```sh
curl -H "X-API-Key: your-generated-api-key" \
     "http://127.0.0.1:8000/generate?age=25&gender=male&country=US"
```
📌 **Response**:
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1-202-555-0192",
  "address": {
    "street": "123 Fake Street",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
  },
  "geo": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "dob": "1990-05-22",
  "gender": "male",
  "education": "Master's Degree in Computer Science",
  "family": {
    "spouse": "Jane Doe",
    "children": ["Emma Doe", "Lucas Doe"]
  }
}
```

---

### 📦 **4️⃣ Bulk Generate Fake Profiles**
#### **Endpoint**: `GET /bulk-generate`
```sh
curl -H "X-API-Key: your-generated-api-key" \
     "http://127.0.0.1:8000/bulk-generate?count=5"
```
📌 **Response**:
```json
[
  { "name": "Alice Johnson", "email": "alice@example.com", ... },
  { "name": "Bob Smith", "email": "bob@example.com", ... }
]
```

---

### 🔍 **5️⃣ List User API Keys**
#### **Endpoint**: `GET /list-api-keys`
```sh
curl -H "X-API-Key: your-generated-api-key" \
     "http://127.0.0.1:8000/list-api-keys"
```
📌 **Response**:
```json
{
  "api_keys": [
    { "api_key": "your-api-key-1", "created_at": "2024-02-05 12:00:00" },
    { "api_key": "your-api-key-2", "created_at": "2024-02-06 14:30:00" }
  ]
}
```

---

### ❌ **6️⃣ Revoke API Key**
#### **Endpoint**: `DELETE /revoke-api-key`
```sh
curl -X DELETE -H "X-API-Key: your-generated-api-key" \
     "http://127.0.0.1:8000/revoke-api-key?api_key=your-api-key-1"
```
📌 **Response**:
```json
{
  "message": "API key revoked successfully"
}
```

---

## 📊 **API Statistics**
#### **Endpoint**: `GET /stats`
```sh
curl -H "X-API-Key: your-generated-api-key" \
     "http://127.0.0.1:8000/stats"
```
📌 **Response**:
```json
[
  { "endpoint": "/generate", "count": 150 },
  { "endpoint": "/bulk-generate", "count": 75 }
]
```

---

## ❓ **FAQs**

### 1️⃣ Why do I need an API Key?
An API Key is required for **authentication and security** to prevent abuse.

### 2️⃣ How do I increase my rate limit?
Rate limits are set at `5 requests/minute`. Contact the developer for custom plans.

### 3️⃣ Can I use this API commercially?
Yes! You can integrate it into any **project, application, or SaaS service**.

### 4️⃣ Can I deploy this on a cloud server?
Yes! You can deploy it on **AWS, DigitalOcean, Heroku, or Railway.app**.

---

## 📜 **License**
This project is licensed under the **MIT License**.

---

## 🤝 **Contributing**
Feel free to open issues, submit PRs, or request new features!

---

## 💡 **Need Help?**
For any questions, reach out via:
📧 Email: `your-email@example.com`  
🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)  
```
