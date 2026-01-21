# 🚀 Expense Receipt AI - Backend

The backend engine for **Expense Receipt AI**, a powerful system designed to automate expense tracking using OCR and Intelligent Categorization.

## 🌟 Features

- **OCR Extraction**: Automatically extracts text from receipt images using Tesseract OCR.
- **Hybrid Categorization**:
  - **Rule-based**: High-speed matching for known vendors and keywords.
  - **LLM-powered**: Advanced categorization using Groq (Llama-3) for complex or unknown receipts.
- **Duplicate Detection**: Smart check to prevent double-entry of expenses based on amount, vendor, and date.
- **Evaluation Ready**: Built-in hooks for accuracy testing and human-in-the-loop review.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python web framework)
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Validation**: [Pydantic](https://docs.pydantic.dev/) for data schemas
- **OCR Engine**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- **AI Engine**: [Groq Cloud](https://groq.com/) (Llama 3.1 8B)

## 📁 Directory Structure

```text
backend/
├── main.py          # Application entry point & route registration
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic data schemas for API requests/responses
├── db.py            # Database connection and session management
├── routes/          # API endpoint definitions
│   └── receipts.py  # Receipt processing and upload routes
├── services/        # Core business logic
│   ├── ocr.py            # Image processing and text extraction
│   ├── categorization.py # Hybrid rule/LLM categorization logic
│   └── duplicate_check.py # Receipt deduplication logic
└── utils/           # Helper functions (Image processing, etc.)
```

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8+
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) installed on your system.

### Environment Variables

Create a `.env` file in the root directory or set these variables in your shell:

```bash
# Required for AI categorization
export GROQ_API_KEY="your_groq_api_key_here"

# Optional: Path to Tesseract executable (if not in PATH)
export TESSERACT_CMD="/usr/local/bin/tesseract"
```

### Installation

1.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server**:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## 🔌 API Documentation

Once the server is running, you can access the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

### Key Endpoints

#### 1. Health Check
`GET /`
- Quick check if the service is up.

#### 2. Upload Receipt
`POST /receipts/upload`
- **Request**: Multipart form-data with a `file` (image).
- **Processing**:
  - Extracts text via OCR.
  - Detects duplicates.
  - Automatically categorizes the expense.
  - Saves to the SQLite database.
- **Response**:
  ```json
  {
    "receipt_id": 123,
    "status": "approved",
    "review_status": "pending"
  }
  ```

## 🧠 Categorization Logic

The system follows a tiered approach:
1. **Vendor Override**: Direct mapping for top vendors (e.g., Swiggy → Food).
2. **Keyword Rules**: Scans OCR text for specific identifiers with a confidence score.
3. **LLM Fallback**: If rules are insufficient, the text is sent to Llama-3 (via Groq) for intelligent classification.

---
*Built for the Expense Receipt AI Project.*
