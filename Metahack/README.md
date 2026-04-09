# Cyber Security Operations Center (SOC) Triage OpenEnv

## Problem Description
This environment challenges agents with complex security incident management, analyzing alerts, taking actions like assigning severity, applying mitigation tags, and escalating dangerous incidents to specialized response teams.

## Real-world use case
Security Operations Centers (SOC) frequently triage thousands of alerts daily into different severity buckets and apply automated mitigations (like IP blocking) or routing to specific tiers. This environment provides a realistic training ground for LLM agents completing enterprise security capabilities.

## Action Space
`models.Action`
- `focus_alert(alert_id)`: View an alert payload
- `assign_severity(alert_id, severity_level)`: Change an alert's severity rating (e.g. 'Low', 'High', 'Critical')
- `add_mitigation_tag(alert_id, mitigation_tag)`: Append a mitigation protocol (e.g. 'BlockIP')
- `escalate_to_team(alert_id, escalation_message)`: Send an outgoing escalation to human operators
- `submit()`: Signal task completion

## Observation Space
`models.Observation`
- `done`: Indicates episode termination
- `reward`: Current total reward (0.0 - 1.0)
- `current_alert_id`: The ID of currently focused alert
- `alerts`: Full state block of the SOC dashboard and incident details
- `task_description`: Instructions for the agent
- `last_action_error`: Reason for previous action failure

## Task Descriptions
- The **easy** task contains a single internal alert that must be classified as 'Low' severity.
- The **medium** task acts as a batch triage exercise, containing 3 alerts (Failed Logins, Port Scans, SQL Injections) that need parallel severity assignments.
- The **hard** task layers on contextual action generation: agents must escalate Data Exfiltration to "Tier3" and implicitly mitigate an injection by tagging it with "BlockIP".

## Reward Logic
Rewards track partial progress continuously. 
Instead of waiting until `submit()`, the `reward` climbs parametrically matching the *correct ratio* of correctly mitigated alerts divided by total required actions.

## Setup Instructions
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## How to run locally
Execute the exact command above. If using a container:
```bash
docker build -t openenv-cyber-sec-triage .
docker run -p 8000:8000 openenv-cyber-sec-triage
```

## Example API calls

Reset environment to task:
```bash
curl -X POST http://localhost:8000/reset \
     -H "Content-Type: application/json" \
     -d '{"task": "hard"}'
```

Step execution:
```bash
curl -X POST http://localhost:8000/step \
     -H "Content-Type: application/json" \
     -d '{"action_type": "assign_severity", "alert_id": "alert_1", "severity_level": "Low"}'
```

Get state:
```bash
curl http://localhost:8000/state
```

## Baseline scores
When evaluating the default proxy in `inference.py` script:
- Easy: 1.00
- Medium: 1.00
- Hard: 1.00
