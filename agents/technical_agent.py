from config import model


def generate_technical_questions(
        resume_text
):

    prompt = f"""
    Generate 15 technical interview
    questions from the skills
    mentioned in the resume.

    Resume:

    {resume_text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text