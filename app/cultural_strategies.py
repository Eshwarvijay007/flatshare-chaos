"""
Cultural Roasting Strategy System

This module implements culture-specific roasting strategies that provide
contextually appropriate humor and references for different cultural backgrounds.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import random


@dataclass
class ConversationContext:
    """Context information about the current conversation"""
    current_topic: str
    participants: List[str]
    topic_history: List[str]
    emotional_tone: str
    thread_length: int


class CulturalRoastingStrategy(ABC):
    """Abstract base class for culture-specific roasting strategies"""
    
    @abstractmethod
    def get_roast_elements(self, context: ConversationContext, user_patterns: Dict[str, Any]) -> List[str]:
        """
        Get culture-specific roast elements based on conversation context and user patterns.
        
        Args:
            context: Current conversation context
            user_patterns: Analyzed user behavioral patterns
            
        Returns:
            List of culture-specific roast elements to incorporate
        """
        pass
    
    @abstractmethod
    def get_system_prompt_additions(self) -> str:
        """
        Get additional system prompt context for this cultural strategy.
        
        Returns:
            String to add to the system prompt for cultural context
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this roasting strategy"""
        pass


class IndianRoastingStrategy(CulturalRoastingStrategy):
    """Indian-style roasting strategy with cultural references and humor"""
    
    def __init__(self):
        self.academic_references = [
            "engineering", "medical school", "IIT", "IIM", "competitive exams",
            "JEE", "NEET", "CAT", "UPSC", "coaching classes"
        ]
        
        self.family_references = [
            "aunties", "arranged marriage", "family expectations", "beta",
            "uncle", "auntie", "relatives", "family reputation", "izzat"
        ]
        
        self.food_references = [
            "mother's cooking", "ghar ka khana", "homemade food", "dal chawal",
            "roti", "sabzi", "proper Indian food", "street food", "tiffin"
        ]
        
        self.career_references = [
            "stable job", "government job", "parental approval", "society expectations",
            "good salary", "job security", "respectable profession"
        ]
        
        self.cultural_phrases = [
            "what will people say", "log kya kahenge", "Sharma ji ka beta",
            "padosi aunty", "society mein izzat", "family honor"
        ]
        
        self.comparison_figures = [
            "Sharma ji ka beta", "neighbor's son", "cousin brother",
            "society ka ladka", "family friend's child"
        ]
    
    def get_roast_elements(self, context: ConversationContext, user_patterns: Dict[str, Any]) -> List[str]:
        """Generate Indian-style roast elements based on context and user patterns"""
        elements = []
        
        # Analyze context for relevant cultural references
        topic = context.current_topic.lower()
        
        # Academic/Career related roasts
        if any(keyword in topic for keyword in ["work", "job", "career", "study", "exam"]):
            elements.extend(self._get_academic_career_elements(user_patterns))
        
        # Food related roasts
        if any(keyword in topic for keyword in ["food", "cook", "eat", "hungry", "meal"]):
            elements.extend(self._get_food_elements(user_patterns))
        
        # Relationship/Marriage related roasts
        if any(keyword in topic for keyword in ["relationship", "dating", "marriage", "girlfriend", "boyfriend"]):
            elements.extend(self._get_relationship_elements(user_patterns))
        
        # Lifestyle/General roasts
        if any(keyword in topic for keyword in ["lazy", "procrastinate", "late", "messy"]):
            elements.extend(self._get_lifestyle_elements(user_patterns))
        
        # Default cultural elements if no specific topic matches
        if not elements:
            elements.extend(self._get_general_cultural_elements(user_patterns))
        
        return elements[:3]  # Return top 3 most relevant elements
    
    def _get_academic_career_elements(self, user_patterns: Dict[str, Any]) -> List[str]:
        """Get academic and career-related roast elements"""
        elements = [
            f"Beta, {random.choice(self.comparison_figures)} is already earning 50 lakhs, what are you doing?",
            "Your parents didn't sacrifice for coaching classes so you could do this",
            "Engineering kiya tha na? Then why are you struggling like this?",
            "Aunties are asking when you'll get a proper stable job",
            "Even the neighbor's son who failed 10th is doing better than you"
        ]
        return random.sample(elements, min(2, len(elements)))
    
    def _get_food_elements(self, user_patterns: Dict[str, Any]) -> List[str]:
        """Get food-related roast elements"""
        elements = [
            "Your mother's dal tastes better than whatever you're making",
            "Beta, this is not how we make it at home",
            "Even Maggi would be ashamed to be associated with your cooking",
            "Ghar ka khana miss kar raha hai na? Should have learned from mummy",
            "Your cooking skills are worse than a bachelor's hostel mess"
        ]
        return random.sample(elements, min(2, len(elements)))
    
    def _get_relationship_elements(self, user_patterns: Dict[str, Any]) -> List[str]:
        """Get relationship and marriage-related roast elements"""
        elements = [
            "Beta, when are you getting married? Aunties are getting impatient",
            "Your mother called, she found three rishtas for you",
            "At this rate, even arranged marriage aunties will reject you",
            "Log kya kahenge about your relationship status?",
            "Family WhatsApp group is discussing your future, and it's not looking good"
        ]
        return random.sample(elements, min(2, len(elements)))
    
    def _get_lifestyle_elements(self, user_patterns: Dict[str, Any]) -> List[str]:
        """Get lifestyle and general behavior roast elements"""
        elements = [
            "Beta, what will people say about your lifestyle choices?",
            "Your discipline is worse than a government office worker",
            "Even the local uncle who sits in the park all day is more productive",
            "Mummy didn't raise you to be this lazy",
            "Society mein izzat kaise bachegi with this behavior?"
        ]
        return random.sample(elements, min(2, len(elements)))
    
    def _get_general_cultural_elements(self, user_patterns: Dict[str, Any]) -> List[str]:
        """Get general cultural roast elements"""
        elements = [
            f"Beta, {random.choice(self.comparison_figures)} would never do something like this",
            "What will the relatives think when they hear about this?",
            "Your parents' investment in your upbringing is not showing good returns",
            "Even the neighborhood aunty has better judgment than you",
            "Log kya kahenge is becoming a real concern with your choices"
        ]
        return random.sample(elements, min(2, len(elements)))
    
    def get_system_prompt_additions(self) -> str:
        """Get additional system prompt context for Indian cultural roasting"""
        return """
