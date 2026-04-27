# AI-Driven Network Incident Triage System

An automated Network Operations (NetOps) tool designed to reduce **Mean Time to Repair (MTTR)** by bridging the gap between unstructured user complaints and technical diagnostics. This system utilizes the **Gemini 2.0 Flash** LLM to analyze support tickets and map them to precise **Cisco IOS** troubleshooting commands.

## 🏗️ System Architecture
The tool operates as an intelligent middleware layer between the helpdesk (CSV) and the technical engineering tier (NOC). 
- **Input Layer:** Ingests raw, unstructured incident descriptions.
- **Cognitive Engine:** Processes data via Gemini 2.0 Flash, acting as a virtual Tier 1 Engineer.
- **Validation Tier:** Implements technical guardrails to filter non-networking inputs.
- **Output Layer:** Generates structured diagnostic data for rapid engineering response.

## 🚀 Key Features
- **Automated Triage:** Immediate classification of incidents into Networking Layers (Routing, Switching, Security, L1).
- **Incident Prioritization:** Heuristic-based priority assignment (High/Medium/Low) based on symptom severity.
- **Diagnostic Command Mapping:** Direct mapping of symptoms to Cisco IOS verification commands (e.g., `show ip ospf neighbor`).
- **Input Validation:** Built-in "Sanity Checks" to detect and flag "Out of Scope" (non-technical) tickets.

## 🛠️ Technical Stack
- **Language:** Python 3.12
- **Core Libraries:** `pandas` (I/O), `google-genai` (Inference), `re` (Data Extraction).
- **Environment:** Professional virtual environment (`.venv`) structure.

## 📺 Demo
[Video Walkthrough: AI-Driven Network Analysis](https://youtu.be/0gocSxgC5f0)
*Demonstration of the system processing real-world scenarios and filtering out-of-scope noise.*

## 📋 Setup & Usage
1. **Initialize Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Configure Authentication:**
   Export your Gemini API Key as an environment variable:
   `export GEMINI_API_KEY='your_key_here'`
3. **Execute Triage:**
   Run the analysis script: `python src/main.py`

## 📂 Project Structure
- `src/main.py`: Main execution logic and LLM interface.
- `network_tickets.csv`: Dataset of diverse network incidents for technical analysis.

