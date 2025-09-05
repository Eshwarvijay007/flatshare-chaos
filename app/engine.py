
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
            return "This is the start of the conversation."
        return "\n".join(self.conversation_history[-self.max_history:])

    def _add_to_history(self, message: str):
        self.conversation_history.append(message)
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def _get_provider(self) -> Any:
        return getattr(self, "adapter", None) or self.backend

    def _generate_stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 150,
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
        
        system_prompt = f"""You are {speaker.name}. You are in a conversation with your flatmates.

Your personality is as follows:
- Style: {speaker.style}
- Background: {speaker.cultural_context.get('background', 'N/A')}
- Interests: {', '.join(speaker.cultural_context.get('interests', []))}
- Speech Patterns: {', '.join(speaker.cultural_context.get('speech_patterns', []))}
- Conversational Goals: {', '.join(speaker.conversational_goals)}

Here is the recent conversation history:
{conversation_history}

Your task is to generate a response to the last message in the conversation. Your response should be in character, conversational, and should contribute to the ongoing discussion. You can agree, disagree, ask a question, tell a story, or even try to change the subject, but your response should be a natural continuation of the conversation."""

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

        num_speakers = random.randint(2, min(len(self.roommates), self.max_speakers_per_turn))
        speakers = random.sample(self.roommates, k=num_speakers)

        for speaker in speakers:
            for chunk in self._generate_response_stream(speaker):
                yield chunk
            yield "\n"

    def turn(self, user_msg: str) -> List[str]:
        # Non-streaming version for compatibility
        lines = [f"You: {user_msg}"]
        self._add_to_history(f"You: {user_msg}")

        num_speakers = random.randint(2, min(len(self.roommates), self.max_speakers_per_turn))
        speakers = random.sample(self.roommates, k=num_speakers)

        for speaker in speakers:
            # This is a simplified, non-streaming version of _generate_response_stream
            conversation_history = self._build_conversation_history()
            system_prompt = f"""You are {speaker.name}. You are in a conversation with your flatmates.

Your personality is as follows:
- Style: {speaker.style}
- Background: {speaker.cultural_context.get('background', 'N/A')}
- Interests: {', '.join(speaker.cultural_context.get('interests', []))}
- Speech Patterns: {', '.join(speaker.cultural_context.get('speech_patterns', []))}
- Conversational Goals: {', '.join(speaker.conversational_goals)}

Here is the recent conversation history:
{conversation_history}

Your task is to generate a response to the last message in the conversation. Your response should be in character, conversational, and should contribute to the ongoing discussion."""
            user_prompt = "Based on the conversation history, what is your response?"
            
            provider = self._get_provider()
            response_text = provider.generate(system_prompt, user_prompt, 0.7, 150)
            
            line = f"{speaker.name}: {response_text}"
            lines.append(line)
            self._add_to_history(line)
            
        return lines
