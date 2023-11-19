# Penser à avoir uvicorn dans le PATH
cd /opt/git/pijoule/fastapi/
uvicorn main:app --reload --host 0.0.0.0
cd -