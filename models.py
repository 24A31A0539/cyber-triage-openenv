from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from enum import Enum

class ActionType(str, Enum):
    focus_alert = "focus_alert"
    assign_severity = "assign_severity"
    add_mitigation_tag = "add_mitigation_tag"
    escalate_to_team = "escalate_to_team"
    submit = "submit"

class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action_type: ActionType
    alert_id: Optional[str] = None
    severity_level: Optional[str] = None
    mitigation_tag: Optional[str] = None
    escalation_message: Optional[str] = None
    metadata: Dict[str, Any] = {}

class SecurityAlert(BaseModel):
    id: str
    source_ip: str
    alert_type: str
    payload: str
    severity: str = "Unclassified"
    mitigation_tags: List[str] = []
    escalated_to: Optional[str] = None

class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    done: bool = False
    reward: float = 0.0
    current_alert_id: Optional[str] = None
    alerts: List[SecurityAlert] = []
    last_action_error: Optional[str] = None
    task_description: str = ""
    metadata: Dict[str, Any] = {}

class Reward(BaseModel):
    score: float
    done: bool
