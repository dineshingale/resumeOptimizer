# main.py
import os
from config import GEMINI_API_KEY, INPUT_RESUME, INPUT_JD, OUTPUT_RESUME
from src.extractor import textExtractor
from src.prompt_engine import optimizationPrompt
from src.gemini_client import optimizedKeywords
from src.replacer import wordReplacer

def main():
    print("1. Starting Resume Optimization...")

    # read the JD
    if not os.path.exists(INPUT_JD):
        print(f"Error: {INPUT_JD} not found.")
        return
    with open(INPUT_JD, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # extract Text from Resume
    print("2. Extracting text from resume...")
    resume_text = textExtractor(INPUT_RESUME)
    if not resume_text:
        return

    # generate Prompt & Call Gemini
    print("3. Consulting Gemini for optimization...")
    prompt = optimizationPrompt(resume_text, jd_text)
    replacement_map = optimizedKeywords(prompt, GEMINI_API_KEY)

    if not replacement_map:
        print("Failed to get optimization keywords.")
        return

    print(f"4. Received {len(replacement_map)} optimizations from Gemini.")
    for old, new in replacement_map.items():
        if new == "None":
            continue
        print(f"   - Replacing '{old}' with '{new}'")

    # apply Replacements to Docx
    print("5. Generating optimized .docx file...")
    success = wordReplacer(INPUT_RESUME, OUTPUT_RESUME, replacement_map)

    if success:
        print(f"\n Success! Optimized resume saved at: {OUTPUT_RESUME}")
    else:
        print("Error during file generation.")

if __name__ == "__main__":
    main()