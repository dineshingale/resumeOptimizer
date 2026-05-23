def generate_optimization_prompt(resume_text, jd_text):
    """
    Constructs the prompt to be sent to Gemini.
    """
    prompt = f"""
ACT AS AN EXPERT CAREER COACH AND ATS (APPLICANT TRACKING SYSTEM) SPECIALIST.

TASK:
Analyze the provided RESUME and JOB DESCRIPTION (JD). Identify specific words or short phrases in the RESUME that can be replaced with more impactful keywords or action verbs found in the JD to improve alignment.

INPUT DATA:
1. JOB DESCRIPTION: 
{jd_text}

2. RESUME TEXT:
{resume_text}

CONSTRAINTS:
- Identify at least 5-10 strategic replacements.
- Use the exact phrasing found in the JD where appropriate.
- Maintain the original tense (e.g., if the resume says "Worked", don't replace it with "Leading").
- Ensure the replacement is a direct contextual substitute for the original word/phrase.
- DO NOT invent facts; only optimize the wording of existing experience.

OUTPUT FORMAT:
Return ONLY a valid JSON object. Do not include any introductory or concluding text.
The JSON must be a single flat object where:
- Key: The exact word or phrase currently in the resume.
- Value: The optimized replacement word or phrase.

Example:
{{
  "Managed projects": "Orchestrated end-to-end project lifecycles",
  "responsible for coding": "Developed scalable microservices"
}}
"""
    return prompt
