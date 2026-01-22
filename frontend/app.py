import streamlit as st
import requests
import json
from PIL import Image


# Configuration

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Expense Receipt System",
    page_icon="🧾",
    layout="centered"
)

# Title

st.title("🧾 Expense Receipt Management System")

st.write(
    """
    This application demonstrates:
    - Receipt upload and processing
    - OCR + categorization
    - 3-layer evaluation (automated, LLM, human-in-the-loop)
    """
)

# SECTION 1: USER FLOW – RECEIPT UPLOAD

st.divider()
st.header("👤 User: Upload Receipt")

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=["png", "jpg", "jpeg"]
)

receipt_id = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    if st.button("📤 Submit Receipt"):
        with st.spinner("Processing receipt..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                f"{BACKEND_URL}/receipts/upload",
                files=files,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                receipt_id = data["receipt_id"]

                st.success("Receipt uploaded successfully")
                st.json(data)

                # Store for later sections
                st.session_state["receipt_id"] = receipt_id
            else:
                st.error("Receipt upload failed")
                st.text(response.text)

# SECTION 2: INTERNAL – RUN EVALUATION

st.divider()
st.header("🔍 Internal: Evaluation Layer")

receipt_id = st.session_state.get("receipt_id")

if receipt_id:
    st.write(f"**Receipt ID:** {receipt_id}")

    if st.button("Run Full Evaluation"):
        with st.spinner("Running evaluation..."):

            # Demo payload (ground truth usually comes from dataset)
            payload = {
                "ground_truth": {
                    "full_text": "Uber trip receipt Rs 245",
                    "vendor_name": "Uber",
                    "total_amount": 245,
                    "currency": "INR",
                    "date": "2024-01-01"
                },
                "prediction": {
                    "raw_ocr_text": "Uber trip Rs 245",
                    "category": "Travel",
                    "total_amount": 245,
                    "currency": "INR",
                    "date": "2024-01-01"
                }
            }

            response = requests.post(
                f"{BACKEND_URL}/evaluation/run",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                st.success("Evaluation completed")
                st.json(response.json())
                st.session_state["evaluation_result"] = response.json()
            else:
                st.error("Evaluation failed")
                st.text(response.text)
else:
    st.info("Upload a receipt first to enable evaluation")

# SECTION 3: INTERNAL – HUMAN REVIEW


st.divider()
st.header("🧑‍⚖️ Internal: Human Review")

if receipt_id:
    decision = st.radio(
        "Final decision",
        ["Approve", "Reject"]
    )

    corrections = st.text_area(
        "Corrected fields (optional JSON)",
        placeholder='{"total_amount": 245.50}'
    )

    if st.button("Submit Human Review"):
        corrected_fields = None
        if corrections.strip():
            corrected_fields = json.loads(corrections)

        payload = {
            "receipt_id": receipt_id,
            "approved": decision == "Approve",
            "corrected_fields": corrected_fields,
            "reviewer_id": "human_001"
        }

        response = requests.post(
            f"{BACKEND_URL}/review/submit",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            st.success("Human review submitted")
            st.json(response.json())
        else:
            st.error("Failed to submit human review")
            st.text(response.text)
else:
    st.info("Upload and evaluate a receipt first")

# Footer

st.divider()
st.caption(
    "FastAPI Backend • OCR • Rule-based + LLM Categorization • "
    "3-Layer Evaluation • Human-in-the-loop"
)
