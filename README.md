# JFAM Contact Form — Backend API

## Live Deployment
- **API:** https://jfam-backend.onrender.com
- **Swagger Docs:** https://jfam-backend.onrender.com/docs
- **Database:** Neon (PostgreSQL cloud)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/contact` | Submit form data |
| GET | `/api/contacts` | All inquiries |
| GET | `/api/contacts/{id}` | Single inquiry by ID |

---

## Frontend Integration (for JFAM team)

**Endpoint:** `POST https://jfam-backend.onrender.com/api/contact`

**Request body:**
```json
{
  "full_name": "string",
  "email_address": "string",
  "organisation_name": "string",
  "contact_number": "string",
  "project_type": "string",
  "location": "string",
  "investment": "string",
  "vision": "string",
  "best_time_to_reach": "string"
}
```

**Success response:**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "inquiry_id": 1
}
```

**Fetch call example:**
```javascript
const response = await fetch("https://jfam-backend.onrender.com/api/contact", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    full_name: formData.full_name,
    email_address: formData.email_address,
    organisation_name: formData.organisation_name,
    contact_number: formData.contact_number,
    project_type: formData.project_type,
    location: formData.location,
    investment: formData.investment,
    vision: formData.vision,
    best_time_to_reach: formData.best_time_to_reach
  })
});
const result = await response.json();
// result = { success: true, message: "...", inquiry_id: 1 }
```

> **Note:** First request may take ~30 seconds to wake up (free tier cold start).

---

## View Stored Data

All submitted inquiries can be fetched at:
```
GET https://jfam-backend.onrender.com/api/contacts
```

Or directly in Neon dashboard → SQL Editor:
```sql
SELECT * FROM project_inquiries ORDER BY submitted_at DESC;
```

---

## Local Development

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file:
```
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=jfam_db
PG_USER=jfam_user
PG_PASSWORD=jfam123
```

### 3. Create local DB and table
```sql
CREATE DATABASE jfam_db;
CREATE USER jfam_user WITH PASSWORD 'jfam123';
GRANT ALL PRIVILEGES ON DATABASE jfam_db TO jfam_user;
\c jfam_db
\i db_setup.sql
```

### 4. Start the server
```bash
uvicorn main:app --reload
```
Local API: http://localhost:8000  
Local docs: http://localhost:8000/docs

### 5. Test locally
```bash
python test_local.py
```

---

## Production Environment Variables (Render)

| Variable | Value |
|----------|-------|
| PG_HOST | Neon host |
| PG_PORT | 5432 |
| PG_DATABASE | neondb |
| PG_USER | neondb_owner |
| PG_PASSWORD | (set in Render dashboard) |
| PYTHON_VERSION | 3.11.0 |