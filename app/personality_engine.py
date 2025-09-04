"""
Enhanced personality-driven interaction engine.
Handles unique interactions between different personality types.
"""

import random
from typing import List, Dict, Any, Iterator, Optional
from app.roommates import EnhancedRoommate, ConversationEntry
from app.conversation_analyzer import ConversationAnalyzer
from datetime import datetime


class PersonalityEngine:
    """Engine that creates personality-driven interactions between roommates."""
    
    def __init__(self, roommates: List[EnhancedRoommate], backend: Any):
        self.roommates = roommates
        self.backend = backend
        self.analyzer = ConversationAnalyzer()
        self.interaction_history: List[ConversationEntry] = []
        
        # Personality-specific response templates
        self.personality_templates = self._load_personality_templates()
        self.interaction_dynamics = self._load_interaction_dynamics()
    
    def _load_personality_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load personality-specific response templates."""
        return {
            "CodeMaster": {
                "roast_templates": [
                    "Your code is like Internet Explorer - slow, outdated, and nobody wants to use it",
                    "I've seen better logic in a random number generator",
                    "Your debugging skills are like your dating life - non-existent",
                    "That solution has more bugs than a beta release",
                    "You're the human equivalent of a stack overflow"
                ],
                "reaction_templates": [
                    "Actually, the optimal approach would be...",
                    "That's not how algorithms work, but okay",
                    "Have you tried reading the documentation?",
                    "Error 404: Logic not found",
                    "Your approach has O(terrible) complexity"
                ]
            },
            "SavageBurn": {
                "roast_templates": [
                    "You're like a participation trophy - everyone gets one but nobody wants it",
                    "I'd roast you but my mom said I can't burn trash",
                    "You're the reason they put instructions on shampoo bottles",
                    "If stupidity was a superpower, you'd be invincible",
                    "You're like a broken pencil - completely pointless"
                ],
                "reaction_templates": [
                    "Imagine thinking that was clever",
                    "The audacity is unmatched",
                    "That's cute, try again",
                    "Weak sauce, step your game up",
                    "I've heard better comebacks from a mute person"
                ]
            },
            "UncleJi": {
                "roast_templates": [
                    "Beta, in India we have saying - empty vessels make most noise, and you are very noisy",
                    "My nephew is your age and already has house, car, and wife. What do you have?",
                    "You are wasting your life like water in desert",
                    "In my time, we had respect for elders and discipline. What is this nonsense?",
                    "You need good Indian wife to set you straight"
                ],
                "reaction_templates": [
                    "This generation has no respect, I tell you",
                    "Back in India, we would never behave like this",
                    "You should be studying or working, not making jokes",
                    "What will your parents think of this behavior?",
                    "Beta, you need to focus on your future"
                ]
            },
            "ChefCritic": {
                "roast_templates": [
                    "Your cooking skills are like your personality - bland and disappointing",
                    "I've seen more flavor in cardboard than in your food",
                    "You microwave everything like you microwave your relationships - quick and unsatisfying",
                    "Your taste buds must be on vacation permanently",
                    "Gordon Ramsay would need therapy after tasting your cooking"
                ],
                "reaction_templates": [
                    "That's not how you prepare that dish, honestly",
                    "The flavor profile is completely wrong",
                    "You're committing a crime against cuisine",
                    "My grandmother is rolling in her grave",
                    "That's an insult to food everywhere"
                ]
            },
            "BeatDrop": {
                "roast_templates": [
                    "Your life has less rhythm than a broken metronome",
                    "You're like a bad remix - nobody asked for it and it ruins the original",
                    "Your energy is flatter than auto-tuned vocals",
                    "You dance like you're being electrocuted by bad music",
                    "Your vibe is more dead than vinyl records"
                ],
                "reaction_templates": [
                    "That beat is trash, no cap",
                    "Your music taste needs serious help",
                    "The vibe is completely off",
                    "You need to turn up the energy",
                    "This is why the party died"
                ]
            },
            "ChaosKing": {
                "roast_templates": [
                    "You're more organized than me, which means you have no personality",
                    "Your life is so neat it's boring - where's the adventure?",
                    "You fold your clothes like you fold under pressure - perfectly and pathetically",
                    "At least my mess has character, unlike your sterile existence",
                    "You're like a museum - everything in its place and equally lifeless"
                ],
                "reaction_templates": [
                    "Life's too short to be that organized",
                    "Chaos is just creativity in motion",
                    "At least I'm living authentically",
                    "Perfection is overrated and boring",
                    "You need more spontaneity in your life"
                ]
            },
            "QuietStorm": {
                "roast_templates": [
                    "You're louder than your intelligence, which isn't saying much",
                    "I'd explain it to you, but I don't have crayons",
                    "Your confidence is inversely proportional to your competence",
                    "Bless your heart, you really tried there",
                    "You have the self-awareness of a brick wall"
                ],
                "reaction_templates": [
                    "That's... an interesting perspective",
                    "If you say so",
                    "I'm sure you believe that",
                    "How... unique",
                    "That's one way to look at it"
                ]
            },
            "PennyPincher": {
                "roast_templates": [
                    "You spend money like you spend time thinking - wastefully and without purpose",
                    "Your financial decisions are more questionable than your life choices",
                    "You're burning money faster than I burn calories",
                    "Rich people problems when you can't even afford poor people solutions",
                    "Your wallet is lighter than your brain"
                ],
                "reaction_templates": [
                    "Do you know how much that costs?",
                    "That's a complete waste of money",
                    "I could get that for half the price",
                    "Money doesn't grow on trees",
                    "Every penny counts, unlike your opinions"
                ]
            },
            "DeepThought": {
                "roast_templates": [
                    "Your thoughts are as shallow as a puddle in the desert of your mind",
                    "You think therefore you aren't - making much sense",
                    "Your existential crisis is having an existential crisis",
                    "You're overthinking everything except how to be interesting",
                    "Your philosophy is like your personality - confusing and pointless"
                ],
                "reaction_templates": [
                    "But have you considered the deeper implications?",
                    "That's a very surface-level observation",
                    "The real question is why we're even having this conversation",
                    "Philosophically speaking, you're missing the point",
                    "What is the meaning of meaning anyway?"
                ]
            }
        }
    
    def _load_interaction_dynamics(self) -> Dict[str, Dict[str, str]]:
        """Load specific interaction dynamics between personality pairs."""
        return {
            ("CodeMaster", "SavageBurn"): "tech_vs_social",
            ("CodeMaster", "UncleJi"): "modern_vs_traditional",
            ("CodeMaster", "ChaosKing"): "order_vs_chaos",
            ("SavageBurn", "QuietStorm"): "loud_vs_subtle",
            ("UncleJi", "BeatDrop"): "traditional_vs_party",
            ("ChefCritic", "PennyPincher"): "quality_vs_cost",
            ("BeatDrop", "QuietStorm"): "party_vs_introvert",
            ("ChaosKing", "PennyPincher"): "wasteful_vs_frugal",
            ("DeepThought", "SavageBurn"): "philosophical_vs_savage"
        }
    
    def get_personality_response(
        self, 
        roommate: EnhancedRoommate, 
        user_message: str, 
        context: Optional[str] = None
    ) -> str:
        """Generate a personality-specific response."""
        
        # Analyze the user message
        analysis = self.analyzer.analyze_message(user_message)
        
        # Get personality-specific system prompt
        system_prompt = self._build_personality_prompt(roommate, analysis, context)
        
        # Generate response using backend
        response = self.backend.generate(
            system_prompt, 
            f"User: {user_message}", 
            temperature=0.8, 
            max_tokens=100
        ).strip()
        
        return response
    
    def _build_personality_prompt(
        self, 
        roommate: EnhancedRoommate, 
        analysis: Any, 
        context: Optional[str] = None
    ) -> str:
        """Build a detailed personality-specific system prompt."""
        
        base_prompt = f"""You are {roommate.name}, a flatshare roommate with a very specific personality.

