# Skillbridge
# SkillBridge - Academia-Industry Collaboration Platform

AI-powered platform connecting students, recruiters, and academicians.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m seed_data.seed
uvicorn server:app --reload