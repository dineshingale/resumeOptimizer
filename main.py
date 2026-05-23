# main.py
import os
from config import GEMINI_API_KEY, INPUT_RESUME, INPUT_JD, OUTPUT_RESUME
from src.extractor import extract_text_from_docx
from src.prompt_engine import generate_optimization_prompt
from src.gemini_client import get_optimized_keywords
from src.replacer import replace_keywords_in_docx

def main():
    print("🚀 Starting Resume Optimization...")

    # 1. Read the JD
    if not os.path.exists(INPUT_JD):
        print(f"❌ Error: {INPUT_JD} not found.")
        return
    with open(INPUT_JD, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # 2. Extract Text from Resume
    print("📄 Extracting text from resume...")
    resume_text = extract_text_from_docx(INPUT_RESUME)
    if not resume_text:
        return

    # 3. Generate Prompt & Call Gemini
    print("🧠 Consulting Gemini for optimization...")
    prompt = generate_optimization_prompt(resume_text, jd_text)
    replacement_map = get_optimized_keywords(prompt, GEMINI_API_KEY)

    if not replacement_map:
        print("❌ Failed to get optimization keywords.")
        return

    print(f"✅ Received {len(replacement_map)} optimizations from Gemini.")
    for old, new in replacement_map.items():
        print(f"   - Replacing '{old}' with '{new}'")

    # 4. Apply Replacements to Docx
    print("📝 Generating optimized .docx file...")
    success = replace_keywords_in_docx(INPUT_RESUME, OUTPUT_RESUME, replacement_map)

    if success:
        print(f"\n✨ Success! Optimized resume saved at: {OUTPUT_RESUME}")
    else:
        print("❌ Error during file generation.")

if __name__ == "__main__":
    main()
