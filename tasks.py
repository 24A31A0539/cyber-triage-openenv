from models import SecurityAlert

def get_initial_alerts(task_level: str) -> list[SecurityAlert]:
    if task_level == "easy":
        return [
            SecurityAlert(id="alert_1", source_ip="192.168.1.50", alert_type="Failed Login", payload="5 failed attempts from internal IP.")
        ]
    elif task_level == "medium":
        return [
            SecurityAlert(id="alert_1", source_ip="192.168.1.50", alert_type="Failed Login", payload="5 failed attempts from internal IP."),
            SecurityAlert(id="alert_2", source_ip="203.0.113.10", alert_type="SQL Injection", payload="Malicious SQL payload detected on /login block."),
            SecurityAlert(id="alert_3", source_ip="10.0.0.5", alert_type="Port Scan", payload="Sequential port scan detected.")
        ]
    elif task_level == "hard":
        return [
            SecurityAlert(id="alert_1", source_ip="192.168.1.50", alert_type="Failed Login", payload="5 failed attempts from internal IP."),
            SecurityAlert(id="alert_2", source_ip="203.0.113.10", alert_type="SQL Injection", payload="Malicious SQL payload detected on /login block."),
            SecurityAlert(id="alert_3", source_ip="10.0.0.5", alert_type="Port Scan", payload="Sequential port scan detected."),
            SecurityAlert(id="alert_4", source_ip="198.51.100.22", alert_type="Data Exfiltration", payload="Unusually large data transfer to external IP.")
        ]
    return []

def get_task_description(task_level: str) -> str:
    if task_level == "easy":
        return "Classify alert_1 ('Failed Login') as 'Low' severity."
    elif task_level == "medium":
        return "Classify alert_1 and alert_3 as 'Low' severity. Classify alert_2 ('SQL Injection') as 'High' severity."
    elif task_level == "hard":
        return "Classify alert_1 and alert_3 as 'Low' severity. Classify alert_2 as 'High' and assign mitigation_tag 'BlockIP'. Classify alert_4 as 'Critical' and escalate_to_team 'Tier3'."
    return ""

def grade_task(task_level: str, alerts: list[SecurityAlert]) -> float:
    score = 0.0
    if task_level == "easy":
        for a in alerts:
            if a.id == "alert_1" and a.severity == "Low":
                return 1.0
        return 0.0
        
    elif task_level == "medium":
        correct = 0
        for a in alerts:
            if a.id == "alert_1" and a.severity == "Low": correct += 1
            if a.id == "alert_2" and a.severity == "High": correct += 1
            if a.id == "alert_3" and a.severity == "Low": correct += 1
        return round(correct / 3.0, 2)
        
    elif task_level == "hard":
        correct = 0
        for a in alerts:
            if a.id == "alert_1" and a.severity == "Low": correct += 1
            if a.id == "alert_2" and a.severity == "High" and "BlockIP" in a.mitigation_tags:
                correct += 1
            if a.id == "alert_3" and a.severity == "Low": correct += 1
            if a.id == "alert_4" and a.severity == "Critical":
                if a.escalated_to and "Tier3" in a.escalated_to:
                    correct += 2 # Worth more
        
        return round(min(1.0, correct / 5.0), 2)
        
    return 0.0
