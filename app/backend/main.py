from fastapi import FastAPI

app = FastAPI(
    title="Daily Diary",
    description="Ежедневник для ваших планов",
    version="1.0",
)



# ===== Проверка =====
@app.get("/")
async def root():
    return {"message": "Hello Daily Diary"}
