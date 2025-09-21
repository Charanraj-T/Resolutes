import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

def get_gemini_analysis(startup_name, extracted_text):
    """
    Analyzes startup text with Gemini Pro and returns a structured JSON object.

    Args:
        startup_name (str): The name of the startup.
        team_name (str): The name of the team.
        extracted_text (str): The combined text from uploaded documents.

    Returns:
        A dictionary with the startup analysis, or None if an error occurs.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id or not location:
        raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables must be set.")

    vertexai.init(project=project_id, location=location)

    model = GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Analyze the following information about a startup and generate a JSON object with the specified schema.
    The output MUST be a valid JSON object, without any markdown code fences or other text.

    Startup Name: {startup_name}
    
    Extracted Text from documents:
    ---
    {extracted_text}
    ---

    JSON Schema to follow:
    {{
      "startup_name": "{startup_name}",
      "summary": "A concise summary of the startup.",
      "founder_profile": {{
        "founders": [
          {{
            "name": "Founder's Name",
            "background": "Founder's relevant background and experience.",
            "commitment_level": "e.g., Full-time, Part-time",
            "capital_invested": "Amount of capital invested by the founder."
          }}
        ],
        "team_strengths": "Strengths of the founding team.",
        "red_flags": "Any red flags regarding the team."
      }},
      "problem_and_market": {{
        "problem_statement": "The problem the startup is solving.",
        "market_size": "The size of the target market.",
        "competitors": ["List of competitors"],
        "differentiator": "What makes the startup unique."
      }},
      "traction_and_financials": {{
        "revenue": "Current revenue figures.",
        "growth_rate": "Growth rate of the startup.",
        "key_metrics": ["Key performance indicators"],
        "funding_history": "History of funding rounds."
      }},
      "risk_factors": ["Potential risks for the startup"],
      "overall_investment_recommendation": "A recommendation for investment (e.g., 'High Potential', 'Needs More Data', 'Risky').",
      "confidence_score": 0.0
    }}
    """

    generation_config = GenerationConfig(
        response_mime_type="application/json",
    )

    for _ in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content(prompt, generation_config=generation_config)
            
            # Clean up the response text before parsing
            cleaned_response_text = response.text.strip()
            if cleaned_response_text.startswith("```json"):
                cleaned_response_text = cleaned_response_text[7:-3].strip()

            gemini_json = json.loads(cleaned_response_text)
            return gemini_json
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error parsing Gemini response: {e}")
            print("Retrying...")
            continue
    
    return None
