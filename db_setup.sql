-- Run this inside psql after connecting to jfam_db
-- Connect with: \c jfam_db

CREATE TABLE IF NOT EXISTS project_inquiries (
    id                  SERIAL PRIMARY KEY,
    full_name           VARCHAR(200)    NOT NULL,
    email_address       VARCHAR(300)    NOT NULL,
    organisation_name   VARCHAR(300)    NOT NULL,
    contact_number      VARCHAR(20)     NOT NULL,
    project_type        VARCHAR(100),
    location            VARCHAR(200),
    investment          VARCHAR(100),
    vision              TEXT,
    best_time_to_reach  VARCHAR(100),
    submitted_at        TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for fast email lookups
CREATE INDEX IF NOT EXISTS idx_inquiries_email
    ON project_inquiries(email_address);
