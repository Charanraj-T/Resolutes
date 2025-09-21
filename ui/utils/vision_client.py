import os
import io
import filetype
import docx2txt
from google.cloud import vision

def get_mime_type(file_bytes):
    """Detects the mime type of a file."""
    kind = filetype.guess(file_bytes)
    if kind is None:
        return None
    return kind.mime

def extract_text_from_file(file):
    """
    Extracts text from an uploaded file (PDF or DOCX).

    Args:
        file: An uploaded file object from Streamlit.

    Returns:
        The extracted text as a string.
    """
    file_bytes = file.getvalue()
    mime_type = get_mime_type(file_bytes)

    if mime_type == 'application/pdf':
        return extract_text_from_pdf(file_bytes)
    elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
        return extract_text_from_docx(file_bytes)
    else:
        return f"Unsupported file type: {mime_type}"

def extract_text_from_pdf(file_bytes):
    """
    Extracts text from a PDF file using Google Cloud Vision API.
    """
    client = vision.ImageAnnotatorClient()
    content = file_bytes
    input_config = vision.InputConfig(
        gcs_source=None,
        content=content,
        mime_type='application/pdf'
    )
    features = [vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)]

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=features,
    )

    response = client.batch_annotate_files(requests=[request])
    
    text = ""
    for image_response in response.responses[0].responses:
        text += image_response.full_text_annotation.text
    
    return text

def extract_text_from_docx(file_bytes):
    """
    Extracts text from a DOCX file.
    """
    try:
        text = docx2txt.process(io.BytesIO(file_bytes))
        return text
    except Exception as e:
        return f"Error processing DOCX file: {e}"

def process_files(uploaded_files):
    """
    Processes a list of uploaded files and extracts text from them.
    """
    combined_text = ""
    for uploaded_file in uploaded_files:
        text = extract_text_from_file(uploaded_file)
        combined_text += text + "\n\n"
    return combined_text
