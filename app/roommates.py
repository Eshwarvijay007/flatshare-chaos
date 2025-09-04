from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class ConversationEntry:
    timestamp: datetime
    speaker: str
    message: str
    context_tags: List[str]
    sentiment: float
    effectiveness_score: Optional[float] = None

@dataclass
class AnalysisResult:
    topics: List[str]
    sentiment: float
    urgency: float
    question_count: int
    repeated_phrases: List[str]
    behavioral_flags: List[str]

@dataclass
class ConversationContext:
    current_topic: str
    participants: List[str]
    topic_history: List[str]
    emotional_tone: str
    thread_length: int

@dataclass
class Roommate:
    name: str
    style: str
    roast_signature: str
    quirks: List[str]
    triggers: Dict[str, List[str]]
    spice: int = 2
    roast_count: int = 0
    memory: List[str] = field(default_factory=list)

@dataclass
class EnhancedRoommate(Roommate):
    # New personality fields
    mood: int = 50  # 1-100 scale
    baseline_mood: int = 50
    roasting_strategy: str = "witty"  # aggressive, passive-aggressive, witty, absurd, indian-style
    effectiveness_score: float = 50.0  # percentage of successful roasts
    
    # Relationship tracking
    relationships: Dict[str, int] = field(default_factory=dict)  # roommate_name -> score (0-100)
    
    # Enhanced memory system
    conversation_memory: List[ConversationEntry] = field(default_factory=list)
    user_patterns: Dict[str, Any] = field(default_factory=dict)
    
    # Cultural context for roasting
    cultural_context: Dict[str, Any] = field(default_factory=dict)
