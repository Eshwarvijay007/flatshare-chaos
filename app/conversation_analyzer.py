from typing import List, Dict, Any, Optional
import re
from datetime import datetime, timedelta
from collections import Counter
from app.roommates import ConversationEntry, AnalysisResult, ConversationContext


class ConversationAnalyzer:
    """Analyzes conversations for patterns, sentiment, and context to enhance roasting intelligence."""
    
    def __init__(self):
        self.topic_keywords = self._load_topic_keywords()
        self.sentiment_indicators = self._load_sentiment_indicators()
        self.behavioral_patterns = self._load_behavioral_patterns()
    
    def _load_topic_keywords(self) -> Dict[str, List[str]]:
        """Load topic classification keywords."""
        return {
            "career": ["job", "work", "career", "boss", "office", "salary", "promotion", "interview", "resume"],
            "relationships": ["girlfriend", "boyfriend", "dating", "love", "crush", "relationship", "marriage", "single"],
            "food": ["eat", "food", "cook", "recipe", "restaurant", "hungry", "dinner", "lunch", "breakfast"],
            "technology": ["computer", "phone", "app", "software", "coding", "programming", "tech", "internet"],
            "health": ["gym", "exercise", "diet", "sick", "doctor", "medicine", "fitness", "workout"],
            "money": ["money", "expensive", "cheap", "budget", "broke", "rich", "cost", "price", "financial"],
            "education": ["school", "study", "exam", "college", "university", "degree", "learning", "homework"],
            "entertainment": ["movie", "music", "game", "tv", "show", "book", "party", "fun", "weekend"],
            "family": ["family", "parents", "mom", "dad", "sister", "brother", "relatives", "home"],
            "travel": ["travel", "vacation", "trip", "flight", "hotel", "visit", "explore", "journey"]
        }
    
    def _load_sentiment_indicators(self) -> Dict[str, List[str]]:
        """Load sentiment analysis indicators."""
        return {
            "positive": ["good", "great", "awesome", "amazing", "love", "happy", "excited", "wonderful", "fantastic", "excellent"],
            "negative": ["bad", "terrible", "awful", "hate", "sad", "angry", "frustrated", "disappointed", "worried", "stressed"],
            "uncertainty": ["maybe", "perhaps", "not sure", "i think", "probably", "might", "could be", "unsure"],
            "confidence": ["definitely", "absolutely", "certainly", "sure", "confident", "positive", "know", "obvious"],
            "questions": ["?", "what", "how", "why", "when", "where", "who", "which", "should i", "can you"]
        }
    
    def _load_behavioral_patterns(self) -> Dict[str, List[str]]:
        """Load behavioral pattern indicators."""
        return {
            "indecisive": ["i don't know", "not sure", "maybe", "what should i", "help me decide"],
            "complainer": ["always", "never", "everything", "nothing works", "so annoying", "hate when"],
            "perfectionist": ["perfect", "exactly", "precisely", "must be", "has to be", "should be"],
            "procrastinator": ["later", "tomorrow", "eventually", "when i have time", "putting off"],
            "overachiever": ["best", "top", "first", "win", "achieve", "goal", "success", "excel"],
            "social": ["friends", "people", "everyone", "party", "hang out", "meet up", "social"],
            "introvert": ["alone", "quiet", "by myself", "don't like crowds", "prefer", "stay in"]
        }
    
    def analyze_message(self, message: str) -> AnalysisResult:
        """
        Analyze message for topics, sentiment, and patterns.
        
        Args:
            message: The message to analyze
            
        Returns:
            AnalysisResult containing analysis findings
        """
        message_lower = message.lower()
        
        # Topic detection
        topics = self._detect_topics(message_lower)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(message_lower)
        
        # Urgency detection
        urgency = self._detect_urgency(message_lower)
        
        # Question count
        question_count = message.count('?') + len([word for word in self.sentiment_indicators["questions"] if word in message_lower])
        
        # Repeated phrases detection
        repeated_phrases = self._detect_repeated_phrases(message_lower)
        
        # Behavioral flags
        behavioral_flags = self._detect_behavioral_flags(message_lower)
        
        return AnalysisResult(
            topics=topics,
            sentiment=sentiment,
            urgency=urgency,
            question_count=question_count,
            repeated_phrases=repeated_phrases,
            behavioral_flags=behavioral_flags
        )
    
    def _detect_topics(self, message: str) -> List[str]:
        """Detect topics in the message."""
        detected_topics = []
        
        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    detected_topics.append(topic)
                    break
        
        return detected_topics
    
    def _analyze_sentiment(self, message: str) -> float:
        """
        Analyze sentiment of the message.
        
        Returns:
            Float between -1.0 (very negative) and 1.0 (very positive)
        """
        positive_count = sum(1 for word in self.sentiment_indicators["positive"] if word in message)
        negative_count = sum(1 for word in self.sentiment_indicators["negative"] if word in message)
        
        # Normalize by message length (word count)
        word_count = len(message.split())
        if word_count == 0:
            return 0.0
        
        positive_score = positive_count / word_count
        negative_score = negative_count / word_count
        
        # Calculate net sentiment
        net_sentiment = positive_score - negative_score
        
        # Clamp to [-1, 1] range
        return max(-1.0, min(1.0, net_sentiment * 10))  # Multiply by 10 to amplify the signal
    
    def _detect_urgency(self, message: str) -> float:
        """
        Detect urgency in the message.
        
        Returns:
            Float between 0.0 (no urgency) and 1.0 (high urgency)
        """
        urgency_indicators = [
            "urgent", "asap", "immediately", "now", "quick", "fast", "hurry", "emergency",
            "!!!", "help!", "need", "must", "have to", "should", "important"
        ]
        
        urgency_count = sum(1 for indicator in urgency_indicators if indicator in message)
        
        # Check for multiple exclamation marks
        if "!!!" in message or message.count("!") > 2:
            urgency_count += 2
        
        # Check for all caps words (indicates shouting/urgency)
        words = message.split()
        caps_words = sum(1 for word in words if word.isupper() and len(word) > 2)
        urgency_count += caps_words
        
        # Normalize and clamp
        return min(1.0, urgency_count / 5.0)
    
    def _detect_repeated_phrases(self, message: str) -> List[str]:
        """Detect repeated phrases in the message."""
        words = re.findall(r'\b\w+\b', message)
        
        # Look for 2-3 word phrases that appear multiple times
        phrases = []
        
        # 2-word phrases
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)
        
        # 3-word phrases
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            phrases.append(phrase)
        
        # Count occurrences and return phrases that appear more than once
        phrase_counts = Counter(phrases)
        repeated = [phrase for phrase, count in phrase_counts.items() if count > 1]
        
        return repeated[:5]  # Return top 5 repeated phrases
    
    def _detect_behavioral_flags(self, message: str) -> List[str]:
        """Detect behavioral patterns in the message."""
        flags = []
        
        for behavior, indicators in self.behavioral_patterns.items():
            for indicator in indicators:
                if indicator in message:
                    flags.append(behavior)
                    break
        
        return flags
    
    def detect_user_patterns(self, conversation_history: List[ConversationEntry]) -> Dict[str, Any]:
        """
        Identify user behavioral patterns from conversation history.
        
        Args:
            conversation_history: List of conversation entries to analyze
            
        Returns:
            Dictionary containing detected patterns
        """
        if not conversation_history:
            return {}
        
        user_messages = [entry for entry in conversation_history if entry.speaker == "user"]
        
        if not user_messages:
            return {}
        
        patterns = {}
        
        # Analyze all user messages
        all_topics = []
        all_sentiments = []
        all_behavioral_flags = []
        all_phrases = []
        question_counts = []
        
        for entry in user_messages:
            analysis = self.analyze_message(entry.message)
            all_topics.extend(analysis.topics)
            all_sentiments.append(analysis.sentiment)
            all_behavioral_flags.extend(analysis.behavioral_flags)
            all_phrases.extend(analysis.repeated_phrases)
            question_counts.append(analysis.question_count)
        
        # Topic frequency analysis
        topic_counts = Counter(all_topics)
        patterns["dominant_topics"] = dict(topic_counts.most_common(5))
        
        # Sentiment patterns
        if all_sentiments:
            patterns["average_sentiment"] = sum(all_sentiments) / len(all_sentiments)
            patterns["sentiment_volatility"] = self._calculate_volatility(all_sentiments)
        
        # Behavioral pattern frequency
        behavior_counts = Counter(all_behavioral_flags)
        patterns["behavioral_tendencies"] = dict(behavior_counts.most_common(3))
        
        # Communication style analysis
        avg_message_length = sum(len(entry.message) for entry in user_messages) / len(user_messages)
        patterns["communication_style"] = self._classify_communication_style(avg_message_length)
        
        # Question asking frequency
        total_questions = sum(question_counts)
        patterns["question_frequency"] = total_questions / len(user_messages) if user_messages else 0
        
        # Response time patterns (if timestamps are available)
        patterns["response_patterns"] = self._analyze_response_patterns(user_messages)
        
        # Conversation initiation patterns
        patterns["conversation_starters"] = self._analyze_conversation_starters(user_messages)
        
        return patterns
    
    def _calculate_volatility(self, sentiments: List[float]) -> float:
        """Calculate sentiment volatility (how much sentiment varies)."""
        if len(sentiments) < 2:
            return 0.0
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        variance = sum((s - avg_sentiment) ** 2 for s in sentiments) / len(sentiments)
        return variance ** 0.5  # Standard deviation
    
    def _classify_communication_style(self, avg_length: float) -> str:
        """Classify communication style based on message length."""
        if avg_length < 20:
            return "terse"
        elif avg_length < 50:
            return "concise"
        elif avg_length < 100:
            return "moderate"
        elif avg_length < 200:
            return "verbose"
        else:
            return "extremely_verbose"
    
    def _analyze_response_patterns(self, user_messages: List[ConversationEntry]) -> Dict[str, Any]:
        """Analyze response timing patterns."""
        if len(user_messages) < 2:
            return {}
        
        # Calculate time gaps between messages
        time_gaps = []
        for i in range(1, len(user_messages)):
            gap = user_messages[i].timestamp - user_messages[i-1].timestamp
            time_gaps.append(gap.total_seconds())
        
        if not time_gaps:
            return {}
        
        avg_gap = sum(time_gaps) / len(time_gaps)
        
        patterns = {
            "average_response_time_seconds": avg_gap,
            "response_speed": "fast" if avg_gap <= 30 else "moderate" if avg_gap <= 300 else "slow"
        }
        
        # Analyze active hours
        hours = [msg.timestamp.hour for msg in user_messages]
        hour_counts = Counter(hours)
        most_active_hour = hour_counts.most_common(1)[0][0] if hour_counts else 12
        
        if 6 <= most_active_hour <= 12:
            patterns["most_active_period"] = "morning"
        elif 12 <= most_active_hour <= 18:
            patterns["most_active_period"] = "afternoon"
        else:
            patterns["most_active_period"] = "evening"
        
        return patterns
    
    def _analyze_conversation_starters(self, user_messages: List[ConversationEntry]) -> List[str]:
        """Analyze how the user typically starts conversations."""
        if not user_messages:
            return []
        
        # Look at first words/phrases of messages
        starters = []
        for msg in user_messages:
            # Clean the message by removing punctuation
            clean_message = re.sub(r'[^\w\s]', '', msg.message)
            words = clean_message.split()
            if words:
                first_word = words[0].lower()
                if len(words) > 1:
                    first_phrase = f"{words[0]} {words[1]}".lower()
                    starters.append(first_phrase)
                else:
                    starters.append(first_word)
        
        starter_counts = Counter(starters)
        # Return starters that appear more than once, or if none repeat, return the most common ones
        repeated_starters = [starter for starter, count in starter_counts.most_common(5) if count > 1]
        if repeated_starters:
            return repeated_starters
        else:
            # If no repeats, return top starters anyway (for single occurrence patterns)
            return [starter for starter, count in starter_counts.most_common(3)]
    
    def get_conversation_context(self, recent_messages: List[ConversationEntry]) -> ConversationContext:
        """
        Build context from recent conversation.
        
        Args:
            recent_messages: List of recent conversation entries
            
        Returns:
            ConversationContext object with conversation state
        """
        if not recent_messages:
            return ConversationContext(
                current_topic="general",
                participants=[],
                topic_history=[],
                emotional_tone="neutral",
                thread_length=0
            )
        
        # Analyze recent messages for topics
        all_topics = []
        participants = set()
        sentiments = []
        
        for entry in recent_messages:
            analysis = self.analyze_message(entry.message)
            all_topics.extend(analysis.topics)
            participants.add(entry.speaker)
            sentiments.append(analysis.sentiment)
        
        # Determine current topic (most recent or most frequent)
        if all_topics:
            topic_counts = Counter(all_topics)
            current_topic = topic_counts.most_common(1)[0][0]
        else:
            current_topic = "general"
        
        # Build topic history (chronological order of topics)
        topic_history = []
        for entry in recent_messages:
            analysis = self.analyze_message(entry.message)
            if analysis.topics and (not topic_history or analysis.topics[0] != topic_history[-1]):
                topic_history.append(analysis.topics[0])
        
        # Determine emotional tone
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            if avg_sentiment > 0.3:
                emotional_tone = "positive"
            elif avg_sentiment < -0.3:
                emotional_tone = "negative"
            else:
                emotional_tone = "neutral"
        else:
            emotional_tone = "neutral"
        
        return ConversationContext(
            current_topic=current_topic,
            participants=list(participants),
            topic_history=topic_history[-5:],  # Keep last 5 topic changes
            emotional_tone=emotional_tone,
            thread_length=len(recent_messages)
        )
    
    def calculate_roast_effectiveness(
        self, 
        roast: str, 
        user_response: str, 
        response_time: float
    ) -> float:
        """
        Calculate how effective a roast was based on user response.
        
        Args:
            roast: The roast that was delivered
            user_response: The user's response to the roast
            response_time: Time in seconds between roast and response
            
        Returns:
            Effectiveness score between 0.0 and 1.0
        """
        if not user_response.strip():
            return 0.1  # No response is very low effectiveness
        
        effectiveness = 0.0
        
        # Response time factor (faster response often indicates engagement)
        if response_time < 10:
            time_factor = 0.3  # Very fast response
        elif response_time < 30:
            time_factor = 0.25  # Fast response
        elif response_time < 60:
            time_factor = 0.2   # Moderate response
        elif response_time < 300:
            time_factor = 0.15  # Slow response
        else:
            time_factor = 0.1   # Very slow response
        
        effectiveness += time_factor
        
        # Response length factor (longer responses often indicate engagement)
        response_length = len(user_response)
        if response_length > 100:
            length_factor = 0.25
        elif response_length > 50:
            length_factor = 0.2
        elif response_length > 20:
            length_factor = 0.15
        else:
            length_factor = 0.1
        
        effectiveness += length_factor
        
        # Sentiment analysis of response
        response_analysis = self.analyze_message(user_response)
        
        # Strong emotional response (positive or negative) indicates effectiveness
        sentiment_strength = abs(response_analysis.sentiment)
        effectiveness += sentiment_strength * 0.2
        
        # Defensive responses indicate the roast hit home
        defensive_indicators = [
            "that's not true", "whatever", "shut up", "you're wrong", 
            "i don't care", "so what", "and?", "your point?"
        ]
        
        response_lower = user_response.lower()
        defensive_count = sum(1 for indicator in defensive_indicators if indicator in response_lower)
        if defensive_count > 0:
            effectiveness += 0.15
        
        # Comeback attempts indicate engagement
        comeback_indicators = [
            "at least", "well you", "says the", "look who's talking",
            "that's rich coming from", "you're one to talk"
        ]
        
        comeback_count = sum(1 for indicator in comeback_indicators if indicator in response_lower)
        if comeback_count > 0:
            effectiveness += 0.1
        
        # Questions in response often indicate the roast was thought-provoking
        if response_analysis.question_count > 0:
            effectiveness += 0.05
        
        # Clamp to [0, 1] range
        return min(1.0, max(0.0, effectiveness))
    
    def analyze_roast_patterns(self, conversation_history: List[ConversationEntry]) -> Dict[str, Any]:
        """
        Analyze patterns in roasting effectiveness over time.
        
        Args:
            conversation_history: List of conversation entries including roasts
            
        Returns:
            Dictionary containing roast pattern analysis
        """
        roast_entries = [
            entry for entry in conversation_history 
            if entry.speaker != "user" and entry.effectiveness_score is not None
        ]
        
        if not roast_entries:
            return {}
        
        patterns = {}
        
        # Overall effectiveness
        effectiveness_scores = [entry.effectiveness_score for entry in roast_entries]
        patterns["average_effectiveness"] = sum(effectiveness_scores) / len(effectiveness_scores)
        patterns["effectiveness_trend"] = self._calculate_trend(effectiveness_scores)
        
        # Topic-based effectiveness
        topic_effectiveness = {}
        for entry in roast_entries:
            for tag in entry.context_tags:
                if tag not in topic_effectiveness:
                    topic_effectiveness[tag] = []
                topic_effectiveness[tag].append(entry.effectiveness_score)
        
        # Calculate average effectiveness per topic
        for topic, scores in topic_effectiveness.items():
            topic_effectiveness[topic] = sum(scores) / len(scores)
        
        patterns["topic_effectiveness"] = topic_effectiveness
        
        # Time-based patterns
        patterns["roast_frequency"] = self._analyze_roast_frequency(roast_entries)
        
        return patterns
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate if values are trending up, down, or stable."""
        if len(values) < 3:
            return "insufficient_data"
        
        # Simple linear trend calculation
        n = len(values)
        x_sum = sum(range(n))
        y_sum = sum(values)
        xy_sum = sum(i * values[i] for i in range(n))
        x2_sum = sum(i * i for i in range(n))
        
        slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
        
        if slope > 0.05:
            return "improving"
        elif slope < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _analyze_roast_frequency(self, roast_entries: List[ConversationEntry]) -> Dict[str, Any]:
        """Analyze frequency patterns of roasts."""
        if len(roast_entries) < 2:
            return {}
        
        # Calculate time gaps between roasts
        time_gaps = []
        for i in range(1, len(roast_entries)):
            gap = roast_entries[i].timestamp - roast_entries[i-1].timestamp
            time_gaps.append(gap.total_seconds() / 60)  # Convert to minutes
        
        avg_gap = sum(time_gaps) / len(time_gaps)
        
        return {
            "average_gap_minutes": avg_gap,
            "roast_frequency": "high" if avg_gap < 5 else "moderate" if avg_gap < 15 else "low",
            "total_roasts": len(roast_entries)
        }