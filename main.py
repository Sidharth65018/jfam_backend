from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="JFAM Contact Form API",
    description="Backend API for JFAM project inquiry form",
    version="1.0.0"
)

# CORS — allows the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://jfam.co.in"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── PostgreSQL connection ───────────────────────────────────────────────────

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432"),
            dbname=os.getenv("PG_DATABASE", "jfam_db"),
            user=os.getenv("PG_USER", "jfam_user"),
            password=os.getenv("PG_PASSWORD", "jfam123")
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"DB connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# ── Pydantic schema (matches all form fields) ───────────────────────────────

class ContactFormData(BaseModel):
    full_name: str
    email_address: str
    organisation_name: str
    contact_number: str
    project_type: Optional[str] = None
    location: Optional[str] = None
    investment: Optional[str] = None
    vision: Optional[str] = None
    best_time_to_reach: Optional[str] = None


# ── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "JFAM API is running ✓"}


@app.post("/api/contact", status_code=201)
def submit_contact_form(data: ContactFormData):
    """Receives form submission and stores it in PostgreSQL."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO project_inquiries (
                full_name, email_address, organisation_name,
                contact_number, project_type, location,
                investment, vision, best_time_to_reach
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.full_name,
            data.email_address,
            data.organisation_name,
            data.contact_number,
            data.project_type,
            data.location,
            data.investment,
            data.vision,
            data.best_time_to_reach
        ))

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        logger.info(f"New inquiry stored: id={inserted_id}, email={data.email_address}")
        return {
            "success": True,
            "message": "Application submitted successfully",
            "inquiry_id": inserted_id
        }

    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Insert failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/api/contacts")
def get_all_contacts():
    """Fetch all submitted inquiries."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute("""
            SELECT * FROM project_inquiries
            ORDER BY submitted_at DESC
        """)
        rows = cursor.fetchall()
        return {"count": len(rows), "data": [dict(r) for r in rows]}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


@app.get("/api/contacts/{inquiry_id}")
def get_contact_by_id(inquiry_id: int):
    """Fetch a single inquiry by ID."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(
            "SELECT * FROM project_inquiries WHERE id = %s",
            (inquiry_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Inquiry not found")
        return dict(row)

    finally:
        cursor.close()
        conn.close()
