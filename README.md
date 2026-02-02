# AEGIS (Autonomous Emergency General Intelligence System)

AEGIS is an advanced, autonomous disaster response framework designed to detect, analyze, and coordinate responses to critical incidents. By leveraging Google's **Agent Development Kit (ADK)** and **Gemini** models, AEGIS simulates a multi-agent mesh network that monitors sensors, triages alerts, and deploys specialized "Sentinel" agents for detailed situational analysis.

🏗️ System Architecture
AEGIS utilizes an asynchronous orchestration engine to manage specialized agent lifecycles and tool integration.

graph TD
    subgraph Orchestrator [Agent Mesh Orchestrator]
        A[Input: Real-time Flood Data] --> B{asyncio Task Manager}
    end

    subgraph Specialized_Agents [Parallel Execution]
        B --> C[FloodMonitor: Sensor Surveillance]
        B --> D[TriageAgent: Alert Verification]
        B --> E[MedicalSentinel: Resource Planning]
        B --> F[InfraSentinel: Damage Assessment]
    end

    subgraph Tools [External Tool Integration]
        C --- G[(Satellite API)]
        D --- H[(Emergency Services DB)]
    end

    C & D & E & F --> I[Consolidated Mission Report]
    I --> J[Output: Emergency Intelligence]

    style Orchestrator fill:#f9f,stroke:#333,stroke-width:2px
    style Specialized_Agents fill:#bbf,stroke:#333,stroke-width:2px

## 🚀 Features

*   **Autonomous Monitoring**: Continuous surveillance of sensor data (simulated flood sensors) using the `FloodMonitor` agent.
*   **Intelligent Triage**: The `TriageAgent` verifies alerts using external tools and assesses the severity of the situation.
*   **Parallel Intelligence**: Deploys multiple "Sentinel" agents concurrently to analyze different aspects of a crisis (Medical & Infrastructure) in real-time.
*   **Modular Architecture**: Built with a clear separation of concerns between monitoring, triage, and analysis units.

## 📂 Project Structure

*   **`main.py`**: The core orchestration engine. It initializes the mesh, manages the lifecycle of the response, and consolidates final intelligence reports.
*   **`monitor.py`**: Contains the `FloodMonitor` class. It simulates environmental sensors and uses an AI agent to classify readings as "Normal" or "Critical".
*   **`triage_agent.py`**: Hosts the `TriageAgent`. This agent acts as the dispatcher, verifying incoming SOS signals against real-time data (simulated via tools) and summarizing the event.
*   **`sentinels.py`**: Defines the specialized agents (`Medical_Sentinel` and `Infra_Sentinel`) and the logic for parallel execution using `asyncio`.

## 🛠️ Installation

1.  **Clone the repository** (if applicable) or ensure you are in the project root.

2.  **Install dependencies**:
    Ensure you have Python 3.10+ installed. Run the following command to install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

AEGIS requires a Google Gemini API key to function.

1.  Create a `.env` file in the root directory.
2.  Add your API key to the file:

    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## 🖥️ Usage

To launch the full AEGIS system:

```bash
python main.py
```

### What to Expect
1.  **Initialization**: The system spins up the `FloodMonitor` and begins checking sensor readings.
2.  **Monitoring**: You will see periodic logs of sensor checks. Most will be "Safe".
3.  **Trigger**: Once a simulated "CRITICAL" reading occurs, the system engages the Triage protocols.
4.  **Response**:
    *   The **Triage Agent** verifies the incident.
    *   **Sentinels** are deployed in parallel to analyze the verified report.
5.  **Final Report**: The system outputs a consolidated "Mission Report" detailing Medical and Infrastructure intelligence before entering standby.

### Running Individual Modules
You can also run individual components for testing or demonstration purposes:

*   **Test Monitoring**: `python monitor.py`
*   **Test Triage**: `python triage_agent.py`
*   **Test Sentinels**: `python sentinels.py`

## 📦 Dependencies

*   `google-adk`
*   `google-genai`
*   `python-dotenv`
*   `asyncio`

---
*AEGIS: Autonomous Response for a Safer Tomorrow.*
