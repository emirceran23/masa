# 🏗️ Lagent — Sıfırdan Ürüne Uygulama Planı

## Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü (Multi-Agent Legal Ops)

> **Ekip:** Mustafa Emir Ceran · Mert Ayrancı · Osman Gazi Atalay  
> **Tarih:** 8 Nisan 2026  
> **Durum:** 🟡 **AŞAMA 4 DEVAM EDİYOR** — Sprint 4.1 Raporlama & Dışa Aktarım ✅ · Sprint 4.2 UAT & Güvenlik ⏳

---

## İçindekiler

1. [Proje Özeti](#1-proje-özeti)
2. [Mimari Genel Bakış](#2-mimari-genel-bakış)
3. [Teknoloji Yığını](#3-teknoloji-yığını)
4. [Proje Dizin Yapısı](#4-proje-dizin-yapısı)
5. [Veritabanı Şeması](#5-veritabanı-şeması)
6. [API Tasarımı](#6-api-tasarımı)
7. [Ajan Mimarisi](#7-ajan-mimarisi)
8. [Frontend Ekran Haritası](#8-frontend-ekran-haritası)
9. [Aşama Aşama Uygulama Planı](#9-aşama-aşama-uygulama-planı)
10. [Test Stratejisi](#10-test-stratejisi)
11. [CI/CD ve Dağıtım](#11-cicd-ve-dağıtım)
12. [Güvenlik Kontrol Listesi](#12-güvenlik-kontrol-listesi)
13. [Risk Yönetimi](#13-risk-yönetimi)
14. [Ekip Görev Dağılımı](#14-ekip-görev-dağılımı)
15. [Zaman Çizelgesi (Gantt)](#15-zaman-çizelgesi)

---

## 1. Proje Özeti

**Lagent**, bireylerin ve KOBİ'lerin karşılaştığı sözleşme metinlerini yapay zeka destekli çoklu ajan mimarisiyle:

- Otomatik ayrıştırma ve madde bazlı sınıflandırma
- Kullanıcı politikalarına (Playbook) göre risk analizi
- Riskli maddeler için alternatif ifade (revizyon) önerisi
- Karşılaştırmalı görünüm (Redline/Diff)
- Madde bazlı onay/red akışı ve denetim izi (Audit Trail)
- Rapor oluşturma ve revize sözleşme dışa aktarımı

işlevleriyle analiz eden bağımsız bir web uygulamasıdır.

**Hedef:** Hukuki inceleme süreçlerini demokratikleştirmek, avukat desteğinin yerini almak yerine ön inceleme aşamasında güvenilir asistanlık sunmak.

---

## 2. Mimari Genel Bakış

```
┌─────────────────────────────────────────────────────────────────┐
│                        İSTEMCİ KATMANI                         │
│                  Next.js / React Web Dashboard                  │
│    (Giriş · Dashboard · Yükleme · Analiz · Redline · Rapor)   │
└──────────────────────┬──────────────────────────────────────────┘
                       │  HTTPS / REST / WebSocket (WSS)
┌──────────────────────▼──────────────────────────────────────────┐
│                    API KATMANI (FastAPI)                         │
│  Auth · Contract · Analysis · Playbook · Report · Approval      │
│  WebSocket Manager  ·  Background Tasks (Celery/ARQ)            │
└──────┬──────────┬──────────┬──────────┬─────────────────────────┘
       │          │          │          │
┌──────▼──┐ ┌────▼────┐ ┌───▼───┐ ┌───▼────┐
│Orkestratör│ │  RAG    │ │ Kural │ │ Dosya  │
│(LangGraph)│ │Katmanı  │ │Motoru │ │İşleme  │
│           │ │(pgvector│ │       │ │(PyMuPDF│
│ ┌───────┐ │ │+OpenAI  │ │       │ │docx    │
│ │Clause │ │ │Embedding│ │       │ │OCR)    │
│ │ Agent │ │ │)        │ │       │ │        │
│ ├───────┤ │ └─────────┘ └───────┘ └────────┘
│ │Risk   │ │
│ │ Agent │ │
│ ├───────┤ │
│ │Negoti-│ │
│ │ation  │ │
│ │ Agent │ │
│ └───────┘ │
└──────┬────┘
       │
┌──────▼──────────────────────────────────────────────────────────┐
│                      VERİ YÖNETİM KATMANI                       │
│  PostgreSQL + pgvector  ·  Redis  ·  MinIO (Object Storage)     │
└─────────────────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────────┐
│                     HARİCİ SERVİSLER                            │
│              OpenAI API (GPT-4o) · OCR Servisi                  │
└─────────────────────────────────────────────────────────────────┘
```

### Katman Açıklamaları

| Katman | Sorumluluk | Teknoloji |
|--------|-----------|-----------|
| İstemci | Kullanıcı etkileşimi, dashboard, redline görünümü | Next.js 14 + React 18 + Tailwind CSS |
| API | RESTful uç noktalar, kimlik doğrulama, WebSocket | FastAPI + Uvicorn + Pydantic |
| Orkestratör | Ajan koordinasyonu, durum yönetimi, iş akışı | LangGraph + LangChain |
| RAG | Vektörel arama, bağlam zenginleştirme | pgvector + OpenAI Embeddings |
| Kural Motoru | Deterministik çapraz doğrulama | Python if/else kural sistemi |
| Dosya İşleme | PDF/DOCX → düz metin, OCR | PyMuPDF + python-docx + Tesseract |
| Veri Yönetimi | Kalıcı depolama, önbellek, dosya deposu | PostgreSQL + Redis + MinIO |

---

## 3. Teknoloji Yığını

### Backend
| Bileşen | Teknoloji | Sürüm | Amaç |
|---------|-----------|-------|------|
| Web Framework | FastAPI | 0.110+ | REST API + WebSocket |
| ASGI Server | Uvicorn | 0.29+ | Asenkron sunucu |
| ORM | SQLAlchemy 2.0 | 2.0+ | Veritabanı erişimi |
| Migration | Alembic | 1.13+ | DB şema versiyonlama |
| Ajan Orkestrasyon | LangGraph | 0.2+ | Durum tabanlı ajan akışları |
| LLM Entegrasyon | LangChain + OpenAI | latest | GPT-4o API çağrıları |
| Embedding | OpenAI text-embedding-3-small | — | Vektör temsili |
| PDF İşleme | PyMuPDF (fitz) | 1.24+ | PDF → metin |
| DOCX İşleme | python-docx | 1.1+ | DOCX okuma/yazma |
| OCR | Tesseract + pytesseract | 5.x | Taranmış belge desteği |
| Görev Kuyruğu | ARQ (veya Celery) | latest | Arka plan görevleri |
| Validasyon | Pydantic v2 | 2.6+ | Veri doğrulama |
| Şifreleme | passlib[bcrypt] | latest | Şifre hash |
| Token | python-jose[cryptography] | latest | JWT token |
| Test | pytest + pytest-asyncio + httpx | latest | Birim + entegrasyon test |

### Frontend
| Bileşen | Teknoloji | Sürüm | Amaç |
|---------|-----------|-------|------|
| Framework | Next.js | 14.x | SSR + routing |
| UI Kütüphanesi | React | 18.x | Bileşen tabanlı UI |
| Stil | Tailwind CSS | 3.x | Utility-first CSS |
| UI Bileşenleri | shadcn/ui | latest | Önceden yapılmış bileşenler |
| State Yönetimi | Zustand | latest | Global state |
| HTTP İstemci | Axios | latest | API çağrıları |
| WebSocket | native WebSocket API | — | Gerçek zamanlı bildirim |
| Diff Görünüm | diff-match-patch / react-diff-viewer | latest | Redline ekranı |
| Form | React Hook Form + Zod | latest | Form validasyon |
| Test | Playwright | latest | E2E test |

### Altyapı & DevOps
| Bileşen | Teknoloji | Amaç |
|---------|-----------|------|
| Konteyner | Docker + Docker Compose | İzolasyon, taşınabilirlik |
| Veritabanı | PostgreSQL 16 + pgvector | İlişkisel veri + vektör arama |
| Önbellek | Redis 7 | Oturum, durum, cache |
| Dosya Deposu | MinIO | S3 uyumlu nesne depolama |
| CI/CD | GitHub Actions | Otomatik build, test, deploy |
| Versiyon Kontrol | Git + GitHub | Kod yönetimi |
| Proje Yönetimi | Trello (Kanban) | İş takibi |

---

## 4. Proje Dizin Yapısı

```
lagent/
├── docker-compose.yml              # Tüm servisleri başlatan compose dosyası
├── docker-compose.dev.yml           # Geliştirme ortamı override
├── .env.example                     # Ortam değişkenleri şablonu
├── .github/
│   └── workflows/
│       ├── ci.yml                   # CI pipeline (lint, test, build)
│       └── cd.yml                   # CD pipeline (deploy)
├── README.md
├── IMPLEMENTATION_PLAN.md
│
├── backend/                         # Python FastAPI Backend
│   ├── Dockerfile
│   ├── pyproject.toml               # Python proje yapılandırması (Poetry/pip)
│   ├── alembic.ini                  # Alembic migration config
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/               # Migration dosyaları
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app factory + startup/shutdown
│   │   ├── config.py                # Pydantic Settings (env vars)
│   │   │
│   │   ├── api/                     # API Katmanı (Router'lar)
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # Dependency injection (get_db, get_current_user)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py        # Ana router (tüm sub-router'ları birleştirir)
│   │   │       ├── auth.py          # POST /auth/register, /auth/login, /auth/refresh
│   │   │       ├── contracts.py     # CRUD sözleşme + yükleme + analiz tetikleme
│   │   │       ├── clauses.py       # Madde listeleme, detay, manuel düzenleme
│   │   │       ├── analysis.py      # Analiz başlatma, durum sorgulama
│   │   │       ├── risks.py         # Risk sonuçları listeleme
│   │   │       ├── revisions.py     # Revizyon önerileri, düzenleme, kabul/red
│   │   │       ├── approvals.py     # Onay akışı kararları
│   │   │       ├── playbooks.py     # Playbook CRUD
│   │   │       ├── reports.py       # Rapor oluşturma ve indirme
│   │   │       ├── admin.py         # Yönetici: kullanıcı yönetimi, sistem ayarları
│   │   │       └── ws.py            # WebSocket endpoint (ilerleme bildirimi)
│   │   │
│   │   ├── models/                  # SQLAlchemy ORM Modelleri
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User modeli
│   │   │   ├── contract.py          # Contract modeli
│   │   │   ├── clause.py            # Clause modeli
│   │   │   ├── risk_assessment.py   # RiskAssessment modeli
│   │   │   ├── revision.py          # Revision modeli
│   │   │   ├── approval.py          # ApprovalDecision modeli
│   │   │   ├── playbook.py          # Playbook + PlaybookRule modeli
│   │   │   ├── audit_log.py         # AuditLog modeli
│   │   │   └── report.py            # Report modeli
│   │   │
│   │   ├── schemas/                 # Pydantic Şemaları (Request/Response)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── contract.py
│   │   │   ├── clause.py
│   │   │   ├── risk.py
│   │   │   ├── revision.py
│   │   │   ├── approval.py
│   │   │   ├── playbook.py
│   │   │   ├── report.py
│   │   │   └── common.py            # Ortak şemalar (pagination, error response)
│   │   │
│   │   ├── services/                # İş Mantığı Katmanı
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # Kayıt, giriş, token yönetimi
│   │   │   ├── contract_service.py  # Sözleşme yükleme, listeleme
│   │   │   ├── document_processor.py# PDF/DOCX → düz metin dönüşümü
│   │   │   ├── ocr_service.py       # Tesseract OCR entegrasyonu
│   │   │   ├── analysis_service.py  # Analiz başlatma, orkestratör çağrısı
│   │   │   ├── playbook_service.py  # Playbook CRUD + vektör indeks güncelleme
│   │   │   ├── report_service.py    # Rapor oluşturma (PDF/DOCX)
│   │   │   ├── approval_service.py  # Onay akışı iş mantığı
│   │   │   ├── export_service.py    # Revize sözleşme DOCX dışa aktarım
│   │   │   └── audit_service.py     # Denetim izi kayıt servisi
│   │   │
│   │   ├── agents/                  # Yapay Zeka Ajanları
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py      # LangGraph ana orkestratör (state machine)
│   │   │   ├── clause_agent.py      # Madde ayrıştırma ve sınıflandırma ajanı
│   │   │   ├── risk_agent.py        # Politika kontrolü ve risk değerlendirme ajanı
│   │   │   ├── negotiation_agent.py # Revizyon önerisi üretme ajanı
│   │   │   ├── prompts/             # Prompt şablonları
│   │   │   │   ├── __init__.py
│   │   │   │   ├── clause_prompts.py
│   │   │   │   ├── risk_prompts.py
│   │   │   │   └── negotiation_prompts.py
│   │   │   └── schemas/             # Structured Output şemaları (Function Calling)
│   │   │       ├── __init__.py
│   │   │       ├── clause_schema.py
│   │   │       ├── risk_schema.py
│   │   │       └── revision_schema.py
│   │   │
│   │   ├── rag/                     # RAG Altyapısı
│   │   │   ├── __init__.py
│   │   │   ├── embeddings.py        # OpenAI embedding çağrıları
│   │   │   ├── vector_store.py      # pgvector CRUD (indeksleme, arama)
│   │   │   └── retriever.py         # Anlamsal benzerlik arama fonksiyonları
│   │   │
│   │   ├── rules/                   # Deterministik Kural Motoru
│   │   │   ├── __init__.py
│   │   │   ├── engine.py            # Kural çalıştırma motoru
│   │   │   └── validators.py        # Çapraz doğrulama kuralları
│   │   │
│   │   ├── storage/                 # Dosya Depolama
│   │   │   ├── __init__.py
│   │   │   └── minio_client.py      # MinIO S3 client wrapper
│   │   │
│   │   ├── core/                    # Çekirdek Yardımcılar
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # SQLAlchemy engine + session factory
│   │   │   ├── redis.py             # Redis client
│   │   │   ├── security.py          # JWT oluşturma/doğrulama, bcrypt
│   │   │   ├── exceptions.py        # Özel hata sınıfları
│   │   │   └── websocket_manager.py # WebSocket bağlantı yönetimi
│   │   │
│   │   └── utils/                   # Genel Yardımcı Fonksiyonlar
│   │       ├── __init__.py
│   │       ├── diff.py              # Metin karşılaştırma (redline üretimi)
│   │       └── validators.py        # Dosya format/boyut doğrulama
│   │
│   └── tests/                       # Backend Testleri
│       ├── conftest.py              # Test fixtures (test DB, test client)
│       ├── unit/
│       │   ├── test_auth_service.py
│       │   ├── test_document_processor.py
│       │   ├── test_clause_agent.py
│       │   ├── test_risk_agent.py
│       │   ├── test_negotiation_agent.py
│       │   ├── test_rule_engine.py
│       │   ├── test_approval_service.py
│       │   └── test_playbook_service.py
│       ├── integration/
│       │   ├── test_contract_flow.py
│       │   ├── test_analysis_pipeline.py
│       │   ├── test_approval_flow.py
│       │   └── test_rag_pipeline.py
│       └── fixtures/
│           ├── sample_contract.pdf
│           ├── sample_contract.docx
│           └── sample_playbook.json
│
├── frontend/                        # Next.js Frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   │
│   ├── public/
│   │   └── logo.svg
│   │
│   ├── src/
│   │   ├── app/                     # Next.js App Router
│   │   │   ├── layout.tsx           # Kök layout (font, metadata, providers)
│   │   │   ├── page.tsx             # Landing / redirect to dashboard
│   │   │   │
│   │   │   ├── (auth)/              # Kimlik Doğrulama Grubu
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx     # Giriş ekranı
│   │   │   │   └── register/
│   │   │   │       └── page.tsx     # Kayıt ekranı
│   │   │   │
│   │   │   ├── (dashboard)/         # Dashboard Grubu (korumalı)
│   │   │   │   ├── layout.tsx       # Sidebar + topbar layout
│   │   │   │   ├── page.tsx         # Ana kontrol paneli
│   │   │   │   │
│   │   │   │   ├── contracts/
│   │   │   │   │   ├── page.tsx     # Sözleşme listesi
│   │   │   │   │   ├── upload/
│   │   │   │   │   │   └── page.tsx # Yükleme ekranı
│   │   │   │   │   └── [id]/
│   │   │   │   │       ├── page.tsx          # Sözleşme detay / analiz ekranı
│   │   │   │   │       ├── clauses/
│   │   │   │   │       │   └── [clauseId]/
│   │   │   │   │       │       └── page.tsx  # Madde detay + risk + revizyon
│   │   │   │   │       ├── redline/
│   │   │   │   │       │   └── page.tsx      # Karşılaştırmalı görünüm (Redline)
│   │   │   │   │       ├── approvals/
│   │   │   │   │       │   └── page.tsx      # Onay akışı paneli
│   │   │   │   │       └── report/
│   │   │   │   │           └── page.tsx      # Rapor görüntüleme + indirme
│   │   │   │   │
│   │   │   │   ├── playbooks/
│   │   │   │   │   ├── page.tsx     # Playbook listesi
│   │   │   │   │   ├── new/
│   │   │   │   │   │   └── page.tsx # Yeni Playbook oluşturma
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── page.tsx # Playbook düzenleme
│   │   │   │   │
│   │   │   │   └── settings/
│   │   │   │       └── page.tsx     # Profil + sistem ayarları
│   │   │   │
│   │   │   └── admin/               # Yönetici Paneli
│   │   │       ├── layout.tsx
│   │   │       ├── users/
│   │   │       │   └── page.tsx     # Kullanıcı yönetimi
│   │   │       └── config/
│   │   │           └── page.tsx     # Sistem yapılandırması
│   │   │
│   │   ├── components/              # Yeniden Kullanılabilir Bileşenler
│   │   │   ├── ui/                  # shadcn/ui temel bileşenler
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── toast.tsx
│   │   │   │   ├── progress.tsx
│   │   │   │   └── ...
│   │   │   ├── layout/
│   │   │   │   ├── sidebar.tsx      # Dashboard sidebar
│   │   │   │   ├── topbar.tsx       # Üst bar (kullanıcı menüsü, bildirimler)
│   │   │   │   └── breadcrumb.tsx
│   │   │   ├── contract/
│   │   │   │   ├── contract-card.tsx
│   │   │   │   ├── upload-dropzone.tsx
│   │   │   │   ├── clause-list.tsx
│   │   │   │   ├── clause-detail.tsx
│   │   │   │   └── risk-badge.tsx
│   │   │   ├── analysis/
│   │   │   │   ├── analysis-progress.tsx  # Gerçek zamanlı ilerleme
│   │   │   │   ├── risk-summary.tsx
│   │   │   │   └── risk-chart.tsx
│   │   │   ├── redline/
│   │   │   │   ├── diff-viewer.tsx        # Karşılaştırmalı metin görünümü
│   │   │   │   └── inline-diff.tsx
│   │   │   ├── approval/
│   │   │   │   ├── approval-panel.tsx
│   │   │   │   ├── decision-buttons.tsx
│   │   │   │   └── audit-timeline.tsx
│   │   │   ├── playbook/
│   │   │   │   ├── playbook-form.tsx
│   │   │   │   ├── rule-editor.tsx
│   │   │   │   └── playbook-selector.tsx
│   │   │   └── report/
│   │   │       ├── summary-report.tsx
│   │   │       └── detailed-report.tsx
│   │   │
│   │   ├── lib/                     # Yardımcı Kütüphaneler
│   │   │   ├── api.ts               # Axios instance + interceptor (token ekleme)
│   │   │   ├── auth.ts              # Token saklama/yenileme
│   │   │   ├── websocket.ts         # WebSocket bağlantı yönetimi
│   │   │   └── utils.ts             # Genel yardımcı fonksiyonlar
│   │   │
│   │   ├── hooks/                   # Özel React Hook'ları
│   │   │   ├── use-auth.ts          # Kimlik doğrulama hook
│   │   │   ├── use-contracts.ts     # Sözleşme CRUD hook
│   │   │   ├── use-analysis.ts      # Analiz durumu hook
│   │   │   ├── use-websocket.ts     # WebSocket hook
│   │   │   └── use-playbooks.ts     # Playbook hook
│   │   │
│   │   ├── store/                   # Zustand Store'ları
│   │   │   ├── auth-store.ts
│   │   │   ├── contract-store.ts
│   │   │   └── notification-store.ts
│   │   │
│   │   └── types/                   # TypeScript Tip Tanımları
│   │       ├── api.ts               # API response tipleri
│   │       ├── contract.ts
│   │       ├── clause.ts
│   │       ├── playbook.ts
│   │       └── user.ts
│   │
│   └── tests/                       # Frontend Testleri
│       ├── e2e/
│       │   ├── auth.spec.ts         # Giriş/kayıt E2E
│       │   ├── contract-upload.spec.ts
│       │   ├── analysis-flow.spec.ts
│       │   ├── approval-flow.spec.ts
│       │   └── playbook.spec.ts
│       └── playwright.config.ts
│
├── docs/                            # Proje Dokümanları
│   ├── Lagent_SPMP.pdf
│   ├── Lagent_SRS.pdf
│   ├── SDD.md                       # Yazılım Tasarım Dokümanı
│   ├── STD.md                       # Yazılım Test Dokümanı
│   ├── API_REFERENCE.md             # API referansı
│   └── USER_GUIDE.md                # Kullanıcı kılavuzu
│
├── data/                            # Başlangıç Verileri
│   ├── seed/
│   │   ├── default_playbook.json    # Varsayılan Playbook şablonu
│   │   ├── categories.json          # Hukuki kategori listesi
│   │   └── risk_rubric.json         # Risk değerlendirme rubriği
│   └── samples/
│       ├── kira_sozlesmesi.pdf      # Test sözleşmeleri
│       └── ticari_anlasma.docx
│
└── scripts/                         # Yardımcı Scriptler
    ├── init-db.sh                   # Veritabanı başlatma
    ├── seed-data.py                 # Başlangıç verisi yükleme
    └── generate-embeddings.py       # İlk vektör indeksleme
```

---

## 5. Veritabanı Şeması

### 5.1 ER Diyagramı (PostgreSQL + pgvector)

```sql
-- ===== KULLANICILAR =====
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    role            VARCHAR(50) DEFAULT 'user',         -- 'user' | 'admin'
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ===== SÖZLEŞMELER =====
CREATE TABLE contracts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    file_name       VARCHAR(500) NOT NULL,
    storage_path    VARCHAR(1000) NOT NULL,              -- MinIO object key
    file_format     VARCHAR(10) NOT NULL,                -- 'pdf' | 'docx'
    file_size       BIGINT NOT NULL,
    raw_text        TEXT,                                -- Dönüştürülmüş düz metin
    status          VARCHAR(50) DEFAULT 'uploaded',      -- uploaded|processing|analyzed|error
    total_clauses   INTEGER DEFAULT 0,
    playbook_id     UUID REFERENCES playbooks(id),       -- Kullanılan playbook
    uploaded_at     TIMESTAMP DEFAULT NOW(),
    analyzed_at     TIMESTAMP
);

-- ===== MADDELER =====
CREATE TABLE clauses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id     UUID REFERENCES contracts(id) ON DELETE CASCADE,
    sequence_no     INTEGER NOT NULL,
    original_text   TEXT NOT NULL,
    category        VARCHAR(100),                        -- gizlilik, tazminat, fesih, vb.
    confidence_score FLOAT,                              -- 0.0 - 1.0
    status          VARCHAR(50) DEFAULT 'draft',         -- draft|in_review|approved|rejected
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ===== RİSK DEĞERLENDİRMELERİ =====
CREATE TABLE risk_assessments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clause_id       UUID REFERENCES clauses(id) ON DELETE CASCADE,
    risk_level      VARCHAR(20) NOT NULL,                -- low | medium | high
    commercial_score FLOAT,
    legal_score     FLOAT,
    rationale       TEXT NOT NULL,                        -- Risk gerekçesi
    policy_compliance BOOLEAN,                           -- Playbook uyumlu mu?
    cross_validated BOOLEAN DEFAULT FALSE,               -- Kural motoru doğruladı mı?
    assessed_at     TIMESTAMP DEFAULT NOW()
);

-- ===== REVİZYON ÖNERİLERİ =====
CREATE TABLE revisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clause_id       UUID REFERENCES clauses(id) ON DELETE CASCADE,
    suggested_text  TEXT NOT NULL,
    context_used    TEXT,                                 -- Kullanılan Playbook/RAG bağlamı
    diff_html       TEXT,                                 -- HTML redline çıktısı
    status          VARCHAR(50) DEFAULT 'pending',       -- pending|accepted|rejected|edited
    edited_text     TEXT,                                 -- Kullanıcı düzenlemesi varsa
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ===== ONAY KARARLARI =====
CREATE TABLE approval_decisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clause_id       UUID REFERENCES clauses(id) ON DELETE CASCADE,
    user_id         UUID REFERENCES users(id),
    decision        VARCHAR(20) NOT NULL,                -- approved | rejected | revise
    comment         TEXT,
    decided_at      TIMESTAMP DEFAULT NOW()
);

-- ===== PLAYBOOK =====
CREATE TABLE playbooks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    is_default      BOOLEAN DEFAULT FALSE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE playbook_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    playbook_id     UUID REFERENCES playbooks(id) ON DELETE CASCADE,
    rule_type       VARCHAR(50) NOT NULL,                -- acceptable|rejected|required|threshold
    content         TEXT NOT NULL,
    threshold_value FLOAT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ===== RAPORLAR =====
CREATE TABLE reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id     UUID REFERENCES contracts(id) ON DELETE CASCADE,
    report_type     VARCHAR(20) NOT NULL,                -- summary | detailed
    total_clauses   INTEGER,
    summary_data    JSONB,                               -- Risk dağılımı, karar özeti
    storage_path    VARCHAR(1000),                       -- Oluşturulan rapor dosyası yolu
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ===== DENETİM GÜNLÜĞÜ =====
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    action_type     VARCHAR(100) NOT NULL,               -- login|upload|analyze|approve|reject|...
    resource_type   VARCHAR(50),                         -- contract|clause|playbook|...
    resource_id     UUID,
    details         JSONB,
    ip_address      VARCHAR(45),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ===== EKSİK HÜKÜM TESPİTLERİ =====
CREATE TABLE missing_provisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id     UUID REFERENCES contracts(id) ON DELETE CASCADE,
    playbook_rule_id UUID REFERENCES playbook_rules(id),
    description     TEXT NOT NULL,
    detected_at     TIMESTAMP DEFAULT NOW()
);

-- ===== VEKTÖR DEPOLAMA (pgvector) =====
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE clause_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clause_id       UUID REFERENCES clauses(id) ON DELETE CASCADE,
    embedding       vector(1536),                        -- OpenAI text-embedding-3-small boyutu
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE playbook_rule_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id         UUID REFERENCES playbook_rules(id) ON DELETE CASCADE,
    embedding       vector(1536),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Vektör arama için indeks
CREATE INDEX idx_clause_embeddings ON clause_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX idx_playbook_rule_embeddings ON playbook_rule_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Performans indeksleri
CREATE INDEX idx_contracts_user ON contracts(user_id);
CREATE INDEX idx_clauses_contract ON clauses(contract_id);
CREATE INDEX idx_risk_clause ON risk_assessments(clause_id);
CREATE INDEX idx_revisions_clause ON revisions(clause_id);
CREATE INDEX idx_approvals_clause ON approval_decisions(clause_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
```

### 5.2 Redis Veri Yapısı

```
# Kullanıcı oturumu
session:{user_id}            → JWT payload (TTL: 60 dk)

# Analiz durumu (orkestrasyon state)
analysis:{contract_id}       → { status, current_step, progress_pct, started_at }

# Rate limiting
ratelimit:{user_id}:{endpoint} → counter (TTL: 1 dk)

# Playbook önbellek
playbook_cache:{playbook_id} → serialized playbook rules (TTL: 30 dk)

# Başarısız giriş sayacı
login_attempts:{email}       → counter (TTL: 5 dk, max: 3)
```

---

## 6. API Tasarımı

### 6.1 Kimlik Doğrulama

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/v1/auth/register` | Yeni kullanıcı kaydı |
| POST | `/api/v1/auth/login` | Giriş + JWT token al |
| POST | `/api/v1/auth/refresh` | Token yenileme |
| POST | `/api/v1/auth/logout` | Oturum sonlandırma |

### 6.2 Sözleşmeler

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/contracts` | Kullanıcının sözleşme listesi |
| POST | `/api/v1/contracts/upload` | Sözleşme dosyası yükleme (multipart) |
| GET | `/api/v1/contracts/{id}` | Sözleşme detayı |
| DELETE | `/api/v1/contracts/{id}` | Sözleşme silme |
| POST | `/api/v1/contracts/{id}/analyze` | Analiz başlatma (playbook_id ile) |
| GET | `/api/v1/contracts/{id}/status` | Analiz durumu sorgulama |

### 6.3 Maddeler

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/contracts/{id}/clauses` | Madde listesi (pagination) |
| GET | `/api/v1/clauses/{clauseId}` | Madde detayı + risk + revizyon |
| PATCH | `/api/v1/clauses/{clauseId}/category` | Manuel kategori düzeltme |

### 6.4 Risk & Analiz

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/contracts/{id}/risks` | Tüm maddelerin risk listesi |
| GET | `/api/v1/contracts/{id}/missing-provisions` | Eksik hüküm tespitleri |

### 6.5 Revizyon Önerileri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/clauses/{clauseId}/revisions` | Revizyon önerileri |
| PATCH | `/api/v1/revisions/{revId}` | Revizyon metnini düzenleme |
| GET | `/api/v1/clauses/{clauseId}/diff` | Redline/diff HTML çıktısı |

### 6.6 Onay Akışı

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/v1/clauses/{clauseId}/approve` | Onayla |
| POST | `/api/v1/clauses/{clauseId}/reject` | Reddet (yorum ile) |
| POST | `/api/v1/clauses/{clauseId}/revise` | Yeniden revize et |
| POST | `/api/v1/contracts/{id}/bulk-approve` | Toplu onay |
| GET | `/api/v1/clauses/{clauseId}/audit-trail` | Madde denetim izi |

### 6.7 Playbook

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/playbooks` | Playbook listesi |
| POST | `/api/v1/playbooks` | Yeni Playbook oluştur |
| GET | `/api/v1/playbooks/{id}` | Playbook detayı + kurallar |
| PUT | `/api/v1/playbooks/{id}` | Playbook güncelle |
| DELETE | `/api/v1/playbooks/{id}` | Playbook sil |
| POST | `/api/v1/playbooks/from-template` | Şablondan oluştur |

### 6.8 Rapor & Dışa Aktarım

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/contracts/{id}/report/summary` | Özet rapor JSON |
| GET | `/api/v1/contracts/{id}/report/detailed` | Detaylı rapor JSON |
| GET | `/api/v1/contracts/{id}/report/download?format=pdf` | Rapor indirme |
| GET | `/api/v1/contracts/{id}/export/docx` | Revize sözleşme DOCX |

### 6.9 Yönetici

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/v1/admin/users` | Kullanıcı listesi |
| PATCH | `/api/v1/admin/users/{id}` | Kullanıcı düzenleme |
| GET | `/api/v1/admin/config` | Sistem yapılandırması |
| PUT | `/api/v1/admin/config` | Yapılandırma güncelle |
| GET | `/api/v1/admin/audit-logs` | Güvenlik logları |

### 6.10 WebSocket

| Endpoint | Açıklama |
|----------|----------|
| `ws://host/ws/{contract_id}` | Analiz ilerleme bildirimi (gerçek zamanlı) |

**Mesaj formatı:**
```json
{
  "type": "progress",
  "step": "clause_classification",
  "progress": 45,
  "message": "Maddeler sınıflandırılıyor... (5/11)"
}
```

---

## 7. Ajan Mimarisi

### 7.1 LangGraph Orkestratör Akışı

```
                    ┌──────────────┐
                    │   BAŞLANGIÇ  │
                    │  (contract   │
                    │   uploaded)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   DOKÜMAN    │
                    │   İŞLEME    │
                    │ (PDF/DOCX → │
                    │  düz metin)  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   CLAUSE     │
                    │   AGENT      │
                    │ (Ayrıştırma +│
                    │ Sınıflandırma│
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
              ┌────►│   RISK       │
              │     │   AGENT      │
              │     │ (RAG + Risk  │
              │     │  Skorlama)   │
              │     └──────┬───────┘
              │            │
              │     ┌──────▼───────┐
              │     │  KURAL       │
              │     │  MOTORU      │
              │     │ (Çapraz      │
              │     │ Doğrulama)   │
              │     └──────┬───────┘
              │            │
              │     ┌──────▼───────┐
              │     │ NEGOTIATION  │
              │     │   AGENT      │◄─── Sadece yüksek/orta risk
              │     │ (Revizyon    │     maddeleri için çalışır
              │     │  Önerisi)    │
              │     └──────┬───────┘
              │            │
              │     ┌──────▼───────┐
              └─────┤  TAMAMLANDI  │──► Kullanıcıya bildirim
  (yeniden revize)  │  (Sonuçlar   │
                    │   kaydedildi) │
                    └──────────────┘
```

### 7.2 Ajan Detayları

#### Clause Agent (Madde Ayrıştırma ve Sınıflandırma)
- **Girdi:** Düz sözleşme metni
- **Model:** GPT-4o (Structured Output / Function Calling)
- **Prompt Stratejisi:** Few-shot örnekler + Türkçe hukuki terminoloji
- **Çıktı:** `{ clauses: [{ seq, text, category, confidence }] }`
- **Kategoriler:** gizlilik, tazminat, fesih, fikri_mülkiyet, sorumluluk_sınırlandırma, uyuşmazlık_çözümü, ödeme_koşulları, genel_hükümler, diğer
- **Eşik:** confidence < 0.7 → "belirsiz" olarak işaretle

#### Risk Agent (Politika Kontrolü ve Risk Değerlendirme)
- **Girdi:** Sınıflandırılmış maddeler + Playbook kuralları
- **RAG Akışı:**
  1. Madde metni → embedding → pgvector'da benzer Playbook kurallarını bul
  2. En yakın kurallar + madde metni → GPT-4o'ya gönder
  3. Çok boyutlu risk rubriği ile değerlendir
- **Çıktı:** `{ risk_level, commercial_score, legal_score, rationale, compliance }`
- **Çapraz Doğrulama:** Kural motoru, LLM çıktısını deterministik kurallarla kontrol eder
- **Eksik hüküm tespiti:** Playbook'taki zorunlu hükümler vs sözleşmedeki maddeler karşılaştırılır

#### Negotiation Agent (Revizyon Önerisi)
- **Girdi:** Riskli madde + Playbook bağlamı + fallback clause kütüphanesi
- **RAG Akışı:** pgvector'dan benzer onaylanmış maddeler çekilir
- **Model:** GPT-4o (temperature=0.3 → tutarlı çıktı)
- **Çıktı:** `{ suggested_text, reasoning }`
- **Diff üretimi:** `diff-match-patch` ile HTML redline oluşturulur

### 7.3 Prompt Yönetimi

Tüm promptlar `backend/app/agents/prompts/` altında ayrı dosyalarda tutulacaktır. Her prompt:
- Sistem rolü (system message)
- Bağlam enjeksiyonu (Playbook kuralları, RAG sonuçları)
- Structured Output şeması (JSON Schema / Function Calling)
- Few-shot örnekler
- Güvenlik direktifleri ("hukuki tavsiye verme, sadece analiz yap")

---

## 8. Frontend Ekran Haritası

```
┌───────────────────────────────────────────────────────────┐
│                    EKRAN HARİTASI                          │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  🔐 Giriş/Kayıt ─────────► 📊 Dashboard                  │
│                              │                            │
│              ┌───────────────┼───────────────┐            │
│              │               │               │            │
│         📁 Sözleşme     📋 Playbook     ⚙️ Ayarlar       │
│         Listesi          Yönetimi                         │
│              │               │                            │
│         📤 Yükleme      ➕ Yeni PB                        │
│              │           ✏️ Düzenle                        │
│         📄 Sözleşme                                       │
│         Detay/Analiz                                      │
│              │                                            │
│    ┌─────────┼──────────┬──────────┐                      │
│    │         │          │          │                      │
│  📝 Madde  🔴 Redline  ✅ Onay   📊 Rapor               │
│  Detay     Görünüm     Akışı     İndirme                 │
│                                                           │
│  👑 Admin Panel                                           │
│    ├── 👥 Kullanıcı Yönetimi                              │
│    └── ⚙️ Sistem Yapılandırması                           │
└───────────────────────────────────────────────────────────┘
```

### Ekran Detayları

| # | Ekran | Temel Bileşenler | Özellikler |
|---|-------|-----------------|------------|
| 1 | Giriş | E-posta/şifre formu, kayıt linki | 3 başarısız → 5dk kilit uyarısı |
| 2 | Kayıt | E-posta, ad-soyad, şifre (min 12 kar) | Validasyon kuralları |
| 3 | Dashboard | Sözleşme kartları, risk dağılımı grafik, son aktivite | İstatistik widgetlar |
| 4 | Sözleşme Listesi | Tablo: ad, durum, tarih, madde sayısı | Filtreleme, sıralama |
| 5 | Yükleme | Sürükle-bırak zone, format/boyut uyarısı | İstemci tarafı doğrulama |
| 6 | Analiz Ekranı | Sol: madde listesi (renk kodlu), Sağ: madde detay | WebSocket ilerleme barı |
| 7 | Madde Detay | Orijinal metin, kategori, risk, revizyon öneri | Düzenleme desteği |
| 8 | Redline | Yan yana diff veya satır içi diff | Renk vurgulama (yeşil/kırmızı) |
| 9 | Onay Paneli | Onayla/Reddet/Revize butonları, yorum, tarihçe | Toplu karar desteği |
| 10 | Rapor | Özet + detaylı tablo, grafikler | PDF/DOCX indirme |
| 11 | Playbook Listesi | Kart listesi, varsayılan etiket | Aktif/pasif toggle |
| 12 | Playbook Düzenle | Kural formu: tip, içerik, eşik | Dinamik kural ekleme |
| 13 | Admin: Kullanıcılar | Kullanıcı tablosu, rol atama | Hesap aktif/pasif |
| 14 | Admin: Ayarlar | Dosya limiti, oturum süresi, OCR ayarları | Ortam değişkenleri |

---

## 9. Aşama Aşama Uygulama Planı

### 🔵 AŞAMA 0: Proje Temeli Kurulumu (Tamamlandı — 2-11 Mart)

**Hedef:** Proje iskeleti, geliştirme ortamı ve temel altyapının hazırlanması.

#### Görevler:
- [x] GitHub repository oluşturma, branch stratejisi belirleme (main, develop, feature/*)
- [x] SPMP dokümanı hazırlama
- [x] Trello Kanban panosu kurulumu
- [x] Kapsam ve iş paketlerinin belirlenmesi

#### Yapılacaklar (tamamlanmamış):
- [ ] `docker-compose.yml` — PostgreSQL + pgvector, Redis, MinIO servisleri
- [ ] Backend proje iskeleti: FastAPI + SQLAlchemy + Alembic
- [ ] Frontend proje iskeleti: Next.js + Tailwind + shadcn/ui
- [ ] `.env.example` dosyası + ortam değişkenleri tanımlama
- [ ] CI pipeline: GitHub Actions (lint + test + build)
- [ ] Alembic ile ilk migration: tüm tablolar
- [ ] Seed data: varsayılan playbook, kategoriler, risk rubriği

**Çıktı:** `docker-compose up` ile tüm bileşenlerin ayağa kalktığı çalışan iskelet.

---

### 🟢 AŞAMA 1: Görev-1 — Doküman İşleme & Madde Sınıflandırma (12-27 Mart) — **DEVAM EDIYOR**

**Hedef:** Sözleşme yükleme, metin dönüşümü ve Clause Agent ile madde ayrıştırma/sınıflandırma.

#### Sprint 1.1 — Doküman İşleme Altyapısı (12-19 Mart) — ✅ TAMAMLANDI

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | MinIO client wrapper | Mert | `storage/minio_client.py` | ✅ |
| 2 | PDF → metin (PyMuPDF) | Mert | `services/document_processor.py` | ✅ |
| 3 | DOCX → metin (python-docx) | Mert | `services/document_processor.py` | ✅ |
| 4 | OCR entegrasyonu (Tesseract) | Mert | `services/ocr_service.py` | ✅ |
| 5 | Dosya format/boyut doğrulama | Mert | `utils/validators.py` | ✅ |
| 6 | Sözleşme yükleme API | Mert | `api/v1/contracts.py` | ✅ |
| 7 | Auth modülü (register, login, JWT) | Mert | `api/v1/auth.py`, `core/security.py` | ✅ |
| 8 | Frontend: Giriş/Kayıt sayfaları | Osman | `app/(auth)/login`, `register` | ✅ |
| 9 | Frontend: Dashboard iskeleti | Osman | `app/(dashboard)/page.tsx` | ✅ |
| 10 | Frontend: Dosya yükleme dropzone | Osman | `components/contract/upload-dropzone.tsx` | ✅ |
| 11 | Clause Agent prompt tasarımı | Emir | `agents/prompts/clause_prompts.py` | ✅ |
| 12 | Sınıflandırma kategorileri + örnek veri seti | Emir | `data/seed/categories.json` | ✅ |
| 13 | Backend test iskeleti (pytest) | Osman | `tests/conftest.py` | ✅ |
| 14 | Frontend test iskeleti (Playwright) | Osman | `tests/playwright.config.ts` | ✅ |

#### Sprint 1.2 — Clause Agent & Sınıflandırma (20-27 Mart) — 🟠 DEVAM EDIYOR

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | Clause Agent implementasyonu | Emir | `agents/clause_agent.py` | ✅ |
| 2 | Structured Output şeması | Emir | `agents/schemas/clause_schema.py` | ✅ |
| 3 | LangGraph orkestratör iskeleti | Emir | `agents/orchestrator.py` | ✅ |
| 4 | Analiz servis katmanı | Mert | `services/analysis_service.py` | ✅ |
| 5 | Madde kayıt API'leri | Mert | `api/v1/clauses.py` | ✅ |
| 6 | WebSocket ilerleme bildirimi | Mert | `core/websocket_manager.py`, `api/v1/ws.py` | ✅ |
| 7 | Frontend: Analiz ilerleme bileşeni | Osman | `components/analysis/analysis-progress.tsx` | ✅ |
| 8 | Frontend: Madde listesi bileşeni | Osman | `components/contract/clause-list.tsx` | ✅ |
| 9 | Unit testler: document_processor, clause_agent | Osman | `tests/unit/` | ✅ |
| 10 | SRS dokümanı güncelleme | Emir | `docs/` | ✅ |

**Aşama 1 — Gelinen Nokta (8 Nisan 2026):**

✅ **Tamamlanan:**
- Dosya yükleme (PDF/DOCX) + OCR desteği — **Çalışıyor**
- Clause Agent ile otomatik madde ayrıştırma ve sınıflandırma — **Çalışıyor**
- Sınıflandırılmış maddelerin JSON formatında API çıktısı — **Çalışıyor**
- Giriş/kayıt ve temel dashboard arayüzü — **Çalışıyor**
- Docker Compose tüm servisleri (PostgreSQL, Redis, MinIO, Backend, Frontend) — **Çalışıyor**
- Veritabanı otomatik tabloları oluşturma (`Base.metadata.create_all`) — **Çalışıyor**
- 8/8 unit testler geçiyor — ✅ **TAMAMLANDI**
- Frontend Next.js proxy backend'e bağlantısı — **Çalışıyor**
- Hata yönetimi ve validasyon (formatDate, extractApiError) — **Düzeltildi**
- Analiz endpoint'i opsiyonel playbook_id ile — **Düzeltildi**

🔴 **Bilinen Sorunlar Çözüldü:**
1. ❌ `relation "users" does not exist` — ✅ Çözüldü (Alembic migration + auto-create)
2. ❌ Frontend localhost bağlantı sorunu — ✅ Çözüldü (Next.js rewrite proxy)
3. ❌ `formatDate` RangeError — ✅ Çözüldü (null/undefined güvenli hale getirildi)
4. ❌ FastAPI validation error rendering — ✅ Çözüldü (extractApiError helper)
5. ❌ `/auth/auth/` prefix duplication — ✅ Çözüldü
6. ❌ bcrypt 5.x uyumsuzluğu — ✅ Çözüldü (pinned <5.0.0)
7. ❌ Redis conftest.py event loop — ✅ Çözüldü (function-scoped fixtures)

**Aşama 1 Çıktıları:**
- ✅ **Çalışan dosya yükleme** (PDF/DOCX) + OCR desteği
- ✅ **Clause Agent** ile otomatik madde ayrıştırma ve sınıflandırma
- ✅ **Sınıflandırılmış maddelerin** JSON formatında API çıktısı
- ✅ **Giriş/kayıt ve dashboard** arayüzü (Next.js + Tailwind)
- ✅ **8/8 birim testler** geçiyor (%90+ coverage)
- ✅ **Docker üzerinde end-to-end çalışma** (localhost:3000 ve localhost:8000)
- ✅ **Kayıt → Giriş → Sözleşme Yükleme → Analiz** tam flow çalışıyor

---

### 🟡 AŞAMA 2: Görev-2 — RAG, Politika Kontrolü & Risk Değerlendirme (28 Mart - 10 Nisan)

**Hedef:** Playbook yönetimi, RAG altyapısı ve Risk Agent ile risk analizi.

#### Sprint 2.1 — RAG & Playbook Altyapısı (28 Mart - 3 Nisan)

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | pgvector kurulumu + migration | Mert | `alembic/versions/0002_pgvector_embeddings.py` | ✅ |
| 2 | OpenAI Embedding entegrasyonu | Mert | `rag/embeddings.py` | ✅ |
| 3 | Vektör CRUD (indeksleme, arama) | Mert | `rag/vector_store.py` | ✅ |
| 4 | Anlamsal benzerlik retriever | Mert | `rag/retriever.py` | ✅ |
| 5 | Playbook CRUD servisi | Mert | `services/playbook_service.py` | ✅ |
| 6 | Playbook API uç noktaları | Mert | `api/v1/playbooks.py` | ✅ |
| 7 | Playbook güncelleme → vektör indeks yenileme | Mert | `services/playbook_service.py` | ✅ |
| 8 | Varsayılan Playbook şablonu | Emir | `data/seed/default_playbook.json` | ✅ |
| 9 | Risk değerlendirme rubriği tasarımı | Emir | `data/seed/risk_rubric.json` | ✅ |
| 10 | Risk Agent prompt tasarımı | Emir | `agents/prompts/risk_prompts.py` | ✅ |
| 11 | Frontend: Playbook yönetim ekranları | Osman | `app/(dashboard)/playbooks/` | ✅ |
| 12 | Frontend: Playbook kural editörü | Osman | `components/playbook/rule-editor.tsx` | ✅ |

#### Sprint 2.2 — Risk Agent & Entegrasyon (4-10 Nisan)

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | Risk Agent implementasyonu | Emir | `agents/risk_agent.py` | ✅ |
| 2 | Kural motoru (çapraz doğrulama) | Emir | `rules/engine.py`, `rules/validators.py` | ✅ |
| 3 | Eksik hüküm tespit mekanizması | Emir | `agents/risk_agent.py` | ✅ |
| 4 | Risk API uç noktaları | Mert | `api/v1/risks.py` | ✅ |
| 5 | Orkestratöre Risk Agent eklenmesi | Emir | `agents/orchestrator.py` | ✅ |
| 6 | Redis oturum ve durum yönetimi | Mert | `core/redis.py` | ✅ |
| 7 | Frontend: Risk sonuçları görünümü | Osman | `components/analysis/risk-summary.tsx` | ✅ |
| 8 | Frontend: Risk renk kodlaması (badge) | Osman | `components/contract/risk-badge.tsx` | ✅ |
| 9 | Frontend: Dashboard istatistikleri | Osman | `components/analysis/risk-chart.tsx` | ✅ |
| 10 | Entegrasyon testleri: analiz pipeline | Emir | `tests/test_analysis_pipeline.py`, `tests/test_rules_engine.py` | ✅ |
| 11 | SDD dokümanı ilk sürüm | — | — | ⏸️ ertelendi |

**Aşama 2 — Gelinen Nokta (21 Nisan 2026):**

✅ **Tamamlanan (Mert):**
- pgvector migration (`0002_pgvector_embeddings.py`) — `clause_embeddings`, `playbook_rule_embeddings`, `missing_provisions` tabloları oluşturuldu
- RAG altyapısı: `rag/embeddings.py`, `rag/vector_store.py`, `rag/retriever.py` — **Çalışıyor**
- Playbook CRUD + otomatik vektör indeksleme — **Çalışıyor**
- Playbook API (5 endpoint) + Risk API (2 endpoint) — **Çalışıyor**
- `router.py` güncellendi, tüm yeni router'lar bağlandı

> ⚠️ **Veritabanı migration'ını uygulamak için:**
> ```bash
> docker-compose exec backend alembic upgrade head
> ```

✅ **Tamamlanan (Emir — Sprint 2.1.9-10 + Sprint 2.2):**
- Risk rubric (`data/seed/risk_rubric.json`) — kategori ağırlıkları, tırmanma kuralları, eşik tanımları
- Risk Agent prompt şablonları (`agents/prompts/risk_prompts.py`) — madde değerlendirme + eksik hüküm tespiti
- Risk Agent (`agents/risk_agent.py`) — LLM çağrısı + çapraz doğrulama, `detect_missing_provisions`
- Kural motoru (`rules/engine.py`, `rules/validators.py`) — deterministik yüzde eşiği ve semantik eşleşme
- Orkestratör (`agents/orchestrator.py`) — Clause → embedding → Risk Agent → missing provisions pipeline
- `services/analysis_service.py` — Risk Phase entegrasyonu (Phase 2 güncellendi)
- `agents/schemas/risk_schema.py` — `RiskAgentOutput`, `MissingProvisionsOutput`
- `rules/__init__.py` — yeni paket

✅ **Tamamlanan (Osman — Sprint 2.1.11-12 + Sprint 2.2.7-10):**
- Frontend playbook ekranları: liste (`/playbooks`), yeni (`/playbooks/new`), düzenle (`/playbooks/[id]`)
- Playbook kural editörü (`components/playbook/rule-editor.tsx`) — acceptable/rejected/required/threshold
- Playbook form bileşeni (`components/playbook/playbook-form.tsx`)
- Playbook store (`stores/playbook-store.ts`)
- Risk bileşenleri: `risk-badge.tsx`, `risk-summary.tsx`, `risk-chart.tsx`
- Sözleşme detay sayfasına `RiskSummary` ve madde listesine `RiskBadge` entegrasyonu
- Dashboard'a toplu risk dağılım grafiği eklendi
- Sidebar'a "Playbook'lar" menüsü eklendi
- Tip tanımları güncellendi (`types/api.ts` — Playbook, MissingProvision, RiskAssessmentDetail)
- Entegrasyon testleri: `tests/test_analysis_pipeline.py`, `tests/test_rules_engine.py`

**Aşama 2 Çıktıları:**
- ✅ Playbook CRUD + vektörel indeksleme
- ✅ RAG ile anlamsal benzerlik araması
- ✅ Risk Agent ile risk değerlendirme (düşük/orta/yüksek)
- ✅ Kural motoru çapraz doğrulaması
- ✅ Eksik hüküm tespiti
- ✅ Dashboard'da risk dağılımı görselleştirme

---

### 🟠 AŞAMA 3: Görev-3 — Revizyon, Redline & Onay Akışı (11-24 Nisan) — **DEVAM EDİYOR**

**Hedef:** Negotiation Agent, karşılaştırmalı görünüm, onay akışı ve denetim izi.

#### Sprint 3.1 — Revizyon & Redline (11-17 Nisan)

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | Negotiation Agent implementasyonu | Emir | `agents/negotiation_agent.py` | ✅ |
| 2 | Negotiation Agent prompt tasarımı | Emir | `agents/prompts/negotiation_prompts.py` | ✅ |
| 3 | Orkestratöre Negotiation Agent ekleme | Emir | `agents/orchestrator.py` | ✅ |
| 4 | Diff/Redline üretim servisi | Emir | `utils/diff.py` | ✅ |
| 5 | Revizyon API uç noktaları | Emir | `api/v1/revisions.py` | ✅ |
| 6 | Revizyon metin düzenleme desteği | Emir | `api/v1/revisions.py` | ✅ |
| 7 | Frontend: Diff viewer (karşılaştırmalı) | Osman | `components/redline/diff-viewer.tsx` | ✅ |
| 8 | Frontend: Satır içi diff modu | Osman | `components/redline/inline-diff.tsx` | ✅ |
| 9 | Frontend: Redline ekranı | Osman | `app/(app)/contracts/[id]/redline/` | ✅ |
| 10 | Unit testler: negotiation_agent, diff | Emir | `tests/test_negotiation_agent.py` | ✅ |

#### Sprint 3.2 — Onay Akışı & Denetim İzi (18-24 Nisan)

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | Onay akışı durum makinesi (state transitions) | Emir | `services/approval_service.py` | ✅ |
| 2 | Yüksek risk → zorunlu insan onayı | Emir | `services/approval_service.py` | ✅ |
| 3 | Onay API uç noktaları | Emir | `api/v1/approvals.py` | ✅ |
| 4 | Toplu onay/red desteği | Emir | `api/v1/approvals.py` | ✅ |
| 5 | Denetim izi (audit trail) servisi | — | `services/audit_service.py` (mevcut) | ✅ |
| 6 | Yeniden değerlendirme döngüsü | Emir | `services/approval_service.py` (`promote_risky_clauses_to_review`) | ✅ |
| 7 | Frontend: Onay paneli | Osman | `components/approval/approval-panel.tsx` | ✅ |
| 8 | Frontend: Karar butonları + yorum | Osman | `components/approval/decision-buttons.tsx` | ✅ |
| 9 | Frontend: Denetim izi zaman çizelgesi | Osman | `components/approval/audit-timeline.tsx` | ✅ |
| 10 | Frontend: Madde detay ekranı birleştirme | Osman | `clause-detail-panel.tsx` (ApprovalPanel entegre edildi) | ✅ |
| 11 | Entegrasyon testleri: onay akışı | Osman | `tests/integration/test_approval_flow.py` | ⏳ |

**Aşama 3 — Gelinen Nokta (21 Nisan 2026):**

✅ **Tamamlanan (Emir — Sprint 3.1 + 3.2):**
- Negotiation Agent (`agents/negotiation_agent.py`) — medium/high maddeler için LLM tabanlı revizyon önerisi
- Negotiation Agent prompt şablonları (`agents/prompts/negotiation_prompts.py`)
- Diff servisi (`utils/diff.py`) — kelime bazlı HTML diff, `similarity_ratio`
- Orkestratör Phase 3 güncellendi — Risk → MissingProvisions → Negotiation sıralaması
- Revizyon servisi (`services/revision_service.py`) — list, accept, reject, edit
- Revizyon API (`api/v1/revisions.py`) — 5 endpoint, `router.py`'ye bağlandı
- Onay servisi (`services/approval_service.py`) — state machine, bulk decide, `promote_risky_clauses_to_review`
- Onay API (`api/v1/approvals.py`) — 3 endpoint, `router.py`'ye bağlandı
- `analysis_service.py` güncellendi — analiz sonunda medium/high maddeler otomatik `in_review` durumuna alınıyor
- `agents/schemas/negotiation_schema.py`
- Unit testler: `tests/test_negotiation_agent.py` (Negotiation Agent + diff utility)

✅ **Tamamlanan (Osman — Sprint 3.1.7-9 + 3.2.7-10):**
- `components/redline/diff-viewer.tsx` — HTML diff renderer
- `components/redline/inline-diff.tsx` — madde inline diff toggle
- `components/redline/revision-card.tsx` — kabul/red/düzenle kartı
- `app/(app)/contracts/[id]/redline/page.tsx` — tam Redline ekranı
- `components/approval/decision-buttons.tsx` — yorum + karar butonları
- `components/approval/audit-timeline.tsx` — karar geçmişi zaman çizelgesi
- `components/approval/approval-panel.tsx` — madde onay paneli (decisions + timeline)
- `clause-detail-panel.tsx` — ApprovalPanel entegre edildi
- `contracts/[id]/page.tsx` — Redline linki eklendi
- `globals.css` — diff-del / diff-ins stilleri eklendi
- `types/api.ts` — RevisionDetail, ApprovalDecisionRecord tipleri eklendi

⏳ **Bekleyen:** Onay akışı entegrasyon testi

**Aşama 3 Çıktıları:**
- ✅ Riskli maddeler için otomatik revizyon önerisi
- ✅ Karşılaştırmalı (redline) görünüm
- ✅ Madde bazlı onay/red/revize akışı
- ✅ Denetim izi kayıtları
- ✅ Yeniden değerlendirme döngüsü

---

### 🟡 AŞAMA 4: Görev-4 — Raporlama, Dışa Aktarım & Polisaj (25 Nisan - 8 Mayıs)

**Hedef:** Rapor oluşturma, sözleşme dışa aktarımı, UAT, güvenlik, performans.

#### Sprint 4.1 — Raporlama & Dışa Aktarım (25 Nisan - 1 Mayıs) — ✅ TAMAMLANDI

| # | Görev | Sorumlu | Dosya/Modül | Durum |
|---|-------|---------|-------------|-------|
| 1 | Özet rapor oluşturma servisi | Emir | `services/report_service.py` | ✅ |
| 2 | Detaylı rapor oluşturma servisi | Emir | `services/report_service.py` | ✅ |
| 3 | Rapor PDF üretimi | Emir | `services/report_service.py` (fpdf2) | ✅ |
| 4 | Rapor DOCX üretimi | Emir | `services/report_service.py` (python-docx) | ✅ |
| 5 | Revize sözleşme DOCX dışa aktarımı | Emir | `services/export_service.py` | ✅ |
| 6 | Rapor & dışa aktarım API | Emir | `api/v1/reports.py` | ✅ |
| 7 | Frontend: Rapor ekranı | Emir | `app/(app)/contracts/[id]/report/page.tsx` | ✅ |
| 8 | Frontend: Özet rapor bileşeni | Emir | `components/reports/report-summary-card.tsx` | ✅ |
| 9 | Frontend: İndirme + dışa aktarım butonları | Emir | `contracts/[id]/page.tsx` (Rapor linki eklendi) | ✅ |
| 10 | pyproject.toml: fpdf2 bağımlılığı | Emir | `pyproject.toml` | ✅ |
| 11 | Pydantic şema: ReportGenerateRequest/Response | Emir | `schemas/report.py` | ✅ |
| 12 | API tipler: Report, ReportSummaryData | Emir | `frontend/src/types/api.ts` | ✅ |

**Aşama 4.1 — Gelinen Nokta (29 Nisan 2026):**

✅ **Tamamlanan (Emir — Sprint 4.1):**
- `services/report_service.py` — veri toplama (`_build_payload`), PDF (fpdf2) ve DOCX (python-docx) üretimi; MinIO'ya yükleme; `Report` satırı kayıt
- `services/export_service.py` — kabul edilen revizyonlar uygulanmış sözleşme DOCX üretimi; edited > accepted > original önceliği
- `api/v1/reports.py` — 4 endpoint: POST rapor oluştur, GET listele, GET indir, GET dışa aktar
- `api/v1/router.py` — reports router bağlandı
- `schemas/report.py` — `ReportGenerateRequest`, `ReportResponse`
- `pyproject.toml` — `fpdf2>=2.7.9` eklendi
- `frontend/src/types/api.ts` — `Report`, `ReportSummaryData` tipleri eklendi
- `frontend/src/app/(app)/contracts/[id]/report/page.tsx` — tam rapor ekranı
- `frontend/src/components/reports/report-summary-card.tsx` — risk mini-bar, indirme butonu
- `frontend/src/app/(app)/contracts/[id]/page.tsx` — "Rapor" linki eklendi

#### Sprint 4.2 — Güvenlik, Performans & UAT (2-8 Mayıs)

| # | Görev | Sorumlu | Dosya/Modül |
|---|-------|---------|-------------|
| 1 | Güvenlik: hesap kilitleme (3 deneme) | Mert | `services/auth_service.py` |
| 2 | Güvenlik: rate limiting | Mert | Middleware |
| 3 | Güvenlik: güvenlik logları | Mert | `services/audit_service.py` |
| 4 | Güvenlik: HTTPS yapılandırması | Mert | Docker/nginx config |
| 5 | Güvenlik: veri silme endpoint'i (KVKK) | Mert | `api/v1/auth.py` |
| 6 | Performans: Redis önbellekleme optimizasyonu | Mert | `core/redis.py` |
| 7 | Performans: DB sorgu optimizasyonu | Mert | Tüm servisler |
| 8 | Admin panel: kullanıcı yönetimi | Osman | `app/admin/users/` |
| 9 | Admin panel: sistem yapılandırması | Osman | `app/admin/config/` |
| 10 | E2E testler (Playwright) | Osman | `tests/e2e/` |
| 11 | UAT test senaryoları çalıştırma | Osman | Manuel + otomatik |
| 12 | Emniyet uyarıları ("bu hukuki tavsiye değildir") | Emir | Frontend + Backend |
| 13 | LLM çıktı doğrulama ve hallüsinasyon tespiti | Emir | `agents/`, `rules/` |
| 14 | Hata mesajları ve kullanıcı yönlendirmeleri | Osman | Tüm ekranlar |

**Aşama 4 Çıktıları:**
- ✅ Özet/detaylı rapor (PDF + DOCX)
- ✅ Revize sözleşme DOCX dışa aktarımı
- ✅ Güvenlik kontrolleri tamamlandı
- ✅ Performans optimize edildi
- ✅ UAT geçildi
- ✅ Admin paneli çalışıyor

---

### 🏁 AŞAMA 5: Final — Teslimat & Sunum (9-13 Mayıs)

| # | Görev | Sorumlu |
|---|-------|---------|
| 1 | STD (Yazılım Test Dokümanı) yazımı | Osman |
| 2 | Kullanıcı kılavuzu (USER_GUIDE.md) | Emir |
| 3 | API referans dokümanı | Mert |
| 4 | Docker imajlarının son sürüm etiketlenmesi | Mert |
| 5 | .env.example + README güncelleme | Mert |
| 6 | Final demo hazırlığı | Emir |
| 7 | Proje sunumu | Tüm Ekip |
| 8 | Kapanış raporu | Emir |

---

## 10. Test Stratejisi

### 10.1 Test Piramidi

```
         ╱╲
        ╱  ╲        E2E (Playwright)
       ╱    ╲       → 5-10 kritik senaryo
      ╱──────╲
     ╱        ╲     Entegrasyon Testleri (pytest)
    ╱          ╲    → API endpoint, DB, ajan pipeline
   ╱────────────╲
  ╱              ╲  Birim Testler (pytest + vitest)
 ╱                ╲ → Service, Agent, Utils (hedef: %60+)
╱──────────────────╲
```

### 10.2 Test Kategorileri

| Kategori | Araç | Kapsam | Hedef |
|----------|------|--------|-------|
| Birim Test (Backend) | pytest + pytest-asyncio | Service, Agent, Utils | %60+ kapsama |
| Birim Test (Frontend) | Vitest + React Testing Library | Hooks, Utils | Kritik fonksiyonlar |
| Entegrasyon Test | pytest + httpx (TestClient) | API → DB → Agent flow | Tüm API endpoint'leri |
| E2E Test | Playwright | Tam kullanıcı senaryosu | UC-01 ~ UC-10 |
| Güvenlik Test | Manuel + OWASP checklist | Auth, yetkilendirme, injection | Kritik güvenlik noktaları |
| Performans Test | locust / k6 | 5 eş zamanlı kullanıcı | API < 500ms, analiz < 120s |

### 10.3 Kritik Test Senaryoları

1. **UC-01:** Kayıt → Giriş → Token alma → Oturum yenileme → 3 başarısız → Kilit
2. **UC-02:** PDF yükleme → Metin dönüşümü → OCR tetiklenme → Hata durumu
3. **UC-03:** Ayrıştırma → Sınıflandırma → Güven skoru kontrolü → Belirsiz işaretleme
4. **UC-04:** Risk analizi → RAG arama → Kural motoru doğrulaması → Eksik hüküm
5. **UC-05:** Revizyon önerisi → Diff üretimi → Metin düzenleme
6. **UC-06:** Onay → Red → Yeniden revize → Denetim izi doğrulama
7. **UC-08:** Rapor oluşturma → PDF/DOCX indirme
8. **UC-09:** Playbook CRUD → Vektör indeks güncelleme
9. **Güvenlik:** Yetkisiz erişim → Başka kullanıcının sözleşmesine erişim denemesi
10. **Performans:** 10 sayfalık sözleşme → 120 saniye içinde analiz tamamlanması

---

## 11. CI/CD ve Dağıtım

### 11.1 CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml tetikleme: push/PR → develop, main
Adımlar:
  1. Backend:
     - Python 3.12 kurulumu
     - pip install
     - ruff lint (Python linting)
     - pytest (birim + entegrasyon)
     - coverage raporu (%60+ kontrol)
  
  2. Frontend:
     - Node 20 kurulumu
     - npm install
     - ESLint + Prettier
     - TypeScript type check
     - npm run build
  
  3. Docker:
     - docker-compose build (imaj derleme)
     - docker-compose up → sağlık kontrolü
```

### 11.2 CD Pipeline

```yaml
# .github/workflows/cd.yml tetikleme: main'e merge
Adımlar:
  1. Docker imaj build + tag (semver)
  2. Container registry'ye push
  3. docker-compose.prod.yml ile deploy
```

### 11.3 Docker Compose Servisleri

```yaml
services:
  backend:        # FastAPI (port 8000)
  frontend:       # Next.js (port 3000)
  postgres:       # PostgreSQL 16 + pgvector (port 5432)
  redis:          # Redis 7 (port 6379)
  minio:          # MinIO (port 9000/9001)
  nginx:          # Reverse proxy + HTTPS (port 80/443)
```

---

## 12. Güvenlik Kontrol Listesi

| # | Kontrol | Durum | Öncelik |
|---|---------|-------|---------|
| 1 | Şifre hash: bcrypt (min 12 karakter) | ⬜ | Kritik |
| 2 | JWT token: imzalı, TTL 60dk | ⬜ | Kritik |
| 3 | 3 başarısız giriş → 5dk hesap kilidi | ⬜ | Kritik |
| 4 | HTTPS zorunlu (tüm iletişim) | ⬜ | Kritik |
| 5 | API anahtarları ortam değişkenlerinde (.env) | ⬜ | Kritik |
| 6 | Yetkilendirme: kullanıcı sadece kendi verilerine erişir | ⬜ | Kritik |
| 7 | Input validasyon (Pydantic + Zod) | ⬜ | Yüksek |
| 8 | SQL injection koruması (SQLAlchemy ORM) | ⬜ | Yüksek |
| 9 | XSS koruması (React otomatik + CSP header) | ⬜ | Yüksek |
| 10 | Güvenlik logları (başarısız giriş, yetki ihlali) | ⬜ | Yüksek |
| 11 | Rate limiting (API endpoint'leri) | ⬜ | Orta |
| 12 | CORS yapılandırması | ⬜ | Orta |
| 13 | Veri silme endpoint'i (KVKK uyumu) | ⬜ | Orta |
| 14 | LLM'e gönderilen veri gizlilik bildirimi | ⬜ | Orta |
| 15 | Dosya yükleme: format + boyut + MIME type doğrulama | ⬜ | Orta |

---

## 13. Risk Yönetimi

| # | Risk | Olasılık | Etki | Önlem | Acil Durum Planı |
|---|------|----------|------|-------|------------------|
| 1 | OpenAI API kesintisi/yavaşlığı | Orta | Yüksek | Timeout + retry + cache | Bozulmuş mod: mevcut sonuçlara erişim sürdürülür |
| 2 | LLM halüsinasyonu (yanlış risk/sınıf) | Yüksek | Yüksek | Düşük temperature, kural motoru çapraz doğrulama | Zorunlu insan onayı eşikleri |
| 3 | Karmaşık PDF parse hatası | Orta | Orta | PyMuPDF fallback | GPT-4o Vision veya AWS Textract |
| 4 | OCR düşük doğruluk | Orta | Orta | Görüntü ön işleme | Kullanıcıya uyarı + manuel düzeltme |
| 5 | Performans sorunları (yavaş analiz) | Düşük | Orta | Redis cache, asenkron işleme | Paralel ajan çalıştırma |
| 6 | Veritabanı veri kaybı | Düşük | Kritik | Otomatik yedekleme | Yedekten geri yükleme prosedürü |
| 7 | Kullanıcı deneyimi karmaşıklığı | Orta | Orta | UX testleri, tooltip'ler | Onboarding wizard, tutorial |
| 8 | API maliyeti (OpenAI token tüketimi) | Orta | Orta | Token kullanım izleme | Batch işleme, model downgrade |

---

## 14. Ekip Görev Dağılımı

### Mustafa Emir Ceran — Proje Yönetimi & AI Koordinasyonu
- Kanban akış yönetimi, WIP limitleri, blokaj takibi
- **AI/LLM ajan tasarımı ve prompt mühendisliği**
- Orkestratör (LangGraph) akış tasarımı ve implementasyonu
- Clause Agent, Risk Agent, Negotiation Agent geliştirme
- Kural motoru tasarımı
- Risk rubriği ve Playbook şablonu tasarımı
- Paydaş iletişimi ve teslimat koordinasyonu
- Dokümanlar: SPMP, SRS, SDD katkıları

### Mert Ayrancı — Backend & RAG Geliştirme
- **FastAPI backend tüm API endpoint'leri**
- Veritabanı tasarımı ve Alembic migration'ları
- RAG altyapısı: embedding, pgvector, retriever
- MinIO dosya depolama entegrasyonu
- Redis oturum ve durum yönetimi
- Doküman işleme servisleri (PDF, DOCX, OCR)
- Güvenlik implementasyonu (auth, JWT, rate limit)
- Performans optimizasyonu
- Docker ve CI/CD yapılandırması

### Osman Gazi Atalay — Frontend & Test/QA
- **Next.js/React tüm ekranlar ve bileşenler**
- UI/UX implementasyonu (shadcn/ui, Tailwind)
- WebSocket entegrasyonu (gerçek zamanlı bildirim)
- Diff viewer (redline) bileşeni
- Birim test yazımı (backend + frontend)
- **E2E test (Playwright) senaryoları**
- UAT koordinasyonu ve yürütümü
- Hata mesajları ve kullanıcı yönlendirmeleri
- STD dokümanı hazırlığı

---

## 15. Zaman Çizelgesi

```
2 Mart ─────────── 11 Mart ─── 19 Mart ─── 27 Mart ─── 3 Nisan ─── 10 Nisan ─── 17 Nisan ─── 24 Nisan ─── 1 Mayıs ─── 8 Mayıs ─── 13 Mayıs
│                  │           │           │           │            │            │            │            │           │           │
│   AŞAMA 0        │ Sprint    │ Sprint    │ Sprint    │ Sprint     │ Sprint     │ Sprint     │ Sprint     │ Sprint    │  AŞAMA 5  │
│ Proje Temeli     │   1.1     │   1.2     │   2.1     │   2.2      │   3.1      │   3.2      │   4.1      │   4.2     │  Final    │
│ Kurulum          │ Doküman   │ Clause    │ RAG &     │ Risk       │ Revizyon   │ Onay       │ Rapor &    │ Güvenlik  │ Teslimat  │
│ SPMP             │ İşleme    │ Agent     │ Playbook  │ Agent      │ Redline    │ Akışı      │ Dışa       │ Perf.     │ Sunum     │
│                  │ Auth UI   │ Sınıfland.│           │ Kural Mot. │ Negotiation│ Audit Trail│ Aktarım    │ UAT       │           │
│                  │           │           │           │            │            │            │            │           │           │
├──── AŞAMA 0 ────►├────── AŞAMA 1 ───────►├─────── AŞAMA 2 ───────►├─────── AŞAMA 3 ───────►├─────── AŞAMA 4 ───────►├── AŞAMA 5►│
│                  │                        │                        │                        │                        │           │
│  📄 SPMP         │ 📄 SRS v1             │ 📄 SDD v1             │                        │ 📄 STD                 │ 🎤 SUNUM  │
│  Teslim          │ Teslim                │ Teslim                │                        │ Teslim                 │ FİNAL     │
```

### Kilometre Taşları

| Tarih | Kilometre Taşı | Teslimat |
|-------|----------------|----------|
| 11 Mart | Proje Başlangıcı | SPMP teslim, Kanban panosu hazır |
| 27 Mart | Görev-1 Tamamlandı | Dosya yükleme + Clause Agent çalışıyor |
| 10 Nisan | Görev-2 Tamamlandı | RAG + Risk Agent + Playbook çalışıyor |
| 24 Nisan | Görev-3 Tamamlandı | Revizyon + Redline + Onay akışı çalışıyor |
| 8 Mayıs | Ürün Hazır | Tüm özellikler, güvenlik, UAT tamamlandı |
| 13 Mayıs | Final Teslimat | Sunum + tüm dokümanlar teslim |

---

## Ek: Hızlı Başlangıç Komutları

```bash
# Repo klonlama
git clone https://github.com/emirceran23/masa.git
cd masa

# Ortam değişkenleri
cp .env.example .env
# .env dosyasını düzenle (OpenAI API key, DB credentials, vb.)

# Docker ile tüm servisleri başlat
docker-compose up -d

# Veritabanı migration
docker-compose exec backend alembic upgrade head

# Başlangıç verisi yükleme
docker-compose exec backend python scripts/seed-data.py

# Frontend geliştirme
cd frontend && npm install && npm run dev

# Backend geliştirme
cd backend && pip install -e ".[dev]" && uvicorn app.main:app --reload

# Testler
cd backend && pytest
cd frontend && npx playwright test
```

---

> **Not:** Bu plan, SPMP ve SRS dokümanlarındaki tüm gereksinimleri kapsamaktadır.
> Her sprint sonunda Kanban panosu güncellenecek ve haftalık gözden geçirme toplantılarında
> ilerleme değerlendirilecektir. WIP limitlerine uyulacak ve blokajlar anında raporlanacaktır.
