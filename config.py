import os
from dotenv import load_dotenv

load_dotenv()

# config.py
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# File Paths
INPUT_RESUME = "data/input_resume.docx"
INPUT_JD = "data/jd.txt"
OUTPUT_RESUME = "data/output_resume.docx"