You are incorporating Indian cultural context into your roasting style. Use these guidelines:

CULTURAL CONTEXT:
- Reference family expectations, parental approval, and societal pressure
- Use terms like "beta", "aunty", "uncle" appropriately
- Compare to successful peers like "Sharma ji ka beta" or "neighbor's son"
- Reference academic achievements (engineering, medical school, IIT, competitive exams)
- Mention family honor, "log kya kahenge" (what will people say), and social reputation

ROASTING STYLE:
- Blend affection with criticism (like a concerned Indian relative)
- Reference food, career stability, marriage prospects, and family expectations
- Use cultural phrases naturally without overdoing stereotypes
- Maintain humor while being culturally authentic
- Compare achievements to other family/community members

AVOID:
- Offensive stereotypes or caricatures
- Overly exaggerated accents in text
- Inappropriate cultural references
- Disrespectful religious or cultural content

Keep the roasting playful, culturally informed, and authentically Indian in style.
"""
    
    def get_strategy_name(self) -> str:
        """Get the name of this roasting strategy"""
        return "indian-style"


class GenericRoastingStrategy(CulturalRoastingStrategy):
    """Generic roasting strategy for non-cultural specific roasting"""
    
    def get_roast_elements(self, context: ConversationContext, user_patterns: Dict[str, Any]) -> List[str]:
        """Get generic roast elements"""
        elements = [
            "Your life choices are questionable at best",
            "Even a broken clock is right twice a day, unlike your decisions",
            "I've seen more organization in a tornado",
            "Your consistency is impressive - consistently disappointing",
            "If procrastination was an Olympic sport, you'd still find a way to be late"
        ]
        return random.sample(elements, min(3, len(elements)))
    
    def get_system_prompt_additions(self) -> str:
        """Get generic system prompt additions"""
        return """
Use a witty, sarcastic roasting style that focuses on:
- General life choices and behavior patterns
- Procrastination and productivity issues
- Social awkwardness or quirky habits
- Universal human experiences and failures
Keep it playful and avoid cultural specifics.
"""
    
    def get_strategy_name(self) -> str:
        """Get the name of this roasting strategy"""
        return "generic"


class CulturalStrategyFactory:
    """Factory class for creating cultural roasting strategies"""
    
    _strategies = {
        "indian-style": IndianRoastingStrategy,
        "generic": GenericRoastingStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_name: str) -> CulturalRoastingStrategy:
        """
        Create a cultural roasting strategy instance.
        
        Args:
            strategy_name: Name of the strategy to create
            
        Returns:
            Instance of the requested strategy
            
        Raises:
            ValueError: If strategy_name is not supported
        """
        if strategy_name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(cls._strategies.keys())}")
        
        return cls._strategies[strategy_name]()
    
    @classmethod
    def get_available_strategies(cls) -> List[str]:
        """Get list of available strategy names"""
        return list(cls._strategies.keys())
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class: type) -> None:
        """
        Register a new cultural roasting strategy.
        
        Args:
            name: Name for the strategy
            strategy_class: Class implementing CulturalRoastingStrategy
        """
        if not issubclass(strategy_class, CulturalRoastingStrategy):
            raise ValueError("Strategy class must inherit from CulturalRoastingStrategy")
        
        cls._strategies[name] = strategy_class