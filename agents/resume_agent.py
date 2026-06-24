from config import model


def analyze_resume(resume_text):

    prompt = f"""
    Analyze this resume.

    Give:

    1. Resume Score out of 100
    2. Strengths
    3. Weaknesses
    4. Suggestions

    Resume:

    {resume_text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text