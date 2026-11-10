-- ============================================================================
-- FFernandes Engenharia e Construção Ltda. — Database Schema (SQLite 3NF)
-- ============================================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS company_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    legal_name TEXT NOT NULL,
    brand_name TEXT NOT NULL,
    years_badge TEXT NOT NULL,
    headline TEXT NOT NULL,
    subheadline TEXT NOT NULL,
    essence_summary TEXT NOT NULL,
    mission TEXT NOT NULL,
    vision TEXT NOT NULL,
    values_json TEXT NOT NULL,
    differentials_json TEXT NOT NULL,
    technical_signature TEXT NOT NULL,
    normative_note TEXT NOT NULL,
    address TEXT NOT NULL,
    city_state TEXT NOT NULL,
    phone_display TEXT NOT NULL,
    whatsapp_url TEXT NOT NULL,
    email TEXT NOT NULL,
    instagram_handle TEXT NOT NULL,
    instagram_url TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS engineering_services (
    id TEXT PRIMARY KEY,
    division_slug TEXT NOT NULL,
    division_title TEXT NOT NULL,
    specialty_name TEXT NOT NULL,
    specialty_order INTEGER NOT NULL,
    icon_name TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_services_division ON engineering_services(division_slug, specialty_order);

CREATE TABLE IF NOT EXISTS portfolio_projects (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    display_order INTEGER NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    category_slug TEXT NOT NULL,
    category_label TEXT NOT NULL,
    partner_name TEXT,
    area_or_scale TEXT,
    official_description TEXT NOT NULL,
    disciplines_json TEXT NOT NULL,
    cover_image TEXT NOT NULL,
    gallery_json TEXT NOT NULL,
    board_image TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_portfolio_category ON portfolio_projects(category_slug, display_order);

CREATE TABLE IF NOT EXISTS official_clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sector_slug TEXT NOT NULL,
    sector_label TEXT NOT NULL,
    logo_webp TEXT NOT NULL,
    logo_png TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clients_sector ON official_clients(sector_slug, id);

CREATE TABLE IF NOT EXISTS leads_orcamento (
    id TEXT PRIMARY KEY,
    idempotency_key TEXT UNIQUE,
    contact_name TEXT NOT NULL,
    company_name TEXT,
    phone_whatsapp TEXT NOT NULL,
    email TEXT NOT NULL,
    discipline_interest TEXT NOT NULL,
    project_location TEXT,
    message TEXT NOT NULL,
    client_ip TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads_orcamento(created_at DESC);
