from google.adk.agents import Agent

def recommend_courses(skills: str) -> list[str]:
    """
    Recommend professional courses and certifications based on a list of missing skills or career paths.
    
    Args:
        skills: A string containing missing skills or career paths (e.g., 'Docker, PyTorch').
        
    Returns:
        A list of recommended course names.
    """
    from mcp_servers.course_mcp import CourseMCP
    server = CourseMCP()
    return server.recommend_courses(skills)

skill_gap_adk_agent = Agent(
    name="SkillGapAgent",
    description="Finds missing skills and learning gaps.",
    model="gemini-2.5-flash",
    instruction="""You are an expert Technical Recruiter and Skill Gap Analyst.
Analyze the candidate's resume and identify missing skills, technologies, or knowledge gaps required for modern Software Developer, Data Scientist, and AI/ML Engineer roles.
You MUST call the `recommend_courses` tool to fetch high-quality course recommendations tailored to the missing skills you identify.
In your final output, list the missing skills clearly and display the recommended courses returned by the tool in a beautiful, structured markdown list. Include a short description for each course.""",
    tools=[recommend_courses]
)