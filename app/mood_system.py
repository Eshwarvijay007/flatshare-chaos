from typing import Dict, List
from datetime import datetime, timedelta
import random
from app.roommates import EnhancedRoommate


class MoodSystem:
    """Manages dynamic mood tracking and behavioral influence for roommates."""
    
    def __init__(self, mood_decay_rate: float = 0.1):
        """
        Initialize the mood system.
        
        Args:
            mood_decay_rate: Rate at which moods decay per minute toward baseline
        """
        self.mood_decay_rate = mood_decay_rate
        self.last_decay_time = datetime.now()
    
    def update_mood(self, roommate: EnhancedRoommate, event_type: str, intensity: int) -> None:
        """
        Update roommate mood based on events.
        
        Args:
            roommate: The roommate whose mood to update
            event_type: Type of event ('roast_received', 'roast_successful', 'defended', 'complimented')
            intensity: Intensity of the mood change (1-10)
        """
        mood_changes = {
            'roast_received': -intensity,
            'roast_successful': intensity // 2,
            'defended': intensity,
            'complimented': intensity,
            'ignored': -intensity // 3,
            'praised': intensity,
            'criticized': -intensity,
            'supported': intensity // 2
        }
        
        delta = mood_changes.get(event_type, 0)
        
        # Apply mood change with clamping
        new_mood = max(1, min(100, roommate.mood + delta))
        roommate.mood = new_mood
    
    def get_mood_modifier(self, roommate: EnhancedRoommate) -> Dict[str, float]:
        """
        Get behavioral modifiers based on current mood.
        
        Args:
            roommate: The roommate to get modifiers for
            
        Returns:
            Dictionary with behavioral modifiers
        """  
      modifiers = {
            'aggression': 1.0,
            'humor': 1.0,
            'defensiveness': 1.0,
            'roast_likelihood': 1.0,
            'response_length': 1.0
        }
        
        mood = roommate.mood
        
        if mood < 30:
            # Low mood - more aggressive, defensive, likely to roast
            modifiers['aggression'] = 1.5
            modifiers['defensiveness'] = 1.3
            modifiers['roast_likelihood'] = 1.4
            modifiers['humor'] = 0.7
            modifiers['response_length'] = 0.8
        elif mood < 50:
            # Below average mood - slightly more aggressive
            modifiers['aggression'] = 1.2
            modifiers['defensiveness'] = 1.1
            modifiers['roast_likelihood'] = 1.2
            modifiers['humor'] = 0.9
        elif mood > 80:
            # High mood - more playful, less harsh
            modifiers['aggression'] = 0.6
            modifiers['defensiveness'] = 0.8
            modifiers['roast_likelihood'] = 0.7
            modifiers['humor'] = 1.3
            modifiers['response_length'] = 1.2
        elif mood > 60:
            # Above average mood - slightly more positive
            modifiers['aggression'] = 0.8
            modifiers['roast_likelihood'] = 0.9
            modifiers['humor'] = 1.1
        
        return modifiers
    
    def decay_moods(self, roommates: List[EnhancedRoommate], minutes_passed: float) -> None:
        """
        Gradually return moods to baseline.
        
        Args:
            roommates: List of roommates to update
            minutes_passed: Number of minutes since last decay
        """
        decay_amount = self.mood_decay_rate * minutes_passed
        
        for roommate in roommates:
            current_mood = roommate.mood
            baseline = roommate.baseline_mood
            
            if current_mood > baseline:
                # Mood is above baseline, decay downward
                new_mood = max(baseline, current_mood - decay_amount)
            elif current_mood < baseline:
                # Mood is below baseline, decay upward
                new_mood = min(baseline, current_mood + decay_amount)
            else:
                # Already at baseline
                new_mood = baseline
            
            roommate.mood = int(new_mood)
    
    def should_initiate_roast(self, roommate: EnhancedRoommate) -> bool:
        """
        Determine if low mood should trigger aggressive behavior.
        
        Args:
            roommate: The roommate to check
            
        Returns:
            True if roommate should initiate a roast due to mood
        """
        if roommate.mood >= 30:
            return False
        
        # Lower mood = higher chance of initiating roast
        # Mood 1-29: 10-40% chance
        base_chance = (30 - roommate.mood) / 30 * 0.4
        
        # Add some randomness
        return random.random() < base_chance   
 
    def get_mood_description(self, roommate: EnhancedRoommate) -> str:
        """
        Get a descriptive string for the roommate's current mood.
        
        Args:
            roommate: The roommate to describe
            
        Returns:
            String describing the current mood
        """
        mood = roommate.mood
        
        if mood >= 90:
            return "ecstatic"
        elif mood >= 80:
            return "very happy"
        elif mood >= 70:
            return "happy"
        elif mood >= 60:
            return "content"
        elif mood >= 50:
            return "neutral"
        elif mood >= 40:
            return "slightly annoyed"
        elif mood >= 30:
            return "irritated"
        elif mood >= 20:
            return "angry"
        elif mood >= 10:
            return "furious"
        else:
            return "livid"
    
    def auto_decay_check(self, roommates: List[EnhancedRoommate]) -> None:
        """
        Automatically check and apply mood decay if enough time has passed.
        
        Args:
            roommates: List of roommates to potentially decay
        """
        now = datetime.now()
        time_diff = now - self.last_decay_time
        minutes_passed = time_diff.total_seconds() / 60.0
        
        # Only decay if at least 1 minute has passed
        if minutes_passed >= 1.0:
            self.decay_moods(roommates, minutes_passed)
            self.last_decay_time = now
    
    def get_mood_influence_on_roast(self, roommate: EnhancedRoommate) -> Dict[str, any]:
        """
        Get specific influences mood has on roasting behavior.
        
        Args:
            roommate: The roommate to analyze
            
        Returns:
            Dictionary with roasting behavior influences
        """
        mood = roommate.mood
        modifiers = self.get_mood_modifier(roommate)
        
        influences = {
            'should_roast_more': mood < 30,
            'roast_intensity': modifiers['aggression'],
            'humor_level': modifiers['humor'],
            'target_selection': 'enemies' if mood < 30 else 'random',
            'response_style': 'aggressive' if mood < 30 else 'playful' if mood > 80 else 'normal'
        }
        
        return influences
    
    def simulate_mood_event(
        self, 
        roommate: EnhancedRoommate, 
        event_description: str,
        mood_impact: int
    ) -> Dict[str, any]:
        """
        Simulate a mood-affecting event and return the results.
        
        Args:
            roommate: The roommate affected
            event_description: Description of what happened
            mood_impact: Direct mood change (-10 to +10)
            
        Returns:
            Dictionary with event results
        """
        old_mood = roommate.mood
        old_description = self.get_mood_description(roommate)
        
        # Apply mood change
        roommate.mood = max(1, min(100, roommate.mood + mood_impact))
        
        new_mood = roommate.mood
        new_description = self.get_mood_description(roommate)
        
        return {
            'event': event_description,
            'mood_change': new_mood - old_mood,
            'old_mood': old_mood,
            'new_mood': new_mood,
            'old_description': old_description,
            'new_description': new_description,
            'behavioral_change': old_description != new_description
        }