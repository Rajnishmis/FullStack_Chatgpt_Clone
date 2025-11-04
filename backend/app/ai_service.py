# import google.generativeai as genai
# import os
# # Configure Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# def generate_ai_response(user_message: str):
#     """
#     Sends the user message to Gemini and returns the generated response.
#     """
#     try:
#         client = genai.Client()

#         # ✅ Use the latest stable free model
#         model_name = "models/gemini-2.5-flash-live-preview"

#         # ✅ Generate response
#         response = client.models.generate_content(
#             model=model_name,
#             contents=user_message
#         )

#         return response.text
#     except Exception as e:
#         return f"Error generating response: {e}"

import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_response(user_message: str):
    """
    Sends the user message to Gemini and returns the generated response.
    """
    try:
        # Create the model (choose one of the free models)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Send message to Gemini
        response = model.generate_content(user_message)

        # Extract text response
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"
