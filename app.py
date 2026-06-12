from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from config import GEMINI_API_KEY
from src.extractor import textExtractor
from src.prompt_engine import optimizationPrompt
from src.gemini_client import optimizedKeywords
from src.replacer import wordReplacer

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
        resume_text = textExtractor(input_path)
        prompt = optimizationPrompt(resume_text, jd_text)
        replacement_map = optimizedKeywords(prompt, GEMINI_API_KEY)

        if not replacement_map:
            raise HTTPException(status_code=500, detail="Gemini failed to generate keywords")

        wordReplacer(input_path, output_path, replacement_map)

        # return the optimized file
        return FileResponse(
            path=output_path, 
            filename=f"optimized_{resume.filename}",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
