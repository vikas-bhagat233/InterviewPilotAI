from config import model


def analyze_skill_gap(resume_text):

    prompt = f"""
    Analyze the resume.

    Find missing skills.

    Suggest skills needed
    for software and AI jobs.

    Resume:

    {resume_text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text