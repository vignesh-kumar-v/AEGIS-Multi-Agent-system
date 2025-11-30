import asyncio
import logging
import sys
from monitor import FloodMonitor
from triage_agent import TriageAgent
from sentinels import run_parellel_analysis

logger = logging.getLogger("AEGIS_CORE")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('>> %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def run_aegis_system():
    logger.info("INITIALIZING AEGIS AUTONOMOUS MESH...")
    monitor_unit = FloodMonitor()
    triage_unit = TriageAgent()
    logger.info("SYSTEM LIVE. MONITORING SENSORS...")
    monitoring_active = True
    while monitoring_active:
        sensor_status = await monitor_unit.check_sensor()
        if "CRITICAL" not in sensor_status:
            logger.info(f"Sector clear: {sensor_status}")
            await asyncio.sleep(2)
            continue
        logger.warning(f"TRIGGER RECEIVED: {sensor_status}")
        logger.info("Engaging triage protocols...")
        sos_payload = f"SENSOR ALERT: {sensor_status}. Location: Downtown River District. Requesting immediate verification."
        triage_report = await triage_unit.process_sos("session_master", sos_payload)
        logger.info("TRIAGE REPORT GENERATED.")
        logger.info("Deploying sentinel swarm (Parallel execution)...")
        tactical_data = await run_parellel_analysis(triage_report)
        print("\n" + "█"*50)
        print("      AEGIS FINAL MISSION REPORT")
        print("█"*50)
        print(f"STATUS:  🔴 ACTIVE DISASTER")
        print(f"SOURCE:  {sensor_status}")
        print("-" * 50)
        print("MEDICAL INTELLIGENCE:")
        print(tactical_data[0] if len(tactical_data) > 0 else "No Data")
        print("-" * 50)
        print("INFRASTRUCTURE INTELLIGENCE:")
        print(tactical_data[1] if len(tactical_data) > 1 else "No Data")
        print("█"*50 + "\n")
        logger.info("Response Coordination Complete. System entering standby.")
        monitoring_active = False

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_aegis_system())
    except KeyboardInterrupt:
        logger.info("System manually shut down.")