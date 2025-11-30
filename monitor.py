import asyncio
import random
import logging
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
from google.adk.models.google_llm import Gemini
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()

logger = logging.getLogger("AEGIS_Monitor")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_sensor_reading():
    level = random.choices([2.0, 4.5, 8.0, 14.5], weights=[0.4, 0.3, 0.2, 0.1])[0]
    return f"Water level sensor reading: {level} feet."

class FloodMonitor:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(model="gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY")),
            name="Flood_Watch_Unit",
            instruction="""
            You are an autonomous flood monitoring agent.
            Analyse the sensor reading.
            Rules:
            - If level < 10ft: Respond "STATUS: Normal".
            - If level > 10ft: Respond "STATUS: CRITICAL WARNING - DISPATCH REQUIRED".
            output ONLY the status string.
            """
        )
        self.runner = InMemoryRunner(agent=self.agent)
    
    async def check_sensor(self):
        session_id = f"monitor_run_{datetime.now().timestamp()}"
        await self.runner.session_service.create_session(
            app_name=self.runner.app_name,
            user_id="system_monitor",
            session_id=session_id
        )
        reading = get_sensor_reading()
        logger.info(f"Sensor data received: {reading}")
        response_stream = self.runner.run_async(
            user_id="system_monitor",
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=reading)])
        )
        final_decision = ""
        async for event in response_stream:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_decision += part.text
        return final_decision.strip()

async def start_monitoring_loop():
    monitor = FloodMonitor()
    logger.info("--- AEGIS Flood Monitor Started ---")
    for i in range(5):
        decision = await monitor.check_sensor()
        if "CRITICAL" in decision:
            logger.error(f"Alert triggered: {decision}")
        else:
            logger.info(f"Safe: {decision}")
        logger.info("sleeping for 3 seconds...")
        await asyncio.sleep(3)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_monitoring_loop())