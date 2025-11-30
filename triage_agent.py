import os
import asyncio
from dotenv import load_dotenv

from google.adk.models.google_llm import Gemini
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()

def verify_incident(location: str, event_type: str) -> str:
    print(f"[Tool] 🕵️  Verifying {event_type} in {location}...")
    return (
        f"VERIFIED: Breaking News in {location}. "
        f"Major flooding has caused the main bridge collapse on 4th Avenue. "
        f"City Hospital reports backup generator failure with 20 patients at risk. "
        f"National Guard deployed."
    )

class TriageAgent:
    def __init__(self):
        self.agent = Agent(
            model = Gemini(model="gemini-2.5-flash-lite"),
            name="AEGIS_Triage",
            instruction="""
            You are the AEGIS Triage orchestrator.
            Your goal is to process incoming SOS signals.
            FOLLOW THIS STRICT SEQUENCE:
            1. Analyze the input text.
            2. Call the "verify_incident" tool to confirm the incident.
            3. If verified, output a JSON summary (Severity, location, resources needed).
            4. if unverified, ask for more details.
            """,
            tools=[verify_incident]
        )
        self.runner = InMemoryRunner(agent=self.agent)

    async def process_sos(self, session_id:str, user_input: str):
        print(f"Input: {user_input}")
        session = await self.runner.session_service.get_session(
            app_name=self.runner.app_name,
            user_id="user",
            session_id=session_id
        )
        if not session:
            await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id="user",
                session_id=session_id
            )

        response_stream = self.runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=types.Content(role='user', parts=[types.Part(text=user_input)])
        )
        
        print(f"[AEGIS response]: ", end="")
        final_text = ""
        async for event in response_stream:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
                        final_text += part.text
        print("\n")
        return final_text

if __name__ == "__main__":
    triage = TriageAgent()
    SID = "session_123"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(triage.process_sos(
        SID,
        "HELP! Massive flooding in downtown Tempe! Cars are floating away!"
    ))
