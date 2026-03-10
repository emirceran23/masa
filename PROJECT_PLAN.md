# 🚀 Multi-Agent Legal Ops — Proje Başlangıç Planı

> **Proje:** Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü  
> **Tarih:** 10 Mart 2026  
> **Durum:** Başlangıç Fazı

---

## 📐 Proje Mimarisi (Üst Düzey)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                           │
│  (Sözleşme Yükleme • Risk Dashboard • Redline Görünüm • Onay)  │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
┌────────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Ingestion│  │  Clause  │  │   Risk   │  │ Negotiation  │   │
│  │  Agent   │→ │  Agent   │→ │  Agent   │→ │   Agent      │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│                    ↕ LangGraph Orkestrasyon                      │
├─────────────────────────────────────────────────────────────────┤
│  OpenAI API │ PostgreSQL+pgvector │ Redis │ MinIO               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Hedef Dizin Yapısı

```
masa/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Ayarlar ve env variables
│   │   ├── models/             # SQLAlchemy / Pydantic modelleri
│   │   │   ├── contract.py
│   │   │   ├── clause.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── api/                # API route'ları
│   │   │   ├── v1/
│   │   │   │   ├── contracts.py
│   │   │   │   ├── reviews.py
│   │   │   │   └── approvals.py
│   │   │   └── deps.py
│   │   ├── agents/             # LangGraph Agent'ları
│   │   │   ├── orchestrator.py # Ana LangGraph akışı
│   │   │   ├── ingestion.py    # Doküman parse & OCR
│   │   │   ├── clause.py       # Madde sınıflandırma
│   │   │   ├── risk.py         # Risk skorlama
│   │   │   ├── negotiation.py  # Revizyon önerisi üretme
│   │   │   └── approval.py     # Onay akışı
│   │   ├── services/           # İş mantığı servisleri
│   │   │   ├── document_parser.py
│   │   │   ├── rag_service.py
│   │   │   ├── rule_engine.py
│   │   │   └── storage.py
│   │   ├── db/                 # Veritabanı
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   └── core/               # Yardımcı modüller
│   │       ├── security.py
│   │       └── logging.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   ├── package.json
│   └── Dockerfile
├── docker/                     # Docker Compose & infra
│   └── docker-compose.yml
├── docs/                       # Proje dokümanları
│   ├── project_spmp.tex
│   ├── srs/
│   ├── sdd/
│   └── std/
├── data/                       # Test verileri & playbook'lar
│   ├── sample_contracts/
│   └── playbooks/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── README.md
└── PROJECT_PLAN.md
```

---

## 📅 Sprint Planı (Zaman Çizelgesi ile Uyumlu)

### 🔷 Faz 0: Proje Altyapı Kurulumu (10-13 Mart 2026)
**Hedef:** Geliştirme ortamını hazırla, temel iskelet yapısını oluştur.

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 0.1 | Repo yapısını oluştur (dizinler, .gitignore, README) | Emir | ⬜ |
| 0.2 | Backend iskelet: FastAPI app + pyproject.toml + Dockerfile | Mert | ⬜ |
| 0.3 | Frontend iskelet: Next.js proje oluşturma | Osman | ⬜ |
| 0.4 | Docker Compose: PostgreSQL + Redis + MinIO | Mert | ⬜ |
| 0.5 | GitHub Actions CI pipeline (lint + test) | Emir | ⬜ |
| 0.6 | .env.example ve config yapısı | Mert | ⬜ |
| 0.7 | Kanban board kurulumu (GitHub Projects) | Emir | ⬜ |

---

### 🔷 Faz 1: Görev-1 — Veri Alımı ve Madde Sınıflandırma (14-25 Mart 2026)
**Hedef:** Sözleşme yükleme → metin çıkarma → madde bazında ayrıştırma pipeline'ı.

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 1.1 | PDF parse servisi (PyMuPDF) | Mert | ⬜ |
| 1.2 | DOCX parse servisi (python-docx) | Mert | ⬜ |
| 1.3 | Upload API endpoint'i (FastAPI + MinIO) | Mert | ⬜ |
| 1.4 | Clause Agent: LLM ile madde sınıflandırma | Emir | ⬜ |
| 1.5 | Sınıflandırma kategorileri tanımlama (gizlilik, tazminat, fesih vb.) | Emir | ⬜ |
| 1.6 | DB modelleri: Contract, Clause tabloları | Mert | ⬜ |
| 1.7 | Birim testleri: parser + clause agent | Mert/Emir | ⬜ |
| 1.8 | SRS dokümanı hazırlığı başlangıç | Emir | ⬜ |

---

