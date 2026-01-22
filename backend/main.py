from fastapi import FastAPI
from backend.db import Base, engine
from backend.routes import receipts
import backend.models  # important
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(receipts.router)

@app.get("/")
def health_check():
    return {"status": "ok"}
