# 🚀 Expense Receipt AI

A powerful system designed to automate expense tracking using OCR (Tesseract) and Intelligent Categorization (Llama 3.1). This project consists of a **FastAPI Backend** and a **Streamlit Frontend**.

## 🌟 Features

- **Automated Text Extraction**: Extracts text from receipt images using OCR.
- **Smart Categorization**: A hybrid approach using rule-based logic and LLM-powered (Groq/Llama-3) classification.
- **Interactive Web UI**: A clean, modern interface built with Streamlit for uploading receipts and viewing results.
- **Duplicate Detection**: Smart check to prevent double-entry of expenses.

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Frontend**: [Streamlit](https://streamlit.io/) (Data app framework)
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/)
- **OCR Engine**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- **AI Engine**: [Groq Cloud](https://groq.com/) (Llama 3.1 8B)

## 📁 Directory Structure

```text
├── backend/            # FastAPI Backend
│   ├── main.py         # Application entry point
│   ├── models.py       # Database models
│   ├── routes/         # API endpoints
│   └── services/       # OCR & Categorization logic
├── frontend/           # Streamlit Frontend
│   └── app.py          # Main frontend application
└── data/               # Local database & storage
```

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8+
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html) installed on your system.

### Installation

1.  **Clone the repository and enter directory**:
    ```bash
    cd expense-receipt-ai
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables**:
    Create a `.env` file in the root directory:
    ```bash
    GROQ_API_KEY="your_groq_api_key_here"
    ```

### 🚀 Running the Application

To run the full application, you need to start both the backend and frontend in separate terminals.

#### Terminal 1: Backend Server
```bash
python -m uvicorn backend.main:app --reload
```
The FastAPI server will start at `http://127.0.0.1:8000`.

#### Terminal 2: Frontend App
```bash
streamlit run frontend/app.py
```
The Streamlit interface will open in your browser (usually at `http://127.0.0.1:8501`).

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
