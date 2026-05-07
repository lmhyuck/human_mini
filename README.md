# 🌳 NearGarden (니어가든)
> **"내 손안의 작은 쉼표, 가장 가까운 도심 속 녹지를 찾아서"**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232a?style=flat-square&logo=react&logoColor=61dafb)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 프로젝트 개요 (Project Overview)
**NearGarden**은 사용자의 현재 위치를 기반으로 주변의 **근린공원 및 녹지 정보**를 빠르게 검색하고 안내해주는 웹 서비스입니다. 

도심 속에서 휴식이 필요한 순간, 멀리 나가지 않아도 내 주변에 숨겨진 공원을 찾아내어 시설 정보와 경로를 제공함으로써 현대인의 정서적 안정과 건강한 여가 생활을 돕는 것을 목적으로 합니다.

## ✨ 주요 기능 (Key Features)
- **📍 실시간 위치 기반 검색**: Geolocation API를 활용하여 현재 위치 주변의 공원을 거리순으로 나열합니다.
- **🗺️ 인터랙티브 지도**: 지도 위에 공원 위치를 마커로 표시하고, 상세 위치를 시각적으로 제공합니다.
- **ℹ️ 상세 시설 정보**: 공원 내 운동기구, 산책로, 화장실, 벤치 등 주요 편의시설 유무를 확인합니다.
- **🔍 스마트 필터링**: 주차 가능 여부, 반려동물 동반 가능 여부 등 조건에 맞는 공원을 필터링할 수 있습니다. (구현 예정)
- **⚡ 빠른 데이터 처리**: 공공데이터포털의 전국 도시공원 정보를 FastAPI를 통해 비동기로 빠르게 전달합니다.

## 🛠 기술 스택 (Tech Stack)
### **Backend**
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: PostgreSQL / SQLAlchemy (ORM)
- **Data Source**: 공공데이터포털 (전국도시공원표준데이터)

### **Frontend**
- **Library**: React.js
- **State Management**: React Context API
- **Map API**: Google Maps API / Kakao Maps API
- **Styling**: Tailwind CSS

## 📂 프로젝트 구조 (Project Structure)
```text
near-garden/
├── backend/            # FastAPI source code
│   ├── app/
│   │   ├── api/        # API Endpoints
│   │   ├── core/       # Configurations
│   │   ├── models/     # Database Models
│   │   └── schemas/    # Pydantic Schemas
│   └── main.py
├── frontend/           # React source code
│   ├── public/
│   └── src/
│       ├── components/ # Reusable UI Components
│       ├── pages/      # Page Views
│       └── services/   # API Call Logic
└── README.md