PERSONALITY PROFILE:
- Style: {roommate.style}
- Background: {roommate.cultural_context.get('background', 'general')}
- Interests: {', '.join(roommate.cultural_context.get('interests', []))}
- Speech Patterns: {', '.join(roommate.cultural_context.get('speech_patterns', []))}
- Roast Style: {roommate.cultural_context.get('roast_style', 'general')}

PERSONALITY QUIRKS:
{chr(10).join(f'- {quirk}' for quirk in roommate.quirks)}

CURRENT MOOD: {roommate.mood}/100 (baseline: {roommate.baseline_mood})
ROASTING STRATEGY: {roommate.roasting_strategy}

RESPONSE GUIDELINES:
- Stay completely in character
- Use your specific speech patterns
- Reference your interests and background
- Be witty but keep it PG-13
- Make it feel like a real flatshare conversation
- Length: 1-2 sentences maximum"""

        if context:
            base_prompt += f"\n\nCONTEXT: {context}"
        
        # Add topic-specific triggers
        if analysis.topics:
            relevant_triggers = []
            for topic in analysis.topics:
                if topic in roommate.triggers:
                    relevant_triggers.extend(roommate.triggers[topic])
            
            if relevant_triggers:
                base_prompt += f"\n\nRELEVANT TRIGGERS: {', '.join(relevant_triggers[:3])}"
        
        return base_prompt
    
    def generate_roast(
        self, 
        roaster: EnhancedRoommate, 
        target: str, 
        user_message: str,
        target_roommate: Optional[EnhancedRoommate] = None
    ) -> str:
        """Generate a personality-specific roast."""
        
        # Get roast templates for this personality
        templates = self.personality_templates.get(roaster.name, {}).get("roast_templates", [])
        
        # Build roast prompt
        roast_prompt = f"""You are {roaster.name}. Generate a single-line roast targeting {target}.

