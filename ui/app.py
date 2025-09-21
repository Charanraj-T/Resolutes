import streamlit as st
import json
from dotenv import load_dotenv
from utils.vision_client import process_files
from utils.gemini_client import get_gemini_analysis
from utils.db import save_startup_data

# Load environment variables from .env file
load_dotenv()

def main():
    st.set_page_config(page_title="LetsVenture – Resolutes", layout="wide")
    st.title("LetsVenture – Resolutes")
    st.write("Analyze startups quickly by processing pitch decks and founder checklists.")

    startup_name = st.text_input("Startup Name")
    
    uploaded_files = st.file_uploader(
        "Upload Pitch Decks, Checklists, etc. (PDF or DOCX, up to 5 files)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if len(uploaded_files) > 5:
        st.error("You can upload a maximum of 5 files.")
        st.stop()

    if st.button("Process Startup"):
        if not startup_name or not uploaded_files:
            st.warning("Please fill in all fields and upload at least one document.")
        else:
            with st.spinner("Processing documents and analyzing startup..."):
                try:
                    # 1. Extract text from uploaded files
                    st.write("Step 1: Extracting text from documents...")
                    extracted_text = process_files(uploaded_files)
                    if not extracted_text.strip():
                        st.error("Could not extract any text from the uploaded documents. Please check the files and try again.")
                        st.stop()
                    
                    # 2. Get analysis from Gemini
                    st.write("Step 2: Analyzing text with Gemini...")
                    gemini_json = get_gemini_analysis(startup_name, extracted_text)
                    if gemini_json is None:
                        st.error("Failed to get analysis from Gemini after multiple retries. Please check the logs.")
                        st.stop()

                    # 3. Save data to MongoDB
                    st.write("Step 3: Saving data to database...")
                    inserted_id = save_startup_data(startup_name, extracted_text, gemini_json)
                    if inserted_id is None:
                        st.error("Failed to save data to the database. Please check your MongoDB connection and credentials.")
                        st.stop()

                    st.success(f"Startup analysis complete! Data saved with ID: {inserted_id}")

                    # 4. Display the JSON output
                    st.subheader("Generated Startup Analysis (JSON)")
                    st.json(gemini_json)

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()