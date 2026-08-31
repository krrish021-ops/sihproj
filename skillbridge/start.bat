@echo off
echo Starting SkillBridge...

echo Starting Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python -m seed_data.seed
start cmd /k "uvicorn server:app --reload --port 8000"

echo Starting Frontend...
cd ../frontend
npm install
start cmd /k "npm run dev"

echo SkillBridge is running!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:8000