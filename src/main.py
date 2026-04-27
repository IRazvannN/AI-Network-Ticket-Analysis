import pandas as pd
from google import genai
import os
import re
import time

"""
AI-Driven Network Incident Triage System
Author: Razvan
Description: Automated classification of network support tickets using LLMs.
"""

# API CONFIGURATION
# Set GEMINI_API_KEY as an environment variable for secure access.
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# FILESYSTEM CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

INPUT_FILE = os.path.join(PROJECT_ROOT, "network_tickets.csv")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "analyzed_tickets_final.csv")

def analyze_ticket(ticket_text):
    """
    Executes inference via Gemini 2.0 Flash for incident classification.
    Implements guardrails to filter non-technical input.
    """
    prompt = f"""
    You are a Senior Cisco Network Engineer. 
    TASK: Analyze the support ticket provided below. 
    
    GUARDRAIL: If the input is not related to networking or IT infrastructure, 
    return exactly: "OUT_OF_SCOPE".
    
    Ticket: "{ticket_text}"
    
    Format:
    Category: [Hardware | Routing | Switching | Security | Layer 1]
    Priority: [High | Medium | Low]
    Command: [Cisco IOS verification command]
    """

    try:
        if not API_KEY:
            return "Error: API Key missing."
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    """ Main execution loop for batch processing tickets. """
    if not os.path.exists(INPUT_FILE):
        print(f"I/O Error: Missing {INPUT_FILE}")
        return

    try:
        df = pd.read_csv(INPUT_FILE, encoding="latin1", sep=None, engine='python')
    except Exception as e:
        print(f"Data Error: {e}")
        return

    results = []
    print(f"Initializing triage for {len(df)} records...")

    for _, row in df.iterrows():
        t_id = row.get('Ticket_ID', row.get('ID', 'N/A'))
        description = row.get('Description', row.get('Issue', ''))

        raw_output = analyze_ticket(description)

        if "OUT_OF_SCOPE" in raw_output:
            results.append({
                "ID": t_id, "Issue": description, "Category": "Non-Technical",
                "Priority": "N/A", "Cisco_Command": "No action required"
            })
        else:
            cat = re.search(r"Category:\s*(.*)", raw_output)
            pri = re.search(r"Priority:\s*(.*)", raw_output)
            cmd = re.search(r"Command:\s*(.*)", raw_output)

            results.append({
                "ID": t_id, "Issue": description,
                "Category": cat.group(1).strip() if cat else "N/A",
                "Priority": pri.group(1).strip() if pri else "N/A",
                "Cisco_Command": cmd.group(1).strip() if cmd else "Manual triage required"
            })

        time.sleep(1) # Rate-limit compliance

    try:
        pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
        print(f"Triage complete. Exported to: {OUTPUT_FILE}")
    except PermissionError:
        print("Export Error: File is currently open in another application.")

if __name__ == "__main__":
    main()