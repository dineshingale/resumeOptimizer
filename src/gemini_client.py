import google.generativeai as genai
import json
import os

def optimizedKeywords(prompt, api_key):
    # send the prompt to Gemini and parses the resulting JSON.
    # initialize the Gemini API
    genai.configure(api_key=api_key)
    
    # change the model based on reasoning needed
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        response = model.generate_content(prompt)
        
        # parse the string response into a Python dictionary
        optimization_map = json.loads(response.text)
        return optimization_map
        
    except json.JSONDecodeError:
        print("Error: Gemini returned invalid JSON.")
        return None
    except Exception as e:
        print(f"API Error: {e}")
        return None