### 🔷 Faz 2: Görev-2 — Politika Kontrolü ve Risk Skorlaması (26 Mart - 8 Nisan 2026)
**Hedef:** RAG altyapısı + risk analiz ajanı + kural motoru.

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 2.1 | pgvector kurulumu ve embedding pipeline | Mert | ⬜ |
| 2.2 | Playbook/politika dokümanlarını vektör DB'ye yükleme | Emir | ⬜ |
| 2.3 | RAG servisini oluşturma (similarity search) | Mert | ⬜ |
| 2.4 | Risk Agent: LLM + RAG ile risk skorlama (1-10) | Emir | ⬜ |
| 2.5 | Kural Motoru (deterministik if/else kontrolleri) | Mert | ⬜ |
| 2.6 | LLM + kural motoru çapraz doğrulama mekanizması | Emir/Mert | ⬜ |
| 2.7 | Risk raporu çıktı formatı (JSON schema) | Emir | ⬜ |
| 2.8 | SRS dokümanı finalizasyonu (1 Nisan teslim) | Emir | ⬜ |

---

### 🔷 Faz 3: Görev-3 — Revizyon ve Onay Akışı (9-22 Nisan 2026)
**Hedef:** Redline üretimi, onay state machine, human-in-the-loop.

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 3.1 | LangGraph orkestrasyon akışı tasarımı | Emir | ⬜ |
| 3.2 | Negotiation Agent: clause-bazlı revizyon önerisi | Emir | ⬜ |
| 3.3 | Fallback clause kütüphanesi (pgvector) | Mert | ⬜ |
| 3.4 | Approval state machine (Taslak→İnceleme→Onay→Red) | Mert | ⬜ |
| 3.5 | Redline çıktı üretimi (python-docx) | Mert | ⬜ |
| 3.6 | Audit trail / log sistemi (PostgreSQL) | Mert | ⬜ |
| 3.7 | Redis session/state yönetimi | Mert | ⬜ |
| 3.8 | SDD dokümanı hazırlanması (22 Nisan teslim) | Emir | ⬜ |

---

### 🔷 Faz 4: Görev-4 — Arayüz Geliştirme ve Entegrasyon (14 Nisan - 8 Mayıs 2026)
**Hedef:** Web dashboard, uçtan uca test, final entegrasyon.  
*Not: Frontend, Faz 3 ile paralel başlar.*

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 4.1 | Sözleşme yükleme ekranı | Osman | ⬜ |
| 4.2 | Risk dashboard (skor + kategori görünümü) | Osman | ⬜ |
| 4.3 | Redline/diff görünüm bileşeni | Osman | ⬜ |
| 4.4 | Onay akışı UI (kabul/red butonları) | Osman | ⬜ |
| 4.5 | API entegrasyonu (backend ↔ frontend) | Osman/Mert | ⬜ |
| 4.6 | Responsive tasarım ve UX iyileştirmeleri | Osman | ⬜ |
| 4.7 | E2E testler | Osman | ⬜ |

---

### 🔷 Faz 5: Test ve Teslim (9-13 Mayıs 2026)
**Hedef:** STD dokümanı, son testler, final sunum.

| # | Görev | Sorumlu | Durum |
|---|-------|---------|-------|
| 5.1 | UAT (User Acceptance Testing) | Osman | ⬜ |
| 5.2 | Performans ve güvenlik testleri | Mert | ⬜ |
| 5.3 | STD dokümanı hazırlığı | Emir | ⬜ |
| 5.4 | API dokümantasyonu (Swagger/OpenAPI) | Mert | ⬜ |
| 5.5 | Demo hazırlığı ve final sunum provası | Hepsi | ⬜ |
| 5.6 | STD teslimi ve final sunum (13 Mayıs) | Hepsi | ⬜ |

---

## 🔑 Kritik Kararlar ve Notlar

### Teknoloji Kararları
- **Python 3.12** — Backend dili
- **FastAPI** — API framework
- **LangGraph** — Agent orkestrasyon
- **OpenAI API (GPT-4o)** — LLM katmanı
- **PostgreSQL + pgvector** — Ana DB + vektör arama
- **Redis** — Cache, session, rate limiting
- **MinIO** — Object storage (sözleşme dosyaları)
- **Next.js** — Frontend framework
- **Docker + GitHub Actions** — CI/CD

### WIP Limitleri (Kanban)
- **Yapılacak:** ∞ (backlog)
- **Devam Eden:** 3 (kişi başı 1)
- **Doğrulama:** 2
- **Tamamlandı:** ∞

### Öncelik Sırası
1. Backend altyapı + Doküman parse (Görev 1) — **En yüksek**
2. RAG + Risk skorlama (Görev 2) — **Yüksek**
3. Revizyon + Onay akışı (Görev 3) — **Yüksek**
4. Frontend (Görev 4) — **Orta** (backend mock'ları ile paralel başlayabilir)

---

## ⚡ Hemen Yapılacaklar (Bugün - 10 Mart 2026)

1. ✅ Proje planı oluşturuldu (bu dosya)
2. ⬜ Repo yapısını oluştur (.gitignore, README, dizinler)
3. ⬜ Backend iskelet kurulumu (FastAPI + pyproject.toml)
4. ⬜ Docker Compose hazırlığı (PostgreSQL + Redis)
5. ⬜ GitHub Projects'te Kanban board oluştur
6. ⬜ .env.example hazırla
