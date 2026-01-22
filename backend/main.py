from fastapi import FastAPI

from backend.routes import receipts
from backend.routes import evaluation
from backend.routes import review
from dotenv import load_dotenv
load_dotenv()

from backend.db import Base, engine
import backend.models  # IMPORTANT: ensures tables are registered

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Receipt Backend")

# Health check
@app.get("/")
def health():
    return {"status": "ok"}

# Register routers
app.include_router(receipts.router)
app.include_router(evaluation.router)
app.include_router(review.router)
