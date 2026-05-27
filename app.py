from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from config import GEMINI_API_KEY
from src.extractor import extract_text_from_docx
from src.prompt_engine import generate_optimization_prompt
from src.gemini_client import get_optimized_keywords
from src.replacer import replace_keywords_in_docx

app = FastAPI()

@app.post("/optimize-resume")
async def optimize_resume(
    resume: UploadFile = File(...), 
    jd_text: str = Form(...)
):
    # create a unique session ID and temporary directory
    session_id = str(uuid.uuid4())
    temp_dir = f"temp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    
    input_path = f"{temp_dir}/input.docx"
    output_path = f"{temp_dir}/optimized.docx"

    try:
        # save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # run your optimization pipeline
        resume_text = extract_text_from_docx(input_path)
        prompt = generate_optimization_prompt(resume_text, jd_text)
        replacement_map = get_optimized_keywords(prompt, GEMINI_API_KEY)

        if not replacement_map:
            raise HTTPException(status_code=500, detail="Gemini failed to generate keywords")

        replace_keywords_in_docx(input_path, output_path, replacement_map)

        # return the optimized file
        return FileResponse(
            path=output_path, 
            filename=f"optimized_{resume.filename}",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
