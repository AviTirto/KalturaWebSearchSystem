import streamlit as st
from backend.utils.cloudfareR2_tools.cloudfareR2_api import download_file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit UI
st.title("Cloudflare R2 File Viewer")

# Input for file name
file_key = "Econ-301/Chapter-1-PPT.pdf"

# Button to fetch file
if st.button("Download & Render File"):
    try:
        bucket_name = os.getenv("CLOUDFARE_R2_BUCKET_NAME")
        file_content = download_file(bucket_name, file_key)
        st.download_button(label="Download PDF", data=file_content["file_data"], file_name=file_key, mime="application/pdf")


    except Exception as e:
        st.error(f"Error: {str(e)}")
