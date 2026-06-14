def optimizationPrompt(resume_text, jd_text):
    """
    Constructs the prompt to be sent to Gemini for skill-set based optimization.
    """
    prompt = f"""
ACT AS AN EXPERT CAREER COACH AND ATS (APPLICANT TRACKING SYSTEM) SPECIALIST.

TASK:
Perform a skill-set based optimization of the RESUME against the JOB DESCRIPTION (JD)
using the algorithm below. Output ONLY individual skill/keyword-level replacements
(single words or short skill phrases). DO NOT rewrite full sentences, bullet points,
or descriptions.

ALGORITHM:

STEP 1: From the RESUME, extract all skills into set S1, split into two subsets:
- Rss = Resume Soft Skills (e.g., communication, leadership, teamwork)
- Rhs = Resume Hard Skills (e.g., Python, SQL, AWS, Docker)
So S1 = Rss + Rhs

STEP 2: From the JOB DESCRIPTION, extract all skills into set S2, split into two subsets:
- Jss = JD Soft Skills
- Jhs = JD Hard Skills
So S2 = Jss + Jhs

STEP 3: Loop through each skill in S1 and compare it against S2:
- If the S1 skill is IRRELEVANT to the JD (no match or relation to anything in S2),
  mark it for removal: output value = "None".
- If the S1 skill is RELEVANT to the JD:
    - If S2 contains a more specific, modern, or higher-impact equivalent
      (e.g., resume has "Database Management" but JD specifies "PostgreSQL"),
      output that S2 skill as the replacement.
    - If the S1 skill is already the best possible match (equal to or better
      than anything in S2), do NOT include it in the output at all.

CONSTRAINTS:
- Keys must be a single skill word or short skill phrase EXACTLY as written in the RESUME
  (not a sentence or bullet point).
- Values must be a single skill word/short phrase, or "None" for removals — NEVER a
  rewritten sentence.
- Only include skills that need a CHANGE (replacement) or REMOVAL ("None"). Skills that
  are already optimal must be omitted entirely.
- Do not invent skills with no basis in the resume or JD.
- Limit to genuinely impactful changes (typically 5-15 entries).

INPUT DATA:
1. JOB DESCRIPTION:
{jd_text}

2. RESUME TEXT:
{resume_text}

OUTPUT FORMAT:
Return ONLY a valid JSON object. Do not include any introductory or concluding text.
The JSON must be a single flat object where:
- Key: The exact skill word/phrase currently in the resume (from S1).
- Value: Either the replacement skill word/phrase (from S2), or "None" if the skill
  should be removed.

Example:
{{
  "Database Management": "PostgreSQL",
  "MS Office": "None",
  "Team Player": "Cross-functional Collaboration"
}}
"""
    return prompt