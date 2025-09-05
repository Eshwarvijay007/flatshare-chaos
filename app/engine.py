from __future__ import annotations
import random
from typing import Iterator, List, Any

try:
    from app.roommates import EnhancedRoommate as Roommate
except ImportError:
    # Fallback for linters if the path is not recognized
    from roommates import EnhancedRoommate as Roommate

class Engine:
    def __init__(
        self,
        roommates: List[Roommate],
        backend: Any,
        spice: int = 2, # Kept for compatibility, but not used in the new engine
        max_roasts_per_turn: int = 4, # Interpreted as max speakers per turn
    ):
        self.roommates = roommates
        self.backend = backend
        self.max_speakers_per_turn = max_roasts_per_turn
        self.conversation_history: List[str] = []
        self.max_history = 10

    def _build_conversation_history(self) -> str:
        if not self.conversation_history:
            return "You're hanging out with your flatmates. Respond naturally to their greeting."
        return "\n".join(self.conversation_history[-self.max_history:])

    def _add_to_history(self, message: str):
        self.conversation_history.append(message)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def _get_provider(self) -> Any:
        return getattr(self, "adapter", None) or self.backend

    def _select_speakers(self, user_msg: str) -> List[Roommate]:
        """Selects speakers for the turn based on the user's message."""
        
        mentioned_roommates = []
        triggered_roommates = []
        other_roommates = list(self.roommates)

        lower_user_msg = user_msg.lower()

        # Prioritize mentioned roommates
        for r in self.roommates:
            if r.name.lower() in lower_user_msg:
                mentioned_roommates.append(r)
                if r in other_roommates:
                    other_roommates.remove(r)
        
        # Then, consider triggered roommates
        if not mentioned_roommates:
            for r in self.roommates:
                if hasattr(r, 'triggers'):
                    for trigger_key, trigger_phrases in r.triggers.items():
                        for phrase in trigger_phrases:
                            if phrase.lower() in lower_user_msg:
                                if r not in triggered_roommates:
                                    triggered_roommates.append(r)
                                if r in other_roommates:
                                    other_roommates.remove(r)
        
        speakers = mentioned_roommates + triggered_roommates
        
        # Add some random other roommates to the conversation
        num_remaining_speakers = min(len(other_roommates), self.max_speakers_per_turn - len(speakers))
        if num_remaining_speakers > 0:
            speakers.extend(random.sample(other_roommates, k=num_remaining_speakers))
            
        # If no one is mentioned or triggered, select random speakers
        if not speakers:
            num_speakers = random.randint(2, min(len(self.roommates), self.max_speakers_per_turn))
            speakers = random.sample(self.roommates, k=num_speakers)

        return speakers

    def _generate_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 100, # Reduced max_tokens for more concise responses
    ) -> Iterator[str]:
        provider = self._get_provider()
        if hasattr(provider, "generate_stream"):
            yield from provider.generate_stream(system_prompt, user_prompt, temperature, max_tokens)
        else:
            text = provider.generate(system_prompt, user_prompt, temperature, max_tokens)
            if text:
                yield text

    def _generate_response_stream(self, speaker: Roommate) -> Iterator[str]:
        conversation_history = self._build_conversation_history()
        
        task_instruction = ""
        if "You're hanging out with your flatmates" in conversation_history:
            task_instruction = "Your task is to start the conversation in character, based on the user's first message. Keep your response to 2-3 sentences."
        else:
            task_instruction = "Your task is to generate a response to the last message in the conversation. Your response should be in character, conversational, and contribute to the ongoing discussion. Keep your response to 2-3 sentences."

        system_prompt = f"""You are {speaker.name}. You are in a conversation with your flatmates.

Your personality is as follows:
- Style: {speaker.style}
- Background: {speaker.cultural_context.get('background', 'N/A')}
- Interests: {', '.join(speaker.cultural_context.get('interests', []))}
- Speech Patterns: {', '.join(speaker.cultural_context.get('speech_patterns', []))}
- Conversational Goals: {', '.join(speaker.conversational_goals)}

Here is the recent conversation history:
{conversation_history}

{task_instruction}"""

        user_prompt = "Based on the conversation history, what is your response?"

        yield f"{speaker.name}: "
        
        response_parts = []
        for chunk in self._generate_stream(system_prompt, user_prompt):
            response_parts.append(chunk)
            yield chunk
        
        complete_response = f"{speaker.name}: {''.join(response_parts)}"
        self._add_to_history(complete_response)

    def turn_stream(self, user_msg: str) -> Iterator[str]:
        self._add_to_history(f"You: {user_msg}")
        yield f"You: {user_msg}\n"

        speakers = self._select_speakers(user_msg)

        for speaker in speakers:
            for chunk in self._generate_response_stream(speaker):
                yield chunk
            yield "\n"

    def turn(self, user_msg: str) -> List[str]:
        # Non-streaming version for compatibility
        lines = [f"You: {user_msg}"]
        self._add_to_history(f"You: {user_msg}")

        speakers = self._select_speakers(user_msg)

        for speaker in speakers:
            # This is a simplified, non-streaming version of _generate_response_stream
            conversation_history = self._build_conversation_history()
            
            task_instruction = ""
            if "You're hanging out with your flatmates" in conversation_history:
                task_instruction = "Your task is to start the conversation in character, based on the user's first message. Keep your response to 2-3 sentences."
            else:
                task_instruction = "Your task is to generate a response to the last message in the conversation. Your response should be in character, conversational, and contribute to the ongoing discussion. Keep your response to 2-3 sentences."

            system_prompt = f"""You are {speaker.name}. You are in a conversation with your flatmates.

Your personality is as follows:
- Style: {speaker.style}
- Background: {speaker.cultural_context.get('background', 'N/A')}
- Interests: {', '.join(speaker.cultural_context.get('interests', []))}
- Speech Patterns: {', '.join(speaker.cultural_context.get('speech_patterns', []))}
- Conversational Goals: {', '.join(speaker.conversational_goals)}

Here is the recent conversation history:
{conversation_history}

{task_instruction}"""
            user_prompt = "Based on the conversation history, what is your response?"
            
            provider = self._get_provider()
            response_text = provider.generate(system_prompt, user_prompt, 0.7, 100) # Reduced max_tokens
            
            line = f"{speaker.name}: {response_text}"
            lines.append(line)
            self._add_to_history(line)
            
        return lines
