import os
from dotenv import load_dotenv

# Primary Gemini SDK
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=API_KEY)

# Low temperature for grounded, factual answers
MODEL_NAME = "gemini-1.5-flash"


def generate_answer(prompt: str) -> str:
    """
    Sends a grounded prompt to Gemini and returns a clean text answer.
    """
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 512
            }
        )

        response = model.generate_content(prompt)

        # Handle different response shapes safely
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        # Fallback if SDK returns candidates
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()

        return "I could not generate a valid response."

    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {str(e)}")