from fastapi import FastAPI

# Usage : uvicorn main:app --reload

app = FastAPI()

@app.get("/")
async def root():
    ret = "Bonjour !"
    return {"message": f"{ret}"}
