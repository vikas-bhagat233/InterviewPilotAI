from config import model


def generate_hr_questions(resume_text):

    prompt = f"""
    Generate 10 HR interview questions
    based on this resume.

    Resume:

    {resume_text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text