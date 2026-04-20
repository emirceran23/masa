# Graph Report - .  (2026-04-20)

## Corpus Check
- 157 files · ~151,031 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 475 nodes · 870 edges · 35 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 350 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `User` - 53 edges
2. `NotFoundError` - 28 edges
3. `Base` - 27 edges
4. `PlaybookResponse` - 20 edges
5. `PlaybookDetailResponse` - 19 edges
6. `MessageResponse` - 19 edges
7. `Contract` - 17 edges
8. `RiskAssessmentResponse` - 16 edges
9. `SQLAlchemy ORM models – package root.  Import all models here so Alembic can det` - 12 edges
10. `Playbook` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Seed data loader — inserts default playbook and admin user.` --uses--> `Base`  [INFERRED]
  scripts/seed-data.py → backend/app/core/database.py
- `Playbook request / response schemas.` --uses--> `Base`  [INFERRED]
  backend/app/schemas/playbook.py → backend/app/core/database.py
- `Seed data loader — inserts default playbook and admin user.` --uses--> `User`  [INFERRED]
  scripts/seed-data.py → backend/app/models/user.py
- `Seed data loader — inserts default playbook and admin user.` --uses--> `Playbook`  [INFERRED]
  scripts/seed-data.py → backend/app/models/playbook.py
- `Seed data loader — inserts default playbook and admin user.` --uses--> `PlaybookRule`  [INFERRED]
  scripts/seed-data.py → backend/app/models/playbook.py

## Communities

### Community 0 - "Playbook & Tests"
Cohesion: 0.07
Nodes (43): Shared test fixtures., Return Authorization headers for the test user., A persisted playbook (no embedding — index_rule is mocked in tests)., A minimal persisted contract in 'analyzed' status., Playbook, PlaybookCreateRequest, PlaybookDetailResponse, PlaybookResponse (+35 more)

### Community 1 - "Clause Agent Pipeline"
Cohesion: 0.11
Nodes (32): BaseModel, _get_client(), Clause Agent — parses contract text into clauses and classifies each one., Send the contract text to GPT-4o, get structured clause list back.      Uses Ope, run_clause_agent(), Clause, ClauseDetailResponse, ClauseListResponse (+24 more)

### Community 2 - "Frontend UI"
Cohesion: 0.06
Nodes (0): 

### Community 3 - "Audit & Approval"
Cohesion: 0.08
Nodes (26): ApprovalDecision, Approval decision model., AuditLog, Audit trail service — records every critical action., Base, Base, get_db(), SQLAlchemy async engine and session factory. (+18 more)

### Community 4 - "Authentication API"
Cohesion: 0.14
Nodes (27): login(), LoginRequest, me(), Authentication endpoints — register, login, refresh., Yeni kullanıcı kaydı oluşturur., E-posta ve şifre ile giriş yapar, JWT token çifti döndürür., Refresh token kullanarak yeni access token alır., Geçerli oturumdaki kullanıcı bilgilerini döndürür. (+19 more)

### Community 5 - "Contract Analysis Pipeline"
Cohesion: 0.1
Nodes (18): Analysis service — orchestrates the full contract analysis pipeline., Run the full analysis pipeline for a contract.      Phase 1 (this sprint): claus, start_analysis(), Contract, Contract service — upload, list, detail, delete., Validate, store, convert to text, and persist contract metadata., upload_contract(), BadRequestError (+10 more)

### Community 6 - "Contract API Schemas"
Cohesion: 0.25
Nodes (17): MessageResponse, AnalyzeRequest, ContractDetailResponse, ContractListResponse, ContractResponse, Contract request / response schemas., analyze_contract(), contract_status() (+9 more)

### Community 7 - "Risk API Tests"
Cohesion: 0.12
Nodes (9): api_client(), auth_client(), _fake_user(), API tests for risk and missing-provisions endpoints — service mocked, no DB., Service enforces ownership — other user's contract looks like 404., Client with mocked DB — no auth override (for 401 tests)., _risk_response(), TestListRisks (+1 more)

### Community 8 - "Validator Tests"
Cohesion: 0.11
Nodes (5): Unit tests for validators., TestValidateEmail, TestValidateFileExtension, TestValidateFileSize, TestValidatePasswordStrength

### Community 9 - "RAG Embedding Tests"
Cohesion: 0.18
Nodes (7): _mock_openai_response(), Unit tests for rag/embeddings.py — OpenAI calls are fully mocked., Build a fake openai embeddings response for n inputs., Vectors must come back in the same order as inputs., embed_text must delegate to embed_texts (not duplicate logic)., TestEmbedText, TestEmbedTexts

### Community 10 - "Auth Tests"
Cohesion: 0.15
Nodes (4): Unit tests for auth endpoints., TestAuthLogin, TestAuthMe, TestAuthRegister

### Community 11 - "Redis Cache & Rate Limiting"
Cohesion: 0.2
Nodes (3): increment_login_attempts(), Redis client wrapper for session, cache, and rate-limiting., Increment failed login counter; returns current count.

### Community 12 - "WebSocket Manager"
Cohesion: 0.24
Nodes (4): WebSocket connection manager for real-time progress updates., Manages active WebSocket connections per contract analysis., Send a JSON message to every client watching a given contract., WebSocketManager

### Community 13 - "Input Validators"
Cohesion: 0.2
Nodes (9): Input validation helpers., Return the lowercase extension if valid, else raise ValueError., Raise ValueError if file exceeds maximum allowed size., Basic e-mail format validation., Enforce password policy (min 12 chars, mixed case, digit, special)., validate_email(), validate_file_extension(), validate_file_size() (+1 more)

### Community 14 - "Vector Store (pgvector)"
Cohesion: 0.27
Nodes (9): index_clause(), index_rule(), pgvector CRUD — index embeddings and search by cosine similarity., Convert a Python float list to the pgvector literal format '[1.0,2.0,...]'., Embed clause_text and upsert into clause_embeddings., Embed rule_text and upsert into playbook_rule_embeddings., Return the top-N playbook rules closest to query_text (cosine distance).      Ea, search_similar_rules() (+1 more)

### Community 15 - "MinIO Storage"
Cohesion: 0.29
Nodes (9): delete_file(), download_file(), ensure_bucket(), _get_client(), MinIO object-storage client wrapper., Create the default bucket if it doesn't exist (called on startup)., Upload bytes to MinIO. Returns the object path., Download an object from MinIO and return raw bytes. (+1 more)

### Community 16 - "Database Migrations"
Cohesion: 0.25
Nodes (7): Alembic environment configuration for async SQLAlchemy., Run migrations in 'offline' mode., Run migrations in 'online' (async) mode., Entry-point for online migrations — delegates to async runner., run_async_migrations(), run_migrations_offline(), run_migrations_online()

### Community 17 - "JWT & Security"
Cohesion: 0.25
Nodes (3): decode_token(), JWT token creation / verification and password hashing utilities., Return payload dict or None if invalid / expired.

### Community 18 - "Playbook Service"
Cohesion: 0.5
Nodes (6): create_playbook(), delete_playbook(), _get_owned_playbook(), get_playbook(), _index_rules(), update_playbook()

### Community 19 - "Document Processor"
Cohesion: 0.32
Nodes (7): docx_to_text(), extract_text(), pdf_to_text(), Document processor — PDF / DOCX → plain text conversion., Extract text from a PDF file. Falls back to OCR for scanned pages., Extract text from a DOCX file., Unified entry point — dispatches by format.

### Community 20 - "Test Infrastructure"
Cohesion: 0.36
Nodes (5): auth_headers(), _session_factory(), test_contract(), test_playbook(), test_user()

### Community 21 - "Doc Processor Tests"
Cohesion: 0.25
Nodes (4): Unit tests for document processing (text extraction)., Smoke test — creates a minimal dummy PDF to verify the pipeline., Smoke test with docx — requires python-docx., TestExtractText

### Community 22 - "App Configuration"
Cohesion: 0.29
Nodes (3): BaseSettings, Application configuration via environment variables., Settings

### Community 23 - "OpenAI Embeddings"
Cohesion: 0.38
Nodes (6): embed_text(), embed_texts(), _get_client(), OpenAI embedding helper — converts text to 1536-dim vectors., Return an embedding vector for each input string.      Sends all texts in a sing, Convenience wrapper for a single string.

### Community 24 - "RAG Retriever"
Cohesion: 0.5
Nodes (3): High-level retriever — called by the Risk Agent to get relevant playbook rules., Return the most semantically similar playbook rules for a given clause.      Arg, retrieve_relevant_rules()

### Community 25 - "WebSocket Endpoint"
Cohesion: 0.5
Nodes (3): WebSocket endpoint for real-time analysis progress., Clients connect here to receive real-time analysis updates., websocket_progress()

### Community 26 - "OCR Service"
Cohesion: 0.5
Nodes (3): ocr_image_bytes(), OCR service — Tesseract wrapper for scanned documents., Run Tesseract OCR on raw image bytes. Default language: Turkish.

### Community 27 - "Initial Schema Migration"
Cohesion: 0.5
Nodes (1): initial schema  Revision ID: 0001 Revises: Create Date: 2025-01-01 00:00:00.0000

### Community 28 - "pgvector Migration"
Cohesion: 0.5
Nodes (1): add pgvector embedding tables  Revision ID: 0002 Revises: 0001 Create Date: 2026

### Community 29 - "Clause Prompts"
Cohesion: 1.0
Nodes (1): Prompt templates for the Clause Agent (parsing & classification).

### Community 30 - "API Router"
Cohesion: 1.0
Nodes (1): API v1 router — aggregates all sub-routers.

### Community 31 - "Next.js Config"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Tailwind Config"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "PostCSS Config"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "TS Entry Point"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **62 isolated node(s):** `Application configuration via environment variables.`, `SQLAlchemy async engine and session factory.`, `Base class for all ORM models.`, `Dependency that yields an async database session.`, `JWT token creation / verification and password hashing utilities.` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Clause Prompts`** (2 nodes): `clause_prompts.py`, `Prompt templates for the Clause Agent (parsing & classification).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `API Router`** (2 nodes): `router.py`, `API v1 router — aggregates all sub-routers.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Next.js Config`** (1 nodes): `next.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tailwind Config`** (1 nodes): `tailwind.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `PostCSS Config`** (1 nodes): `postcss.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `TS Entry Point`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Playbook & Tests` to `Clause Agent Pipeline`, `Audit & Approval`, `Authentication API`, `Contract API Schemas`, `Risk API Tests`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `Authentication endpoints — register, login, refresh.` connect `Authentication API` to `Playbook & Tests`, `Contract API Schemas`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `Base` connect `Audit & Approval` to `Playbook & Tests`, `Clause Agent Pipeline`, `Contract Analysis Pipeline`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `User` (e.g. with `Base` and `SQLAlchemy ORM models – package root.  Import all models here so Alembic can det`) actually correct?**
  _`User` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `NotFoundError` (e.g. with `Clause endpoints — list, detail, manual category update.` and `Bir sözleşmenin tüm maddelerini döndürür.`) actually correct?**
  _`NotFoundError` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `Base` (e.g. with `Lagent — FastAPI Application Factory.` and `Startup & shutdown hooks.`) actually correct?**
  _`Base` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `PlaybookResponse` (e.g. with `Playbook endpoints — CRUD.` and `Kullanıcının tüm playbook'larını listeler.`) actually correct?**
  _`PlaybookResponse` has 17 INFERRED edges - model-reasoned connections that need verification._