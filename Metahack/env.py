import typing
from models import Action, ActionType, Observation, SecurityAlert
from tasks import get_initial_alerts, get_task_description, grade_task
import copy

class Environment:
    def __init__(self):
        self.step_count = 0
        self.alerts: list[SecurityAlert] = []
        self.task_level: str = "easy"
        self.current_alert_id: str | None = None
        self.last_action_error: str | None = None
        
    def reset(self, task: str = "easy") -> Observation:
        self.step_count = 0
        self.task_level = task
        self.alerts = get_initial_alerts(task)
        self.current_alert_id = self.alerts[0].id if self.alerts else None
        self.last_action_error = None
        
        return Observation(
            done=False,
            reward=0.0,
            current_alert_id=self.current_alert_id,
            alerts=self.alerts,
            last_action_error=self.last_action_error,
            task_description=get_task_description(self.task_level)
        )

    def step(self, action: Action) -> dict:
        self.step_count += 1
        self.last_action_error = None
        
        # apply action
        alert = next((a for a in self.alerts if a.id == action.alert_id), None)
        if action.alert_id and not alert:
            self.last_action_error = f"Alert ID {action.alert_id} not found."
            
        elif action.action_type == ActionType.focus_alert:
            if alert:
                self.current_alert_id = alert.id
        elif action.action_type == ActionType.assign_severity:
            if alert and action.severity_level:
                alert.severity = action.severity_level
        elif action.action_type == ActionType.add_mitigation_tag:
            if alert and action.mitigation_tag:
                if action.mitigation_tag not in alert.mitigation_tags:
                    alert.mitigation_tags.append(action.mitigation_tag)
        elif action.action_type == ActionType.escalate_to_team:
            if alert and action.escalation_message:
                alert.escalated_to = action.escalation_message
                
        # grade
        reward = grade_task(self.task_level, self.alerts)
        done = reward >= 1.0 or self.step_count >= 15
        if action.action_type == ActionType.submit:
            done = True
            
        obs = Observation(
            done=done,
            reward=reward,
            current_alert_id=self.current_alert_id,
            alerts=self.alerts,
            last_action_error=self.last_action_error,
            task_description=get_task_description(self.task_level)
        )
        
        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "done": done,
            "info": {}
        }
        
    def state(self) -> dict:
        return {
            "step_count": self.step_count,
            "task_level": self.task_level,
            "current_alert_id": self.current_alert_id
        }
