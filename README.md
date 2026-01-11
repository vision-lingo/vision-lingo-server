# 비전링고 백엔드 서버

비전 프로 기반 인공와우 재활 훈련 앱을 위한 백엔드 API 서버입니다.  
FastAPI와 MySQL을 사용합니다.

## 역할
- 스테이지 기반 훈련 지표 수집 및 조회

## 로컬 실행

```bash
uv sync
uv run uvicorn app.main:app --reload