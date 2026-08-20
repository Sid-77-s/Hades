from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class MissionStatus(str, Enum):
    CONVERSATION = "CONVERSATION"
    ALIGNMENT = "ALIGNMENT"
    AUTHORIZED_EXECUTION = "AUTHORIZED_EXECUTION"
    BACKGROUND_WORK = "BACKGROUND_WORK"
    NEEDS_USER = "NEEDS_USER"
    COMPLETED = "COMPLETED"

class InformationSource(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"

class Criticality(str, Enum):
    CRITICAL = "CRITICAL"
    NON_CRITICAL = "NON_CRITICAL"

class FieldState(BaseModel):
    value: Optional[str] = None
    source: InformationSource = InformationSource.UNKNOWN
    criticality: Criticality = Criticality.NON_CRITICAL
    
class MissionUnderstanding(BaseModel):
    objective: FieldState = FieldState(criticality=Criticality.CRITICAL)
    desired_outcome: FieldState = FieldState(criticality=Criticality.CRITICAL)
    success_criteria: FieldState = FieldState(criticality=Criticality.CRITICAL)
    context: FieldState = FieldState(criticality=Criticality.NON_CRITICAL)
    constraints: FieldState = FieldState(criticality=Criticality.NON_CRITICAL)
    priorities: FieldState = FieldState(criticality=Criticality.NON_CRITICAL)
    preferences: FieldState = FieldState(criticality=Criticality.NON_CRITICAL)
    important_decisions: FieldState = FieldState(criticality=Criticality.CRITICAL)
    
    assumptions: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    
    # We add this field to represent whether we have mutual understanding (true) or still figuring it out
    mutual_understanding_reached: bool = False

class ConversationalAction(str, Enum):
    ASK = "ASK"
    PROPOSE = "PROPOSE"
    EXPLORE = "EXPLORE"
    CHALLENGE = "CHALLENGE"
    ACKNOWLEDGE = "ACKNOWLEDGE"
    
class ConversationalDecision(BaseModel):
    action: ConversationalAction
    reasoning: str
    response_text: str

class Mission(BaseModel):
    id: str
    status: MissionStatus = MissionStatus.CONVERSATION
    understanding: MissionUnderstanding = Field(default_factory=MissionUnderstanding)
