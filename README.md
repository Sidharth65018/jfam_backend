# JFAM Contact Form — Backend API (PostgreSQL)

## Setup (do this once)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create DB and table
Open SQL Shell (psql) from Start Menu:
```sql
CREATE DATABASE jfam_db;
CREATE USER jfam_user WITH PASSWORD 'jfam123';
GRANT ALL PRIVILEGES ON DATABASE jfam_db TO jfam_user;
\c jfam_db
\i db_setup.sql
\q
```

### 3. Start the server
```bash
uvicorn main:app --reload
```
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 4. Test it
Open a second terminal:
```bash
python test_local.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/contact` | Submit form |
| GET | `/api/contacts` | All inquiries |
| GET | `/api/contacts/{id}` | Single inquiry |

---

## Handoff to JFAM Frontend Team

1. Deploy to Railway/Render (free) — set the 5 env variables from `.env`
2. In `main.py` change `allow_origins=["*"]` to `allow_origins=["https://jfam.co.in"]`
3. Share: your deployed URL + `POST /api/contact` endpoint

Their fetch call:
```javascript
await fetch("https://your-api.com/api/contact", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(formData)
});
```
