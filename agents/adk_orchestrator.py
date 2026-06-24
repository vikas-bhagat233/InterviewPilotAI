import os
import asyncio
# pyrefly: ignore [missing-import]
from google.adk.runners import Runner
# pyrefly: ignore [missing-import]
from google.adk.sessions import InMemorySessionService
# pyrefly: ignore [missing-import]
from google.genai import types

# Import the agents
from agents.resume_adk_agent import resume_adk_agent
from agents.skill_gap_adk_agent import skill_gap_adk_agent
from agents.hr_adk_agent import hr_adk_agent
from agents.technical_adk_agent import technical_adk_agent
from agents.roadmap_adk_agent import roadmap_adk_agent
from agents.fallback import generate_fallback_results

all_agents = [
    resume_adk_agent,
    skill_gap_adk_agent,
    hr_adk_agent,
    technical_adk_agent,
    roadmap_adk_agent
]

def get_agent_names():
    return [agent.name for agent in all_agents]

# Initialize a shared InMemorySessionService
sessions = InMemorySessionService()

async def run_single_adk_agent(agent, resume_text, task_prompt):
    """
    Runs a single ADK agent using the official Runner and SessionService.
    """
    # Map GEMINI_API_KEY to GOOGLE_API_KEY if needed (ADK expects GOOGLE_API_KEY)
    if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
        
    # Instantiate the Runner for this agent
    runner = Runner(agent=agent, session_service=sessions, app_name="InterviewPilot")
    
    # Create an asynchronous session
    session = await sessions.create_session(app_name="InterviewPilot", user_id="user_adk")
    
    # Construct the Content object in the format required by ADK
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"{task_prompt}\n\nResume Content:\n{resume_text}")]
    )
    
    # Run the agent (returns a synchronous Generator of Event objects)
    events = runner.run(
        user_id="user_adk",
        session_id=session.id,
        new_message=user_message
    )
    
    # Iterate over the events to collect the agent's text response
    response_text = ""
    for event in events:
        # ADK runner yields error events instead of raising exceptions directly during iteration
        if (hasattr(event, "error_code") and event.error_code) or (hasattr(event, "error_message") and event.error_message):
            error_code = getattr(event, "error_code", "UnknownError")
            error_msg = getattr(event, "error_message", "No detailed message")
            raise Exception(f"ADK Agent {agent.name} failed with {error_code}: {error_msg}")
            
        if hasattr(event, "content") and event.content:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
                    
    return response_text

def run_adk_agents(resume_text):
    """
    Runs all 5 ADK agents concurrently using asyncio.gather.
    If an API limit or quota exception is raised, it gracefully falls back to the high-fidelity offline synthesis engine.
    """
    async def run_all():
        tasks = [
            run_single_adk_agent(
                resume_adk_agent, 
                resume_text, 
                "Provide an in-depth resume analysis, scoring out of 100, strengths, weaknesses, and suggestions."
            ),
            run_single_adk_agent(
                skill_gap_adk_agent, 
                resume_text, 
                "Identify skill gaps and recommend professional courses using the registered tool."
            ),
            run_single_adk_agent(
                hr_adk_agent, 
                resume_text, 
                "Generate exactly 10 customized HR interview questions with insights."
            ),
            run_single_adk_agent(
                technical_adk_agent, 
                resume_text, 
                "Generate exactly 15 customized technical interview questions with model answers."
            ),
            run_single_adk_agent(
                roadmap_adk_agent, 
                resume_text, 
                "Create a detailed 30-day interview preparation and study roadmap."
            )
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        return {
            "resume_analysis": results[0],
            "skill_gap": results[1],
            "hr_questions": results[2],
            "technical_questions": results[3],
            "roadmap": results[4]
        }
        
    try:
        return asyncio.run(run_all())
    except Exception as e:
        print(f"[WARNING] ADK Orchestrator hit an error: {e}. Activating High-Fidelity Fallback Engine.")
        return generate_fallback_results(resume_text)