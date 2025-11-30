import asyncio
import os
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()
def create_sentinel(name: str, focus_area: str):
    return Agent(
        model=Gemini(model="gemini-2.5-flash-lite"),
        name=name,
        instruction=f"""
        You are the {name}.
        Your only job is to extract {focus_area} details from the text.
        If found: return a short strict bulleted list of {focus_area} issues.
        If not found: return "CLEAR".
        Do not include conversational filler. Just the data.
        """
    )
async def run_agent_task(agent_name: str, prompt: str, focus: str):
    agent = create_sentinel(agent_name, focus)
    runner = InMemoryRunner(agent=agent)
    session_id = f"session_{agent_name}"
    await runner.session_service.create_session(
        app_name = runner.app_name,
        user_id = "user",
        session_id = session_id
    )
    print(f"{agent_name} started analysis.")
    response_stream = runner.run_async(
        user_id = "user",
        session_id = session_id,
        new_message = types.Content(role="user", parts=[types.Part(text=prompt)])
    )
    final_text = ""
    async for event in response_stream:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text += part.text
    print(f"{agent_name} finished.")
    return f"--- {agent_name.upper()} REPORT --- \n{final_text}"

async def run_parellel_analysis(incident_text: str):
    print(f"Input scenario: {incident_text}\n")
    print("[system] broadcasting to sentinels in PARALLEL...")
    task_medic = run_agent_task(
        "Medical_Sentinel",
        incident_text,
        "HUMAN INJURY, CASUALITIES, & HEALTH RISKS"
    )
    task_infra = run_agent_task(
        "Infra_Sentinel",
        incident_text,
        "ROADS, BRIDGES, POWER LINES, & BUILDINGS"
    )
    results = await asyncio.gather(task_medic, task_infra)
    return results

if __name__ == "__main__":
    disaster_scenario = """
    A 6.0 earthquake hit downtown. The I-10 bridge has collapsed blocking all exit routes. 
    St. Mary's Hospital reports power failure and they have 40 critical patients on ventilators 
    with backup generators failing in 2 hours. No fatalities reported yet.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    reports = loop.run_until_complete(run_parellel_analysis(disaster_scenario))
    print("\n" + "="*40)
    print("      FINAL CONSOLIDATED INTELLIGENCE")
    print("="*40)
    for report in reports:
        print(report)