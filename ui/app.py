import streamlit as st
import json
import base64
from dotenv import load_dotenv
from utils.vision_client import process_files
from utils.gemini_client import get_gemini_analysis
from utils.db import save_startup_data, save_adk_analysis
try:
    from utils.pdf_generator import generate_investment_report_pdf
    PDF_AVAILABLE = True
except ImportError:
    from utils.simple_report import simple_pdf_fallback
    PDF_AVAILABLE = False
    print("⚠️  ReportLab not available. Using simple text reports.")
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
        if not startup_name:
            st.warning("Please enter a startup name before requesting ADK analysis.")
        else:
            with st.spinner("ADK Agent is analyzing the data..."):
                try:
                    prompt = f"Research and analyze startup: {startup_name}\n\nPlease conduct comprehensive research and provide detailed structured analysis covering:\n1. Team evaluation (founder background, completeness, commitment)\n2. Market analysis (TAM/SAM, competition, growth dynamics)\n3. Product assessment (MVP stage, differentiators, technical feasibility)\n4. Traction review (revenue metrics, engagement signals, hiring velocity)\n5. Financial analysis (funding status, unit economics, risk factors)\n6. Competitive landscape (key competitors, market positioning, benchmarks)\n7. Research insights and investment recommendations\n\nProvide structured JSON responses for each analysis domain."
                    
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

                    # Save ADK analysis to MongoDB
                    st.write("Saving ADK analysis to database...")
                    save_result = save_adk_analysis(startup_name, adk_response)
                    
                    if save_result:
                        if save_result == "updated":
                            st.success("ADK analysis updated in existing startup record!")
                        else:
                            st.success(f"ADK analysis saved to database with ID: {save_result}")
                    else:
                        st.warning("ADK analysis completed but failed to save to database.")

                    st.toast("ADK Agent analysis complete!")
                    st.subheader("ADK Agent Analysis")
                    
                    # Try to display as JSON if possible, otherwise as text
                    try:
                        if adk_response.strip().startswith('{') or adk_response.strip().startswith('['):
                            import json
                            parsed_response = json.loads(adk_response)
                            st.json(parsed_response)
                        else:
                            st.text(adk_response)
                    except json.JSONDecodeError:
                        st.text(adk_response)
                    
                    # Generate PDF Report
                    st.subheader("📄 Investment Report")
                    
                    try:
                        # Generate the PDF or text report
                        with st.spinner("Generating professional investment report..."):
                            if PDF_AVAILABLE:
                                pdf_buffer = generate_investment_report_pdf(adk_response, startup_name)
                                file_extension = ".pdf"
                                mime_type = "application/pdf"
                                report_type = "PDF Report"
                            else:
                                pdf_buffer = simple_pdf_fallback(adk_response, startup_name)
                                file_extension = ".txt"
                                mime_type = "text/plain"
                                report_type = "Text Report"
                            
                        # Create download button
                        pdf_bytes = pdf_buffer.getvalue()
                        
                        st.download_button(
                            label=f"📥 Download Investment Report ({report_type})",
                            data=pdf_bytes,
                            file_name=f"{startup_name}_Investment_Analysis_Report{file_extension}",
                            mime=mime_type,
                            key="download_report"
                        )
                        
                        if PDF_AVAILABLE:
                            # Display PDF in browser
                            st.subheader("📊 Report Preview")
                            b64_pdf = base64.b64encode(pdf_bytes).decode()
                            
                            # Create an iframe to display the PDF
                            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)
                        else:
                            # Display text report
                            st.subheader("📊 Report Preview")
                            st.text_area(
                                "Report Content:",
                                value=pdf_bytes.decode('utf-8'),
                                height=400,
                                disabled=True
                            )
                            st.info("💡 Install ReportLab (`pip install reportlab`) for professional PDF reports!")
                        
                        st.success(f"✅ Professional {report_type.lower()} generated successfully!")
                        
                    except Exception as pdf_error:
                        st.error(f"Failed to generate report: {pdf_error}")
                        st.info("The analysis was completed successfully, but report generation encountered an issue.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to the ADK Agent server. Please ensure it is running. Error: {e}")
                except Exception as e:
                    st.error(f"An error occurred with the ADK Agent: {e}")


if __name__ == "__main__":
    main()