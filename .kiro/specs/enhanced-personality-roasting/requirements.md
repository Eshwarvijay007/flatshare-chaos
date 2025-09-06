# Requirements Document

## Introduction

This feature enhances the Flatshare Chaos application by implementing a sophisticated personality system with dynamic character interactions and an advanced context-aware roasting engine. The current system uses static responses and basic character definitions. This enhancement will create more engaging, memorable, and contextually relevant interactions by giving roommates persistent memory, relationship dynamics, and the ability to generate roasts based on conversation history and user patterns.

## Requirements

### Requirement 1

**User Story:** As a user, I want roommates to remember our previous conversations and reference them in future interactions, so that the experience feels more personal and continuous.

#### Acceptance Criteria

1. WHEN a user interacts with a roommate THEN the system SHALL store conversation context in the roommate's memory
2. WHEN a roommate generates a response THEN the system SHALL consider the last 10 conversation turns from their memory
3. WHEN a user mentions a topic they've discussed before THEN the roommate SHALL reference previous conversations about that topic
4. WHEN a roommate roasts someone THEN they SHALL incorporate details from past interactions to make it more personal
5. IF a roommate's memory exceeds 50 entries THEN the system SHALL remove the oldest entries while preserving important context

### Requirement 2

**User Story:** As a user, I want roommates to develop relationships with each other and react differently based on their history, so that the social dynamics feel realistic and evolving.

#### Acceptance Criteria

1. WHEN roommates interact with each other THEN the system SHALL track relationship scores between all roommate pairs
2. WHEN a roommate roasts another roommate THEN the relationship score SHALL influence the tone and content of the roast
3. WHEN roommates have positive interactions THEN their relationship score SHALL increase by 1-3 points
4. WHEN roommates have negative interactions THEN their relationship score SHALL decrease by 1-5 points
5. IF two roommates have a relationship score above 70 THEN they SHALL occasionally defend each other from roasts
6. IF two roommates have a relationship score below 30 THEN they SHALL be more likely to target each other for roasts

### Requirement 3

**User Story:** As a user, I want roommates to have evolving moods that affect their behavior, so that interactions feel more dynamic and unpredictable.

#### Acceptance Criteria

1. WHEN the system starts THEN each roommate SHALL have a mood score between 1-100
2. WHEN a roommate receives a harsh roast THEN their mood SHALL decrease by 5-15 points
3. WHEN a roommate successfully roasts someone THEN their mood SHALL increase by 3-8 points
4. WHEN a roommate's mood is below 30 THEN they SHALL be more aggressive and likely to initiate roasts
5. WHEN a roommate's mood is above 80 THEN they SHALL be more playful and less harsh in their roasts
6. WHEN 5 minutes pass without interaction THEN all roommate moods SHALL gradually return toward their baseline (50)

### Requirement 4

**User Story:** As a user, I want the roasting engine to analyze conversation patterns and user behavior to create more targeted and relevant roasts, so that the humor feels more intelligent and personalized.

#### Acceptance Criteria

1. WHEN a user sends a message THEN the system SHALL analyze it for topics, sentiment, and behavioral patterns
2. WHEN generating a roast THEN the system SHALL consider the user's recent topics, frequency of certain words, and conversation patterns
3. WHEN a user repeatedly mentions the same topic THEN roommates SHALL create roasts specifically about that obsession
4. WHEN a user uses certain phrases frequently THEN roommates SHALL mock those speech patterns
5. IF a user hasn't interacted for over 30 minutes THEN the next roast SHALL reference their absence
6. WHEN a user asks questions frequently THEN roommates SHALL roast them about being indecisive or needy

### Requirement 5

**User Story:** As a user, I want roommates to have contextual awareness of the current conversation thread, so that their roasts and responses feel connected to what's actually happening.

#### Acceptance Criteria

1. WHEN multiple roommates participate in a conversation THEN the system SHALL maintain a shared conversation context
2. WHEN a roommate joins a conversation THEN they SHALL reference what others have already said
3. WHEN generating a roast THEN the system SHALL ensure it's relevant to the current conversation topic
4. WHEN a conversation topic changes THEN roommates SHALL acknowledge the shift and adapt their responses
5. IF a roast would be completely off-topic THEN the system SHALL generate a different roast that fits the context
6. WHEN a user responds to a specific roommate's comment THEN other roommates SHALL be aware of that interaction

### Requirement 6

**User Story:** As a user, I want roommates to have different roasting strategies and escalation patterns, so that each character feels unique in how they approach conflict and humor.

#### Acceptance Criteria

1. WHEN a roommate is configured THEN they SHALL have a defined roasting strategy (aggressive, passive-aggressive, witty, absurd, indian-style)

4. WHEN an Indian-style roommate roasts someone THEN they SHALL use cultural references, family comparisons, academic achievements, and food-related humor
5. WHEN a roommate's roast gets a strong reaction THEN they SHALL either escalate or back down based on their personality
6. WHEN multiple roommates target the same person THEN they SHALL coordinate their approach based on their relationships
7. IF a roommate's strategy isn't working THEN they SHALL adapt their approach after 3 failed attempts

### Requirement 7

**User Story:** As a user, I want the system to track roasting effectiveness and adjust future behavior, so that the AI learns what works and becomes more engaging over time.

#### Acceptance Criteria

1. WHEN a roast is delivered THEN the system SHALL track user response time, length, and sentiment
2. WHEN a user responds quickly with a long message THEN the roast SHALL be marked as highly effective
3. WHEN a user doesn't respond or gives a short response THEN the roast SHALL be marked as less effective
4. WHEN generating future roasts THEN the system SHALL favor patterns that have been effective
5. IF a roasting approach consistently fails THEN the roommate SHALL try different strategies
6. WHEN a roommate's effectiveness score drops below 40% THEN they SHALL request help from other roommates
##
# Requirement 8

**User Story:** As a user, I want to experience authentic Indian-style roasting that incorporates cultural humor and references, so that the roasting feels diverse and culturally rich.

#### Acceptance Criteria

1. WHEN an Indian-style roommate roasts about academics THEN they SHALL reference engineering, medical school, or competitive exams
2. WHEN an Indian-style roommate roasts about family THEN they SHALL mention aunties, arranged marriages, or family expectations
3. WHEN an Indian-style roommate roasts about food THEN they SHALL compare cooking skills to mothers/grandmothers or reference specific dishes
4. WHEN an Indian-style roommate roasts about career THEN they SHALL reference stable jobs, parental approval, or societal expectations
5. WHEN an Indian-style roommate roasts about lifestyle THEN they SHALL use phrases like "beta", "what will people say", or reference cultural values
6. WHEN delivering Indian-style roasts THEN the system SHALL incorporate appropriate cultural context without stereotyping
7. IF the user mentions achievements THEN the Indian-style roommate SHALL compare them to "Sharma ji ka beta" or similar cultural references