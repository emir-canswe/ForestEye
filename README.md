# 🔥 ForestEye — Orman Yangını Erken Uyarı Sistemi

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**ForestEye**, orman yangınlarını başlamadan önce tahmin etmeyi, coğrafi bilgi sistemleri (GIS) üzerinden risk bölgelerini belirlemeyi ve yetkililere çok kanallı otomatik uyarı göndermeyi hedefleyen yeni nesil bir erken uyarı platformudur.

---

## 🎯 Projenin Amacı ve Vizyonu

Mevcut yangın sistemleri genellikle yangın *başladıktan* sonra devreye girer. ForestEye ise uydu, hava durumu ve tarihsel verileri analiz ederek yangın çıkma olasılığı yüksek bölgeleri önceden (erken uyarı) tespit eder. 

**Özellikleri:**
- NASA FIRMS verileri ile aktif yangınları anlık haritalama
- OpenWeatherMap entegrasyonu ile rüzgar, sıcaklık ve nem analizi
- 0.1° x 0.1° (10km x 10km) Türkiye grid hücreleri üzerinde risk skoru hesabı
- Akıllı bildirim sistemi ile kritik bölgelerde Twilio (SMS), SendGrid (E-posta) ve Firebase (Push) uyarıları
- React + Leaflet altyapısı ile Premium Dark Mode canlı dashboard

---

## 🏗️ Sistem Mimarisi

- **Backend:** Python (FastAPI), SQLAlchemy, APScheduler, GeoAlchemy2
- **Veritabanı:** PostgreSQL + PostGIS (Coğrafi Sorgular), Redis (Caching)
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Leaflet.js
- **Veri Kaynakları:** NASA FIRMS (VIIRS_SNPP_NRT), OpenWeatherMap
- **Makine Öğrenmesi (Gelecek):** XGBoost ile modelleme (Şu an kural tabanlı uzman ağırlıklı V1 kullanılmaktadır)

---

## 🚀 Başlangıç (Kurulum)

Sistemi lokal ortamınızda ayağa kaldırmak oldukça basittir. Proje `docker-compose` kullanarak tüm bağımlılıkları otomatik çalıştırır.

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/emir-canswe/ForestEye-.git
cd yangin
```

### 2. Çevre Değişkenlerini (Environment Variables) Ayarlayın
Ana dizindeki `.env` dosyasını açıp gerekli API anahtarlarınızı yerleştirin:
```env
NASA_FIRMS_API_KEY=your_key_here
OPENWEATHERMAP_API_KEY=your_key_here
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
SENDGRID_API_KEY=your_key
FROM_EMAIL=noreply@yangin-uyari.gov.tr
```

### 3. Docker ile Sistemi Ayağa Kaldırın
```bash
docker-compose up -d --build
```
Bu komut sırasıyla Veritabanı (PostgreSQL+PostGIS), Redis, FastAPI (Backend) ve React (Frontend) konteynerlerini çalıştıracaktır.

### 4. Geliştirme Uç Noktaları
- **Frontend Dashboard:** `http://localhost:3000`
- **Backend API Docs (Swagger):** `http://localhost:8000/docs`
- **PostgreSQL:** `localhost:5432`

---

## 📂 Dizin Yapısı

```
ForestEye/
├── backend/            # FastAPI servisi, veritabanı modelleri, veri çekiciler, bildirim yöneticisi
├── frontend/           # React 18 (Vite) projesi, TailwindCSS, Leaflet.js Harita Modülleri
├── ml/                 # Makine öğrenmesi notebookları ve modelleri (Eğitim stub'ı eklendi)
├── data/               # Ham ve işlenmiş veriler (Git ignore edildi)
├── docker-compose.yml  # Tüm servislerin Docker orkestrasyonu
└── .env                # Gizli yapılandırma değişkenleri
```

---

## 🤝 Katkıda Bulunma

Geliştirici ekibi ve freelancer'lar için görev dağılımı ve projenin geri kalan Aşama planları projenin [Ana Prompt Dokümanı] baz alınarak oluşturulmuştur. PR'larınızı `main` branch'ine gönderebilirsiniz.
