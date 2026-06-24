from config import model


def generate_roadmap(resume_text):

    prompt = f"""
    Create a 30 day roadmap.

    Include:

    Week 1
    Week 2
    Week 3
    Week 4

    Resume:

    {resume_text}
    """

    response = model.generate_content(
        prompt
    )

    return response.text