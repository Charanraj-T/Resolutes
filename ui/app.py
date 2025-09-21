import streamlit as st
import json
from dotenv import load_dotenv
from utils.vision_client import process_files
from utils.gemini_client import get_gemini_analysis
from utils.db import save_startup_data
import requests

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

                    st.session_state.gemini_json = gemini_json

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    if 'gemini_json' in st.session_state:
                        del st.session_state.gemini_json

    if 'gemini_json' in st.session_state:
        st.subheader("Generated Startup Analysis (JSON)")
        st.json(st.session_state.gemini_json)

    if st.button("Get ADK Analysis"):
        with st.spinner("ADK Agent is analyzing the data..."):
            try:
                # prompt = f"Analyze the following startup data and provide a detailed evaluation:\n\n{json.dumps(st.session_state.gemini_json, indent=2)}"
                prompt = f"Hello, what can you do?"
                user_id = "test_user"
                session_id = "adk_session"
                base_url = "http://localhost:8000"
                agent_name = "adk" 

                session_url = f"{base_url}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
                run_url = f"{base_url}/run"

                # Step 1: Create session
                requests.post(session_url).raise_for_status()

                # Step 2: Send prompt to /run
                payload = {
                    "appName": agent_name,
                    "userId": user_id,
                    "sessionId": session_id,
                    "newMessage": {
                        "parts": [{"text": prompt}],
                        "role": "user"
                    },
                    "streaming": False
                }
                
                run_response = requests.post(run_url, json=payload)
                run_response.raise_for_status()
                
                # Step 3: Delete session
                requests.delete(session_url).raise_for_status()

                # Process the response
                response_data = run_response.json()
                
                st.write("Raw ADK Agent Response:")
                st.json(response_data)
                # Extract the text from the last part of the response
                last_block = response_data[-1]
                adk_response = last_block.get("content", {}).get("parts", [{}])[0].get("text", "")

                st.toast("ADK Agent analysis complete!")
                st.subheader("ADK Agent Analysis")
                st.markdown(adk_response)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the ADK Agent server. Please ensure it is running. Error: {e}")
            except Exception as e:
                st.error(f"An error occurred with the ADK Agent: {e}")


if __name__ == "__main__":
    main()