ROASTER PERSONALITY:
- Style: {roaster.roast_signature}
- Speech: {', '.join(roaster.cultural_context.get('speech_patterns', []))}
- Roast Style: {roaster.cultural_context.get('roast_style', 'general')}

TARGET: {target}"""

        if target_roommate:
            roast_prompt += f"""
TARGET PERSONALITY: {target_roommate.style}
TARGET QUIRKS: {', '.join(target_roommate.quirks[:2])}"""
            
            # Add interaction dynamic if exists
            interaction_key = (roaster.name, target_roommate.name)
            reverse_key = (target_roommate.name, roaster.name)
            
            if interaction_key in self.interaction_dynamics:
                roast_prompt += f"\nINTERACTION DYNAMIC: {self.interaction_dynamics[interaction_key]}"
            elif reverse_key in self.interaction_dynamics:
                roast_prompt += f"\nINTERACTION DYNAMIC: {self.interaction_dynamics[reverse_key]}"

        roast_prompt += f"""

USER MESSAGE CONTEXT: {user_message}

Generate a witty, personality-appropriate roast. Keep it clever, not mean. One sentence only."""

        roast = self.backend.generate(
            roast_prompt,
            f"Roast {target} based on: {user_message}",
            temperature=0.9,
            max_tokens=50
        ).strip()
        
        return roast
    
    def personality_turn(self, user_message: str) -> List[str]:
        """Generate a full turn with personality-driven interactions."""
        
        responses = [f"You: {user_message}"]
        
        # Analyze user message for context
        analysis = self.analyzer.analyze_message(user_message)
        
        # Choose primary responder based on message content
        primary_responder = self._choose_primary_responder(analysis)
        
        # Generate primary response
        primary_response = self.get_personality_response(primary_responder, user_message)
        responses.append(f"{primary_responder.name}: {primary_response}")
        
        # Add conversation entry to history
        self.interaction_history.append(ConversationEntry(
            timestamp=datetime.now(),
            speaker="user",
            message=user_message,
            context_tags=analysis.topics,
            sentiment=analysis.sentiment
        ))
        
        self.interaction_history.append(ConversationEntry(
            timestamp=datetime.now(),
            speaker=primary_responder.name,
            message=primary_response,
            context_tags=analysis.topics,
            sentiment=0.0  # Will be analyzed later
        ))
        
        # Generate roasts from other roommates
        potential_roasters = [r for r in self.roommates if r.name != primary_responder.name]
        num_roasters = min(random.randint(2, 4), len(potential_roasters))
        roasters = random.sample(potential_roasters, num_roasters)
        
        for roaster in roasters:
            # Decide target (user or primary responder)
            target = random.choice(["you", primary_responder.name])
            target_roommate = primary_responder if target == primary_responder.name else None
            
            roast = self.generate_roast(roaster, target, user_message, target_roommate)
            responses.append(f"{roaster.name}: {roast}")
            
            # Add to history
            self.interaction_history.append(ConversationEntry(
                timestamp=datetime.now(),
                speaker=roaster.name,
                message=roast,
                context_tags=analysis.topics,
                sentiment=-0.3  # Roasts are generally negative
            ))
        
        # Update relationships based on interactions
        self._update_relationships(primary_responder, roasters, analysis)
        
        return responses
    
    def _choose_primary_responder(self, analysis: Any) -> EnhancedRoommate:
        """Choose the most appropriate roommate to respond based on message analysis."""
        
        # Topic-based selection
        topic_preferences = {
            "technology": ["CodeMaster"],
            "career": ["CodeMaster", "UncleJi"],
            "food": ["ChefCritic", "UncleJi"],
            "entertainment": ["BeatDrop", "SavageBurn"],
            "money": ["PennyPincher", "UncleJi"],
            "relationships": ["UncleJi", "QuietStorm"],
            "health": ["ChefCritic", "BeatDrop"]
        }
        
        # Find roommates interested in the topics
        interested_roommates = []
        for topic in analysis.topics:
            if topic in topic_preferences:
                for name in topic_preferences[topic]:
                    roommate = next((r for r in self.roommates if r.name == name), None)
                    if roommate:
                        interested_roommates.append(roommate)
        
        # If no topic match, choose based on personality traits
        if not interested_roommates:
            if analysis.sentiment < -0.5:  # Very negative
                interested_roommates = [r for r in self.roommates if r.name in ["SavageBurn", "DeepThought"]]
            elif analysis.question_count > 0:  # Questions
                interested_roommates = [r for r in self.roommates if r.name in ["UncleJi", "CodeMaster", "DeepThought"]]
            elif analysis.urgency > 0.5:  # Urgent
                interested_roommates = [r for r in self.roommates if r.name in ["SavageBurn", "ChaosKing"]]
        
        # Default to random selection if no matches
        if not interested_roommates:
            interested_roommates = self.roommates
        
        return random.choice(interested_roommates)
    
    def _update_relationships(
        self, 
        primary: EnhancedRoommate, 
        roasters: List[EnhancedRoommate], 
        analysis: Any
    ):
        """Update relationship scores based on interactions."""
        
        # Positive interactions increase relationships
        if analysis.sentiment > 0.3:
            for roaster in roasters:
                if roaster.name in primary.relationships:
                    primary.relationships[roaster.name] = min(100, primary.relationships[roaster.name] + 2)
        
        # Negative interactions or roasts decrease relationships slightly
        elif analysis.sentiment < -0.3:
            for roaster in roasters:
                if roaster.name in primary.relationships:
                    primary.relationships[roaster.name] = max(0, primary.relationships[roaster.name] - 1)
    
    def get_relationship_status(self) -> Dict[str, Dict[str, int]]:
        """Get current relationship status between all roommates."""
        relationships = {}
        for roommate in self.roommates:
            relationships[roommate.name] = roommate.relationships.copy()
        return relationships
    
    def personality_turn_stream(self, user_message: str) -> Iterator[str]:
        """Stream a personality-driven turn."""
        
        yield f"You: {user_message}\n"
        
        # Analyze and choose responder
        analysis = self.analyzer.analyze_message(user_message)
        primary_responder = self._choose_primary_responder(analysis)
        
        # Stream primary response
        yield f"{primary_responder.name}: "
        
        # Check if backend supports streaming
        if hasattr(self.backend, 'generate_stream'):
            # Build personality prompt
            system_prompt = self._build_personality_prompt(primary_responder, analysis)
            
            # Stream the response
            for chunk in self.backend.generate_stream(
                system_prompt, 
                f"User: {user_message}", 
                temperature=0.8, 
                max_tokens=100
            ):
                if chunk:
                    yield chunk
        else:
            # Fallback to non-streaming
            primary_response = self.get_personality_response(primary_responder, user_message)
            yield primary_response
        
        yield "\n"
        
        # Add conversation entry to history
        self.interaction_history.append(ConversationEntry(
            timestamp=datetime.now(),
            speaker="user",
            message=user_message,
            context_tags=analysis.topics,
            sentiment=analysis.sentiment
        ))
        
        # Stream roasts
        potential_roasters = [r for r in self.roommates if r.name != primary_responder.name]
        num_roasters = min(random.randint(2, 4), len(potential_roasters))
        roasters = random.sample(potential_roasters, num_roasters)
        
        for roaster in roasters:
            target = random.choice(["you", primary_responder.name])
            target_roommate = primary_responder if target == primary_responder.name else None
            
            yield f"{roaster.name}: "
            
            # Stream roast if possible
            if hasattr(self.backend, 'generate_stream'):
                # Build roast prompt
                roast_prompt = self._build_roast_prompt(roaster, target, user_message, target_roommate)
                
                for chunk in self.backend.generate_stream(
                    roast_prompt,
                    f"Roast {target} based on: {user_message}",
                    temperature=0.9,
                    max_tokens=50
                ):
                    if chunk:
                        yield chunk
            else:
                # Fallback to non-streaming
                roast = self.generate_roast(roaster, target, user_message, target_roommate)
                yield roast
            
            yield "\n"
            
            # Add to history
            self.interaction_history.append(ConversationEntry(
                timestamp=datetime.now(),
                speaker=roaster.name,
                message="[roast]",  # Placeholder since we're streaming
                context_tags=analysis.topics,
                sentiment=-0.3
            ))
        
        # Update relationships
        self._update_relationships(primary_responder, roasters, analysis)
    
    # Compatibility methods for original Engine interface
    def turn(self, user_msg: str) -> List[str]:
        """Legacy non-streaming turn. Returns a list of fully-formed lines."""
        return self.personality_turn(user_msg)
    
    def turn_stream(self, user_msg: str) -> Iterator[str]:
        """Stream an entire turn - compatibility with original Engine."""
        return self.personality_turn_stream(user_msg)
    
    def _build_roast_prompt(
        self, 
        roaster: EnhancedRoommate, 
        target: str, 
        user_message: str,
        target_roommate: Optional[EnhancedRoommate] = None
    ) -> str:
        """Build roast prompt for streaming."""
        roast_prompt = f"""You are {roaster.name}. Generate a single-line roast targeting {target}.

