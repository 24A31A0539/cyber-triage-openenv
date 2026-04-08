from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

class ActionType(str, Enum):
    focus_alert = "focus_alert"
    assign_severity = "assign_severity"
    add_mitigation_tag = "add_mitigation_tag"
    escalate_to_team = "escalate_to_team"
    submit = "submit"

class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action_type: ActionType = Field(..., description="The type of action to take. 'submit' ends the episode.")
    alert_id: Optional[str] = Field(None, description="The ID of the alert to apply the action to (e.g. 'alert_1').")
    severity_level: Optional[str] = Field(None, description="Severity to assign: 'Low', 'High', or 'Critical'.")
    mitigation_tag: Optional[str] = Field(None, description="Tag to mitigate the alert, e.g., 'BlockIP'.")
    escalation_message: Optional[str] = Field(None, description="Message to escalate, e.g., 'Tier3 please investigate'.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Any additional metadata.")

class SecurityAlert(BaseModel):
    id: str = Field(..., description="Unique alert ID")
    source_ip: str = Field(..., description="Source IP address of the alert")
    alert_type: str = Field(..., description="Type of the alert, e.g., 'Failed Login', 'SQL Injection'")
    payload: str = Field(..., description="Description or payload of the alert")
    severity: str = Field("Unclassified", description="Assigned severity level")
    mitigation_tags: List[str] = Field(default_factory=list, description="List of assigned mitigation tags")
    escalated_to: Optional[str] = Field(None, description="Team or message escalated to")

class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    done: bool = Field(False, description="Whether the episode is finished")
    reward: float = Field(0.0, description="The current reward")
    current_alert_id: Optional[str] = Field(None, description="The alert ID currently focused")
    alerts: List[SecurityAlert] = Field(default_factory=list, description="List of all alerts in the environment")
    last_action_error: Optional[str] = Field(None, description="Error message from the last action, if any")
    task_description: str = Field("", description="The instruction of the task to complete")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Any additional state metadata")

class Reward(BaseModel):
    score: float = Field(..., description="The final score")
    done: bool = Field(..., description="Whether the task is done")
