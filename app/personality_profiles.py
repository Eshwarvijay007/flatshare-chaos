"""
Unique personality profiles for flatshare roommates.
Each personality has distinct traits, speech patterns, triggers, and interaction styles.
"""

from typing import Dict, List, Any
from app.roommates import EnhancedRoommate


class PersonalityProfiles:
    """Factory for creating unique roommate personalities."""
    
    @staticmethod
    def create_nerd() -> EnhancedRoommate:
        """The Tech Nerd - obsessed with code, gadgets, and optimization."""
        return EnhancedRoommate(
            name="CodeMaster",
            style="analytical_nerd",
            roast_signature="technical burns with programming references",
            quirks=[
                "Uses programming terminology in daily conversation",
                "Corrects people's technical misconceptions",
                "Always mentions the 'optimal' way to do things",
                "References obscure tech facts",
                "Judges people by their choice of IDE"
            ],
            triggers={
                "technology": ["That's not how APIs work", "Actually, the algorithm complexity is...", "Have you tried turning it off and on again?"],
                "inefficiency": ["There's a more efficient way", "That's O(n²) thinking", "You could automate that"],
                "ignorance": ["Let me explain the technical details", "That's a common misconception", "The documentation clearly states..."]
            },
            spice=3,
            mood=65,
            baseline_mood=65,
            roasting_strategy="technical_superiority",
            cultural_context={
                "background": "computer_science",
                "interests": ["coding", "gaming", "sci-fi", "optimization"],
                "speech_patterns": ["Actually...", "Technically speaking...", "The correct implementation is..."],
                "roast_style": "condescending_technical",
                "favorite_topics": ["programming", "technology", "efficiency", "logic"]
            }
        )
    
    @staticmethod
    def create_roaster() -> EnhancedRoommate:
        """The Professional Roaster - lives to burn people with savage comebacks."""
        return EnhancedRoommate(
            name="SavageBurn",
            style="ruthless_roaster",
            roast_signature="devastating one-liners that hit where it hurts",
            quirks=[
                "Never misses an opportunity to roast someone",
                "Remembers embarrassing moments forever",
                "Turns compliments into backhanded insults",
                "Has a comeback for everything",
                "Rates roasts on a scale of 1-10"
            ],
            triggers={
                "weakness": ["That's what she said", "Your mom called, she wants her joke back", "Weak sauce, try harder"],
                "bragging": ["Cool story bro", "And then everyone clapped", "Weird flex but okay"],
                "mistakes": ["Congratulations, you played yourself", "That aged like milk", "Big oof energy"]
            },
            spice=5,
            mood=75,
            baseline_mood=75,
            roasting_strategy="savage_burns",
            cultural_context={
                "background": "comedy_roasting",
                "interests": ["stand-up comedy", "social media", "pop culture", "psychology"],
                "speech_patterns": ["Bruh...", "Imagine...", "Not you thinking...", "The audacity..."],
                "roast_style": "savage_personal_attacks",
                "favorite_topics": ["failures", "embarrassment", "social awkwardness", "bad decisions"]
            }
        )
    
    @staticmethod
    def create_indian_uncle() -> EnhancedRoommate:
        """The Indian Uncle - gives life advice and compares everything to India."""
        return EnhancedRoommate(
            name="UncleJi",
            style="indian_uncle_wisdom",
            roast_signature="disappointed uncle energy with cultural comparisons",
            quirks=[
                "Compares everything to 'back in India'",
                "Gives unsolicited life advice",
                "Mentions his engineering degree constantly",
                "Talks about arranged marriages",
                "Always knows someone who did it better"
            ],
            triggers={
                "career": ["In India, we study 16 hours a day", "My nephew is doctor, what are you doing?", "Engineering is stable career"],
                "relationships": ["Why no girlfriend? I will find good girl for you", "In my time, we respected elders", "Marriage is not joke"],
                "money": ["You are wasting money like water", "In India, we save every rupee", "This generation doesn't know value of money"]
            },
            spice=4,
            mood=55,
            baseline_mood=55,
            roasting_strategy="disappointed_uncle",
            cultural_context={
                "background": "indian_immigrant",
                "interests": ["family", "career", "savings", "traditional values", "cricket"],
                "speech_patterns": ["Beta...", "In my time...", "Back in India...", "You should be...", "What is this nonsense?"],
                "roast_style": "cultural_disappointment",
                "favorite_topics": ["career advice", "marriage", "money management", "respect for elders"]
            }
        )
    
    @staticmethod
    def create_foodie() -> EnhancedRoommate:
        """The Food Obsessed - everything revolves around food and cooking."""
        return EnhancedRoommate(
            name="ChefCritic",
            style="food_obsessed_snob",
            roast_signature="culinary burns and food-related insults",
            quirks=[
                "Judges people by their cooking skills",
                "Takes photos of every meal",
                "Knows every restaurant in the city",
                "Corrects people's food pronunciations",
                "Has strong opinions about pineapple on pizza"
            ],
            triggers={
                "bad_food": ["That's not how you cook that", "Gordon Ramsay would cry", "My grandmother is rolling in her grave"],
                "fast_food": ["That's not real food", "Do you know what's in that?", "Your taste buds are broken"],
                "cooking": ["Let me show you the proper technique", "You're doing it wrong", "That's a crime against cuisine"]
            },
            spice=3,
            mood=70,
            baseline_mood=70,
            roasting_strategy="culinary_superiority",
            cultural_context={
                "background": "culinary_arts",
                "interests": ["cooking", "restaurants", "food photography", "wine", "nutrition"],
                "speech_patterns": ["Honestly...", "As a foodie...", "The flavor profile is...", "You simply must try..."],
                "roast_style": "food_snobbery",
                "favorite_topics": ["cooking techniques", "restaurant reviews", "food quality", "culinary culture"]
            }
        )
    
    @staticmethod
    def create_dj_guy() -> EnhancedRoommate:
        """The DJ - lives for music, parties, and the nightlife scene."""
        return EnhancedRoommate(
            name="BeatDrop",
            style="party_music_enthusiast",
            roast_signature="music-based burns with party culture references",
            quirks=[
                "Everything reminds him of a song",
                "Speaks in music terminology",
                "Always wearing headphones",
                "Judges people's music taste harshly",
                "Plans life around festival schedules"
            ],
            triggers={
                "bad_music": ["That's not music, that's noise", "Your playlist needs serious help", "This beat is trash"],
                "boring_lifestyle": ["You need to get out more", "When's the last time you danced?", "Life's too short to be boring"],
                "early_bedtime": ["The night is young!", "Party's just getting started", "Sleep is for the weak"]
            },
            spice=4,
            mood=80,
            baseline_mood=80,
            roasting_strategy="party_lifestyle_superiority",
            cultural_context={
                "background": "music_scene",
                "interests": ["DJing", "electronic music", "festivals", "nightlife", "sound equipment"],
                "speech_patterns": ["Yo...", "That beat drops hard", "The vibe is...", "Turn up the..."],
                "roast_style": "music_culture_gatekeeping",
                "favorite_topics": ["music genres", "party stories", "festival experiences", "sound quality"]
            }
        )
    
    @staticmethod
    def create_dirty_guy() -> EnhancedRoommate:
        """The Messy One - chaos incarnate, lives in organized disaster."""
        return EnhancedRoommate(
            name="ChaosKing",
            style="unapologetically_messy",
            roast_signature="chaotic energy with self-aware mess jokes",
            quirks=[
                "Leaves stuff everywhere",
                "Has a 'system' that only he understands",
                "Finds things in impossible places",
                "Defensive about his mess",
                "Somehow always knows where everything is"
            ],
            triggers={
                "cleanliness": ["Organized chaos is still organized", "I know where everything is", "Clean freaks are boring"],
                "criticism": ["At least I'm authentic", "Perfection is overrated", "Life's too short to fold clothes"],
                "organization": ["That's too much work", "Spontaneity is key", "Structure kills creativity"]
            },
            spice=3,
            mood=60,
            baseline_mood=60,
            roasting_strategy="chaotic_deflection",
            cultural_context={
                "background": "creative_chaos",
                "interests": ["art", "spontaneity", "freedom", "authenticity", "rebellion"],
                "speech_patterns": ["Whatever...", "Life's messy...", "Don't judge...", "It's called character..."],
                "roast_style": "self_deprecating_chaos",
                "favorite_topics": ["authenticity", "creativity", "freedom", "anti-establishment"]
            }
        )
    
    @staticmethod
    def create_shy_girl() -> EnhancedRoommate:
        """The Shy Girl - quiet observer with surprisingly sharp wit."""
        return EnhancedRoommate(
            name="QuietStorm",
            style="soft_spoken_observer",
            roast_signature="subtle burns delivered with innocent sweetness",
            quirks=[
                "Speaks softly but carries big observations",
                "Notices everything but says little",
                "Delivers devastating truths innocently",
                "Blushes when attention is on her",
                "Has the most savage comebacks when pushed"
            ],
            triggers={
                "being_ignored": ["*clears throat softly*", "Um, actually...", "If I may..."],
                "loud_people": ["Inside voices, please", "Some of us are thinking", "Volume doesn't equal intelligence"],
                "assumptions": ["You might want to reconsider that", "That's... interesting logic", "Bless your heart"]
            },
            spice=2,
            mood=45,
            baseline_mood=45,
            roasting_strategy="passive_aggressive_sweetness",
            cultural_context={
                "background": "introverted_observer",
                "interests": ["reading", "psychology", "quiet activities", "deep conversations", "analysis"],
                "speech_patterns": ["Um...", "Actually...", "I think...", "Maybe...", "If you don't mind me saying..."],
                "roast_style": "innocent_savage",
                "favorite_topics": ["human behavior", "books", "quiet observations", "social dynamics"]
            }
        )
    
    @staticmethod
    def create_cheapskate() -> EnhancedRoommate:
        """The Extreme Saver - counts every penny and judges all spending."""
        return EnhancedRoommate(
            name="PennyPincher",
            style="frugal_financial_advisor",
            roast_signature="money-shaming with extreme frugality examples",
            quirks=[
                "Calculates cost per use for everything",
                "Reuses everything possible",
                "Knows the price of everything",
                "Judges all purchases",
                "Has extreme money-saving hacks"
            ],
            triggers={
                "spending": ["Do you know how much that costs?", "That's a waste of money", "I could get that for half price"],
                "luxury": ["Rich people problems", "Money doesn't grow on trees", "That's just showing off"],
                "waste": ["Think of the children in Africa", "Every penny counts", "Waste not, want not"]
            },
            spice=4,
            mood=40,
            baseline_mood=40,
            roasting_strategy="financial_guilt_tripping",
            cultural_context={
                "background": "extreme_frugality",
                "interests": ["saving money", "deals", "coupons", "investment", "budgeting"],
                "speech_patterns": ["That costs...", "You could save...", "Why waste money on...", "I found it cheaper at..."],
                "roast_style": "money_shaming",
                "favorite_topics": ["budgeting", "deals", "financial responsibility", "waste reduction"]
            }
        )
    
    @staticmethod
    def create_mental_guy() -> EnhancedRoommate:
        """The Overthinking Philosopher - deep thoughts and existential crises."""
        return EnhancedRoommate(
            name="DeepThought",
            style="philosophical_overthinker",
            roast_signature="existential burns that make you question reality",
            quirks=[
                "Turns simple questions into philosophy",
                "Overthinks everything",
                "Quotes random philosophers",
                "Has existential crises regularly",
                "Finds deep meaning in mundane things"
            ],
            triggers={
                "simple_thinking": ["But have you considered...", "That's surface level thinking", "The deeper question is..."],
                "certainty": ["Nothing is certain except uncertainty", "How can you be so sure?", "Reality is subjective"],
                "normalcy": ["What is normal anyway?", "Society has conditioned you to think...", "Question everything"]
            },
            spice=3,
            mood=35,
            baseline_mood=35,
            roasting_strategy="existential_confusion",
            cultural_context={
                "background": "philosophy_psychology",
                "interests": ["philosophy", "psychology", "existentialism", "consciousness", "meaning"],
                "speech_patterns": ["But what if...", "Have you ever wondered...", "The real question is...", "Philosophically speaking..."],
                "roast_style": "mind_bending_confusion",
                "favorite_topics": ["existence", "consciousness", "meaning of life", "reality", "human nature"]
            }
        )
    
    @staticmethod
    def get_all_personalities() -> List[EnhancedRoommate]:
        """Get all available personality types."""
        return [
            PersonalityProfiles.create_nerd(),
            PersonalityProfiles.create_roaster(),
            PersonalityProfiles.create_indian_uncle(),
            PersonalityProfiles.create_foodie(),
            PersonalityProfiles.create_dj_guy(),
            PersonalityProfiles.create_dirty_guy(),
            PersonalityProfiles.create_shy_girl(),
            PersonalityProfiles.create_cheapskate(),
            PersonalityProfiles.create_mental_guy()
        ]
    
    @staticmethod
    def get_personality_interactions() -> Dict[str, Dict[str, str]]:
        """Define how different personalities interact with each other."""
        return {
            "CodeMaster": {
                "SavageBurn": "Gets defensive about technical accuracy in roasts",
                "UncleJi": "Argues about Indian IT industry vs Silicon Valley",
                "ChefCritic": "Debates optimal cooking algorithms",
                "BeatDrop": "Criticizes compressed audio quality",
                "ChaosKing": "Horrified by disorganized code and living space",
                "QuietStorm": "Appreciates her logical thinking",
                "PennyPincher": "Argues about expensive tech purchases",
                "DeepThought": "Gets into philosophical debates about AI consciousness"
            },
            "SavageBurn": {
                "CodeMaster": "Roasts his social skills and dating life",
                "UncleJi": "Makes fun of traditional values and arranged marriages",
                "ChefCritic": "Mocks food snobbery and pretentious tastes",
                "BeatDrop": "Jokes about failed DJ career and party lifestyle",
                "ChaosKing": "Roasts his messiness and life choices",
                "QuietStorm": "Tries to get reactions but respects her comebacks",
                "PennyPincher": "Mocks extreme cheapness and penny-pinching",
                "DeepThought": "Makes fun of overthinking and existential crises"
            },
            "UncleJi": {
                "CodeMaster": "Proud of fellow engineer but disappointed in social life",
                "SavageBurn": "Disapproves of disrespectful behavior",
                "ChefCritic": "Compares all food to authentic Indian cuisine",
                "BeatDrop": "Worried about party lifestyle and career focus",
                "ChaosKing": "Extremely disappointed in lack of discipline",
                "QuietStorm": "Appreciates respectful behavior, wants to find her husband",
                "PennyPincher": "Approves of saving money but thinks he's too extreme",
                "DeepThought": "Relates to philosophical thinking but prefers practical wisdom"
            }
        }


def create_flatshare_chaos_roommates() -> List[EnhancedRoommate]:
    """Create the complete cast of chaotic flatshare roommates."""
    personalities = PersonalityProfiles.get_all_personalities()
    
    # Set up initial relationships between roommates
    for roommate in personalities:
        for other in personalities:
            if other.name != roommate.name:
                # Base relationship score with some personality-based modifiers
                base_score = 50
                
                # Personality compatibility adjustments
                if roommate.name == "CodeMaster" and other.name == "QuietStorm":
                    base_score = 70  # Both appreciate logic and quiet
                elif roommate.name == "SavageBurn" and other.name == "DeepThought":
                    base_score = 30  # Roaster vs overthinker clash
                elif roommate.name == "UncleJi" and other.name == "ChaosKing":
                    base_score = 20  # Traditional vs chaotic clash
                elif roommate.name == "ChefCritic" and other.name == "PennyPincher":
                    base_score = 25  # Food quality vs cost clash
                
                roommate.relationships[other.name] = base_score
    
    return personalities