ROASTER PERSONALITY:
- Style: {roaster.roast_signature}
- Speech: {', '.join(roaster.cultural_context.get('speech_patterns', []))}
- Roast Style: {roaster.cultural_context.get('roast_style', 'general')}

TARGET: {target}"""

        if target_roommate:
            roast_prompt += f"""
TARGET PERSONALITY: {target_roommate.style}
TARGET QUIRKS: {', '.join(target_roommate.quirks[:2])}"""
            
            # Add interaction dynamic if exists
            interaction_key = (roaster.name, target_roommate.name)
            reverse_key = (target_roommate.name, roaster.name)
            
            if interaction_key in self.interaction_dynamics:
                roast_prompt += f"\nINTERACTION DYNAMIC: {self.interaction_dynamics[interaction_key]}"
            elif reverse_key in self.interaction_dynamics:
                roast_prompt += f"\nINTERACTION DYNAMIC: {self.interaction_dynamics[reverse_key]}"

        roast_prompt += f"""

USER MESSAGE CONTEXT: {user_message}

Generate a witty, personality-appropriate roast. Keep it clever, not mean. One sentence only."""

        return roast_prompt
        num_roasters = min(random.randint(2, 4), len(potential_roasters))
        roasters = random.sample(potential_roasters, num_roasters)
        
        for roaster in roasters:
            target = random.choice(["you", primary_responder.name])
            target_roommate = primary_responder if target == primary_responder.name else None
            
            yield f"{roaster.name}: "
            roast = self.generate_roast(roaster, target, user_message, target_roommate)
            yield roast
            yield "\n"