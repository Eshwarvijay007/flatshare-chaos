# Flatshare Chaos: Roast Edition (macOS, offline-first)

An offline multi-agent roommate simulator for macOS where distinct AI roommates, powered by the `gpt-oss:20b` model, roast you and each other.

## Getting Started

### Prerequisites
- macOS
- Python 3.11+

### 1. Setup Environment
First, create and activate a Python virtual environment:
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Backend Servers
In a terminal window, run one of the provided Python scripts to launch the model server and the application backend. The recommended script is `run.py`:
```bash
python3.11 run.py
```
This script will start all the necessary server processes and keep them running.

### 4. Run the Client Interface
Once the servers are running, open a **new terminal window** to run the user interface.

#### Text-Only Mode
To interact with the roommates via a text-only interface, run the following command:
```bash
python3.11 -m app.ui.cli --stream --spice=2
```

#### Voice Mode (macOS)
For the full voice-interactive experience on macOS, you'll need to install some extra audio libraries first.

1.  **Install Audio Libraries**:
    ```bash
    pip install pyttsx3 sounddevice vosk
    ```
2.  **Download Speech-to-Text Model**:
    Download a small [Vosk English model](https://alphacephei.com/vosk/models) and place its contents in the `models/vosk-en-small/` directory.

3.  **(Optional) Install Better TTS Voices**:
    For more natural-sounding roommates, you can install enhanced voices via `System Settings → Accessibility → Spoken Content → System Voice → Manage Voices…`.

Once the setup is complete, run the application with the voice flags in your new terminal:
```bash
python3.11 -m app.ui.cli --voice --mic --vosk-model models/vosk-en-small
```

## Architecture and Tools

This project uses a client-server architecture to create a dynamic, multi-agent simulation.

*   **Backend Server**: A **FastAPI** server acts as the central brain. It receives requests from the client, queries the language model, and manages the state of the simulation.

*   **Core Simulation Engine**: The `app` directory contains the core logic, with separate modules for managing:
    *   **Personalities**: Crafts prompts and context for each AI agent.
    *   **Moods**: Tracks and modifies the mood of each roommate.
    *   **Relationships**: Manages the evolving relationships between agents.

*   **Language Model**: The personalities are powered by a locally-run `gpt-oss:20b` model, which is orchestrated by the backend.

*   **Client Interface**: The primary interface is a Python-based Command-Line Interface (CLI) built using `argparse`.

### Key Libraries and Tools
*   **Language**: Python 3.11
*   **Backend**: FastAPI
*   **Speech-to-Text**: Vosk
*   **Text-to-Speech**: pyttsx3 (utilizing native macOS voices)
*   **HTTP Client**: httpx (for async requests to the model server)

## Contribution

This project is the result of a solo development effort. Every part of this project, from the initial concept and architecture to the final code, was built from scratch by a single contributor.