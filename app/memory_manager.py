from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter
import re
from app.roommates import EnhancedRoommate, ConversationEntry


class MemoryManager:
    """Manages conversation memory and user pattern analysis for enhanced roommates."""
    
    def __init__(self, max_memory_size: int = 50):
        self.max_memory_size = max_memory_size
    
    def add_conversation(self, roommate: EnhancedRoommate, entry: ConversationEntry) -> None:
        """
        Add conversation entry and manage memory size.
        
        Args:
            roommate: The roommate to add memory to
            entry: The conversation entry to add
        """
        roommate.conversation_memory.append(entry)
        
        # Manage memory size - remove oldest entries if exceeding limit
        if len(roommate.conversation_memory) > self.max_memory_size:
            entries_to_remove = len(roommate.conversation_memory) - self.max_memory_size
            
            # If we have more than 10 entries, preserve the 10 most recent and 
            # remove the least effective from the older entries
            if len(roommate.conversation_memory) > 10:
                # Keep the 10 most recent entries untouched
                recent_entries = roommate.conversation_memory[-10:]
                older_entries = roommate.conversation_memory[:-10]
                
                # Sort older entries by effectiveness (lowest first for removal)
                older_entries.sort(key=lambda x: x.effectiveness_score or 0.0)
                
                # Remove the least effective older entries
                entries_to_keep = len(older_entries) - entries_to_remove
                if entries_to_keep > 0:
                    kept_older_entries = older_entries[-entries_to_keep:]
                else:
                    kept_older_entries = []
                
                # Rebuild memory with kept older entries + recent entries
                roommate.conversation_memory = kept_older_entries + recent_entries
            else:
                # If we have 10 or fewer entries, just remove the oldest
                roommate.conversation_memory = roommate.conversation_memory[-self.max_memory_size:]
    
    def get_relevant_context(
        self, 
        roommate: EnhancedRoommate, 
        current_topic: str, 
        limit: int = 10
    ) -> List[ConversationEntry]:
        """
        Retrieve contextually relevant conversation history.
        
        Args:
            roommate: The roommate whose memory to search
            current_topic: The current conversation topic to find relevant context for
            limit: Maximum number of entries to return
            
        Returns:
            List of relevant conversation entries, most recent first
        """
        if not roommate.conversation_memory:
            return []
        
        # Score entries based on relevance to current topic
        scored_entries = []
        current_topic_lower = current_topic.lower()
        
        for entry in roommate.conversation_memory:
            score = 0.0
            
            # Recent entries get higher scores
            days_ago = (datetime.now() - entry.timestamp).days
            recency_score = max(0, 1.0 - (days_ago / 7))  # Decay over a week
            score += recency_score * 0.3
            
            # Topic relevance
            message_lower = entry.message.lower()
            if current_topic_lower in message_lower:
                score += 1.0
            
            # Context tag relevance
            for tag in entry.context_tags:
                if tag.lower() in current_topic_lower or current_topic_lower in tag.lower():
                    score += 0.5
            
            # Effectiveness bonus
            if entry.effectiveness_score and entry.effectiveness_score > 0.7:
                score += 0.2
            
            scored_entries.append((score, entry))
        
        # Sort by score (descending) and return top entries
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored_entries[:limit]]
    
    def analyze_user_patterns(self, roommate: EnhancedRoommate) -> Dict[str, Any]:
        """
        Analyze user behavior patterns from conversation history.
        
        Args:
            roommate: The roommate whose memory to analyze
            
        Returns:
            Dictionary containing user behavior patterns
        """
        if not roommate.conversation_memory:
            return {}
        
        user_messages = [
            entry for entry in roommate.conversation_memory 
            if entry.speaker == "user"
        ]
        
        if not user_messages:
            return {}
        
        patterns = {}
        
        # Analyze frequent topics from context tags
        all_tags = []
        for entry in user_messages:
            all_tags.extend(entry.context_tags)
        
        tag_counts = Counter(all_tags)
        patterns["frequent_topics"] = dict(tag_counts.most_common(10))
        
        # Analyze speech patterns
        all_messages = [entry.message for entry in user_messages]
        all_text = " ".join(all_messages).lower()
        
        # Common phrases (2-3 words that appear frequently)
        words = re.findall(r'\b\w+\b', all_text)
        phrases = []
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        phrase_counts = Counter(phrases)
        common_phrases = [phrase for phrase, count in phrase_counts.most_common(5) if count > 1]
        patterns["speech_patterns"] = common_phrases
        
        # Response style analysis
        avg_length = sum(len(msg.message) for msg in user_messages) / len(user_messages)
        if avg_length > 100:
            patterns["response_style"] = "lengthy_responses"
        elif avg_length < 20:
            patterns["response_style"] = "brief_responses"
        else:
            patterns["response_style"] = "moderate_responses"
        
        # Sentiment analysis
        sentiments = [entry.sentiment for entry in user_messages if entry.sentiment is not None]
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            patterns["average_sentiment"] = avg_sentiment
            patterns["roast_sensitivity"] = max(0.1, 1.0 - abs(avg_sentiment))
        
        # Interaction timing patterns
        timestamps = [entry.timestamp for entry in user_messages]
        if len(timestamps) > 1:
            hours = [ts.hour for ts in timestamps]
            hour_counts = Counter(hours)
            most_active_hour = hour_counts.most_common(1)[0][0]
            
            if 6 <= most_active_hour <= 12:
                patterns["preferred_interaction_time"] = "morning"
            elif 12 <= most_active_hour <= 18:
                patterns["preferred_interaction_time"] = "afternoon"
            else:
                patterns["preferred_interaction_time"] = "evening"
        
        # Question frequency
        question_count = sum(1 for msg in user_messages if "?" in msg.message)
        patterns["question_frequency"] = question_count / len(user_messages) if user_messages else 0
        
        # Update roommate's user patterns
        roommate.user_patterns.update(patterns)
        
        return patterns
    
    def get_conversation_thread(
        self, 
        roommate: EnhancedRoommate, 
        turns: int = 5
    ) -> List[ConversationEntry]:
        """
        Get recent conversation thread for context.
        
        Args:
            roommate: The roommate whose memory to search
            turns: Number of recent conversation turns to retrieve
            
        Returns:
            List of recent conversation entries, chronologically ordered
        """
        if not roommate.conversation_memory:
            return []
        
        # Return the most recent entries, up to the specified number of turns
        recent_entries = roommate.conversation_memory[-turns:]
        return recent_entries
    
    def clear_old_memories(
        self, 
        roommate: EnhancedRoommate, 
        days_threshold: int = 30
    ) -> int:
        """
        Clear memories older than the specified threshold.
        
        Args:
            roommate: The roommate whose memory to clean
            days_threshold: Number of days after which to remove memories
            
        Returns:
            Number of memories removed
        """
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        original_count = len(roommate.conversation_memory)
        roommate.conversation_memory = [
            entry for entry in roommate.conversation_memory
            if entry.timestamp > cutoff_date
        ]
        
        removed_count = original_count - len(roommate.conversation_memory)
        return removed_count
    
    def get_memory_stats(self, roommate: EnhancedRoommate) -> Dict[str, Any]:
        """
        Get statistics about the roommate's memory.
        
        Args:
            roommate: The roommate whose memory to analyze
            
        Returns:
            Dictionary containing memory statistics
        """
        if not roommate.conversation_memory:
            return {
                "total_entries": 0,
                "user_messages": 0,
                "roommate_messages": 0,
                "oldest_entry": None,
                "newest_entry": None,
                "average_effectiveness": 0.0
            }
        
        user_messages = sum(1 for entry in roommate.conversation_memory if entry.speaker == "user")
        roommate_messages = len(roommate.conversation_memory) - user_messages
        
        timestamps = [entry.timestamp for entry in roommate.conversation_memory]
        oldest_entry = min(timestamps)
        newest_entry = max(timestamps)
        
        effectiveness_scores = [
            entry.effectiveness_score for entry in roommate.conversation_memory
            if entry.effectiveness_score is not None
        ]
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0.0
        
        return {
            "total_entries": len(roommate.conversation_memory),
            "user_messages": user_messages,
            "roommate_messages": roommate_messages,
            "oldest_entry": oldest_entry,
            "newest_entry": newest_entry,
            "average_effectiveness": avg_effectiveness
        }