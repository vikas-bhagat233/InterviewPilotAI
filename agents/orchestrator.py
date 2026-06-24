import concurrent.futures
from agents.resume_agent import analyze_resume
from agents.skill_gap_agent import analyze_skill_gap
from agents.hr_agent import generate_hr_questions
from agents.technical_agent import generate_technical_questions
from agents.roadmap_agent import generate_roadmap
from agents.fallback import generate_fallback_results

def run_agents(resume_text):
    """
    Runs all 5 standard agents in parallel using a ThreadPoolExecutor.
    If the Gemini API hits a rate limit or quota exhaustion (like the 20 requests/day free tier limit),
    it gracefully falls back to the high-fidelity offline synthesis engine.
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_resume = executor.submit(analyze_resume, resume_text)
            future_skill = executor.submit(analyze_skill_gap, resume_text)
            future_hr = executor.submit(generate_hr_questions, resume_text)
            future_tech = executor.submit(generate_technical_questions, resume_text)
            future_roadmap = executor.submit(generate_roadmap, resume_text)
            
            return {
                "resume_analysis": future_resume.result(),
                "skill_gap": future_skill.result(),
                "hr_questions": future_hr.result(),
                "technical_questions": future_tech.result(),
                "roadmap": future_roadmap.result()
            }
    except Exception as e:
        print(f"[WARNING] Standard Orchestrator hit an error: {e}. Activating High-Fidelity Fallback Engine.")
        return generate_fallback_results(resume_text)