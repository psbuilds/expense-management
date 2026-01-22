import streamlit as st
import requests
from PIL import Image
import io

# ---------------------------
# Configuration
# ---------------------------

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Expense Receipt Manager",
    page_icon="🧾",
    layout="centered"
)

# ---------------------------
# UI Header
# ---------------------------

st.title("🧾 Expense Receipt Management System")
st.write(
    """
    This interface allows you to upload a receipt image.
    The backend will:
    - Extract text using OCR
    - Categorize the expense (rules + LLM fallback)
    - Detect duplicates
    - Store the result in the database
    """
)

st.divider()

# ---------------------------
# File Upload
# ---------------------------

uploaded_file = st.file_uploader(
    "Upload a receipt image",
    type=["png", "jpg", "jpeg"]
)

# ---------------------------
# Preview + Submit
# ---------------------------

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Receipt", use_column_width=True)
    except Exception:
        st.warning("Unable to preview image.")

    st.divider()

    if st.button("📤 Submit Receipt"):
        with st.spinner("Processing receipt..."):
            try:
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

                    st.success("✅ Receipt processed successfully")

                    st.subheader("📄 Backend Response")
                    st.json(data)

                else:
                    st.error(
                        f"❌ Backend error ({response.status_code})"
                    )
                    st.text(response.text)

            except Exception as e:
                st.error("❌ Failed to connect to backend")
                st.exception(e)

# ---------------------------
# Footer
# ---------------------------

st.divider()
st.caption(
    "FastAPI Backend • OCR • Rule-based + LLM Categorization • Evaluation-ready"
)
