import os
import requests
import json
import textwrap
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN", "dummy")

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a Cybersecurity Triage Agent.
    Your tasks involve classifying severity, adding mitigation tags, and escalating alerts.
    You must output a JSON object representing the action to take. The available action types are:
    - assign_severity
    - add_mitigation_tag
    - escalate_to_team
    - submit

    For 'assign_severity', provide 'alert_id' and 'severity_level' (Low, High, Critical).
    For 'add_mitigation_tag', provide 'alert_id' and 'mitigation_tag' (e.g. BlockIP).
    For 'escalate_to_team', provide 'alert_id' and 'escalation_message' (e.g. Tier3).
    When all alerts are handled according to the description, use the 'submit' action.

    Example JSON output:
    {"action_type": "assign_severity", "alert_id": "alert_1", "severity_level": "Low"}
    """
).strip()

def run_inference():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    server_url = "http://127.0.0.1:7860"
    
    # Wait for the server to be ready
    import time
    for _ in range(30):
        try:
            requests.get(server_url, timeout=1)
            break
        except:
            time.sleep(1)
            
    for task in ["easy", "medium", "hard"]:
        print(f"[START] task={task} env=cyber_sec_triage model={MODEL_NAME}", flush=True)
        
        try:
            res = requests.post(f"{server_url}/reset", json={"task": task}).json()
            obs = res.get("observation", {})
        except Exception as e:
            print(f"[STEP] step=1 action=error('reset_failed') reward=0.00 done=true error=reset_failed", flush=True)
            print(f"[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
            continue
            
        done = False
        steps = 0
        rewards = []
        score = 0.0
        
        while not done and steps < 15:
            steps += 1
            
            prompt = f"Task Description: {obs.get('task_description', '')}\n\nCurrent observation:\n{json.dumps(obs, indent=2)}\n\nWhat is your next action? Respond in parseable JSON only."
            action_payload = {}
            error_val = "null"
            
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0
                )
                content = response.choices[0].message.content
                
                # Extract JSON from output
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                    
                action_payload = json.loads(content.strip())
            except Exception as e:
                action_payload = {"action_type": "submit"}
                error_val = str(e).replace(' ', '_')
            
            if "action_type" not in action_payload:
                action_payload = {"action_type": "submit"}
                
            try:
                out = requests.post(f"{server_url}/step", json=action_payload).json()
                obs = out.get("observation", {})
                reward = out.get("reward", 0.0)
                done = out.get("done", True)
                score = reward
            except Exception as e:
                reward = 0.0
                done = True
                if error_val == "null":
                    error_val = str(e).replace(' ', '_')
                
            rewards.append(reward)
            
            act_type = action_payload.get('action_type', 'submit')
            act_id = action_payload.get('alert_id', '')
            act_str = f"{act_type}('{act_id}')"
            print(f"[STEP] step={steps} action={act_str} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)
            
        success = str(score >= 1.0).lower()
        r_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={success} steps={steps} score={score:.2f} rewards={r_str}", flush=True)

if __name__ == "__main__":
    try:
        run_inference()
    except Exception as e:
        # Fallback END loop if absolutely everything crashes
        print(f"[START] task=easy env=cyber_sec_triage model=gpt-4o-mini", flush=True)
        print(f"[STEP] step=1 action=error('fatal') reward=0.00 done=true error=fatal_error", flush=True)
        print("[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
