from typing import Dict, Tuple, List
from app.roommates import EnhancedRoommate


class RelationshipEngine:
    """Manages relationships and interactions between roommates."""
    
    def __init__(self):
        # Store relationships as (roommate1, roommate2) -> score
        # We use a consistent ordering to avoid duplicate entries
        self.relationship_matrix: Dict[Tuple[str, str], int] = {}
    
    def _get_relationship_key(self, roommate1: str, roommate2: str) -> Tuple[str, str]:
        """
        Get a consistent key for the relationship matrix.
        Always orders names alphabetically to avoid duplicate entries.
        """
        return tuple(sorted([roommate1, roommate2]))
    
    def update_relationship(self, roommate1: str, roommate2: str, delta: int) -> None:
        """
        Update relationship score between two roommates.
        
        Args:
            roommate1: Name of the first roommate
            roommate2: Name of the second roommate
            delta: Change in relationship score (positive or negative)
        """
        if roommate1 == roommate2:
            return  # Can't have relationship with self
        
        key = self._get_relationship_key(roommate1, roommate2)
        current_score = self.relationship_matrix.get(key, 50)  # Default neutral score
        
        # Update score and clamp to valid range (0-100)
        new_score = max(0, min(100, current_score + delta))
        self.relationship_matrix[key] = new_score
    
    def get_relationship_score(self, roommate1: str, roommate2: str) -> int:
        """
        Get current relationship score between two roommates.
        
        Args:
            roommate1: Name of the first roommate
            roommate2: Name of the second roommate
            
        Returns:
            Relationship score (0-100), defaults to 50 if no relationship exists
        """
        if roommate1 == roommate2:
            return 100  # Perfect relationship with self
        
        key = self._get_relationship_key(roommate1, roommate2)
        return self.relationship_matrix.get(key, 50)  # Default neutral score
    
    def should_defend(self, defender: str, target: str) -> bool:
        """
        Determine if defender should protect target from roasts.
        
        Args:
            defender: Name of the potential defender
            target: Name of the potential target to defend
            
        Returns:
            True if defender should defend target, False otherwise
        """
        if defender == target:
            return False  # Can't defend yourself
        
        relationship_score = self.get_relationship_score(defender, target)
        
        # Defend if relationship score is above 70
        return relationship_score > 70
    
    def get_roast_intensity_modifier(self, roaster: str, target: str) -> float:
        """
        Get intensity modifier based on relationship between roaster and target.
        
        Args:
            roaster: Name of the roommate doing the roasting
            target: Name of the target being roasted
            
        Returns:
            Intensity modifier (0.5 to 1.5):
            - Lower values for good relationships (gentler roasts)
            - Higher values for bad relationships (harsher roasts)
        """
        if roaster == target:
            return 1.0  # Normal intensity for self-roasts
        
        relationship_score = self.get_relationship_score(roaster, target)
        
        # Convert relationship score (0-100) to intensity modifier (0.5-1.5)
        # High relationship (80-100) -> Low intensity (0.5-0.7)
        # Medium relationship (40-60) -> Normal intensity (0.9-1.1)
        # Low relationship (0-20) -> High intensity (1.3-1.5)
        
        if relationship_score >= 80:
            # Very good relationship - gentle roasts
            return 0.5 + (relationship_score - 80) * 0.01  # 0.5 to 0.7
        elif relationship_score >= 60:
            # Good relationship - slightly gentle roasts
            return 0.7 + (relationship_score - 60) * 0.01  # 0.7 to 0.9
        elif relationship_score >= 40:
            # Neutral relationship - normal intensity
            return 0.9 + (relationship_score - 40) * 0.01  # 0.9 to 1.1
        elif relationship_score >= 20:
            # Poor relationship - harsher roasts
            return 1.1 + (40 - relationship_score) * 0.01  # 1.1 to 1.3
        else:
            # Very poor relationship - very harsh roasts
            return 1.3 + (20 - relationship_score) * 0.01  # 1.3 to 1.5
    
    def get_all_relationships(self, roommate_name: str) -> Dict[str, int]:
        """
        Get all relationships for a specific roommate.
        
        Args:
            roommate_name: Name of the roommate
            
        Returns:
            Dictionary mapping other roommate names to relationship scores
        """
        relationships = {}
        
        for (name1, name2), score in self.relationship_matrix.items():
            if name1 == roommate_name:
                relationships[name2] = score
            elif name2 == roommate_name:
                relationships[name1] = score
        
        return relationships
    
    def get_strongest_relationships(self, roommate_name: str, limit: int = 3) -> List[Tuple[str, int]]:
        """
        Get the strongest relationships for a roommate.
        
        Args:
            roommate_name: Name of the roommate
            limit: Maximum number of relationships to return
            
        Returns:
            List of tuples (other_roommate_name, relationship_score) sorted by score descending
        """
        relationships = self.get_all_relationships(roommate_name)
        
        # Sort by relationship score (descending)
        sorted_relationships = sorted(relationships.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_relationships[:limit]
    
    def get_weakest_relationships(self, roommate_name: str, limit: int = 3) -> List[Tuple[str, int]]:
        """
        Get the weakest relationships for a roommate.
        
        Args:
            roommate_name: Name of the roommate
            limit: Maximum number of relationships to return
            
        Returns:
            List of tuples (other_roommate_name, relationship_score) sorted by score ascending
        """
        relationships = self.get_all_relationships(roommate_name)
        
        # Sort by relationship score (ascending)
        sorted_relationships = sorted(relationships.items(), key=lambda x: x[1])
        
        return sorted_relationships[:limit]
    
    def simulate_interaction_outcome(
        self, 
        roommate1: str, 
        roommate2: str, 
        interaction_type: str,
        success: bool = True
    ) -> int:
        """
        Simulate the relationship change from an interaction.
        
        Args:
            roommate1: Name of the first roommate
            roommate2: Name of the second roommate
            interaction_type: Type of interaction ('roast', 'defend', 'compliment', 'joke')
            success: Whether the interaction was successful/well-received
            
        Returns:
            The relationship score change (delta)
        """
        if roommate1 == roommate2:
            return 0
        
        base_changes = {
            'roast': -3 if success else -1,  # Successful roasts hurt more
            'defend': 5 if success else 2,   # Successful defenses help more
            'compliment': 4 if success else 1,  # Successful compliments help
            'joke': 2 if success else -1,    # Good jokes help, bad jokes hurt
            'support': 3 if success else 1,  # Support always helps
            'conflict': -5 if success else -2  # Conflicts always hurt
        }
        
        delta = base_changes.get(interaction_type, 0)
        
        # Apply the change
        if delta != 0:
            self.update_relationship(roommate1, roommate2, delta)
        
        return delta
    
    def get_relationship_status(self, roommate1: str, roommate2: str) -> str:
        """
        Get a descriptive status of the relationship between two roommates.
        
        Args:
            roommate1: Name of the first roommate
            roommate2: Name of the second roommate
            
        Returns:
            String describing the relationship status
        """
        score = self.get_relationship_score(roommate1, roommate2)
        
        if score >= 90:
            return "best friends"
        elif score >= 80:
            return "close friends"
        elif score >= 70:
            return "good friends"
        elif score >= 60:
            return "friendly"
        elif score >= 40:
            return "neutral"
        elif score >= 30:
            return "tense"
        elif score >= 20:
            return "hostile"
        elif score >= 10:
            return "enemies"
        else:
            return "bitter enemies"
    
    def reset_relationship(self, roommate1: str, roommate2: str) -> None:
        """
        Reset relationship between two roommates to neutral (50).
        
        Args:
            roommate1: Name of the first roommate
            roommate2: Name of the second roommate
        """
        if roommate1 != roommate2:
            key = self._get_relationship_key(roommate1, roommate2)
            self.relationship_matrix[key] = 50
    
    def get_relationship_matrix_summary(self) -> Dict[str, Dict[str, int]]:
        """
        Get a summary of all relationships in matrix format.
        
        Returns:
            Nested dictionary where result[roommate1][roommate2] = relationship_score
        """
        summary = {}
        
        for (name1, name2), score in self.relationship_matrix.items():
            if name1 not in summary:
                summary[name1] = {}
            if name2 not in summary:
                summary[name2] = {}
            
            summary[name1][name2] = score
            summary[name2][name1] = score
        
        return summary