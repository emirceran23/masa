# 🏛️ Multi-Agent Legal Ops

**Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü**

Bireylerin günlük yaşamlarında karşılaştıkları sözleşme ve hukuki metinleri daha anlaşılır, hızlı ve güvenli biçimde inceleyebilmesini sağlayan çok ajanlı (multi-agent) bir yapay zeka asistanı.

---

## 🎯 Ne Yapar?

- 📄 Sözleşmeleri (PDF/DOCX) madde bazında ayrıştırır
- 🔍 Kullanıcı tercihlerine göre risk analizi yapar (1-10 skor)
- 💡 Alternatif (fallback) ifade önerileri sunar
- ✅ İnsan onaylı revizyon akışı yönetir
- 📊 Risk dashboard ile görselleştirir

## 🏗️ Mimari

```
Frontend (Next.js) → FastAPI Backend → LangGraph Orkestrasyon
                                         ├── Ingestion Agent
                                         ├── Clause Agent
                                         ├── Risk Agent
                                         ├── Negotiation Agent
                                         └── Approval Agent
                                              ↕
                              PostgreSQL + pgvector │ Redis │ MinIO
```

## 🛠️ Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.12, FastAPI |
| Agent Orkestrasyon | LangGraph |
| LLM | OpenAI API (GPT-4o) |
| Veritabanı | PostgreSQL + pgvector |
| Cache | Redis |
| Object Storage | MinIO |
| Doküman İşleme | PyMuPDF, python-docx |
| Frontend | Next.js |
| CI/CD | GitHub Actions, Docker |

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- OpenAI API Key

### Kurulum

```bash
# Repo'yu klonla
git clone https://github.com/emirceran23/masa.git
cd masa

# Ortam değişkenlerini ayarla
cp .env.example .env
# .env dosyasını düzenle ve API key'leri gir

# Altyapı servislerini başlat (PostgreSQL, Redis, MinIO)
docker compose -f docker/docker-compose.yml up -d

# Backend kurulumu
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend kurulumu (ayrı terminal)
cd frontend
npm install
npm run dev
```

## 👥 Ekip

| Kişi | Rol |
|------|-----|
| Mustafa Emir Ceran | Proje Yönetimi & AI Koordinasyonu |
| Mert Ayrancı | Backend & RAG Geliştirme |
| Osman Gazi Atalay | Frontend & Test/QA |

## 📄 Lisans

Bu proje ders projesi kapsamında geliştirilmektedir.
