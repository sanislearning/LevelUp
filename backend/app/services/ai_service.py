import anthropic
from app.config.settings import settings
from typing import Dict, Optional

# Stat descriptions for AI context
STAT_DESCRIPTIONS = {
    "strength": "Physical power and athletic activities",
    "stamina": "Endurance, cardio, and sustained physical effort",
    "mind": "Learning, cognition, reading, studying, problem-solving",
    "discipline": "Consistency, habits, routine tasks, self-control",
    "selfCare": "Personal maintenance, health, hygiene, rest",
    "social": "Relationships, communication, networking, social interaction"
}


async def classify_task(task_title: str) -> Dict:
    """
    Classify a task using Claude AI
    
    Args:
        task_title: The task title/description
        
    Returns:
        Classification result dictionary
    """
    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        # Build stat descriptions for prompt
        stat_list = "\n".join([
            f"- {stat}: {desc}" 
            for stat, desc in STAT_DESCRIPTIONS.items()
        ])
        
        prompt = f"""You are a task classification AI for a gamified life system. Analyze the following task and classify it.

Task: "{task_title}"

Available Stats:
{stat_list}

Classify this task by providing:
1. primary_stat: The main stat this task develops (choose ONE from the list above)
2. secondary_stat: Optional secondary stat (choose ONE from the list above, or null if none applies)
3. difficulty: easy, medium, or hard
4. effort_score: 1-10 scale representing time/energy required
5. reasoning: Brief explanation of your classification

Respond ONLY with valid JSON in this exact format:
{{
  "primary_stat": "stat_name",
  "secondary_stat": "stat_name_or_null",
  "difficulty": "easy|medium|hard",
  "effort_score": 5,
  "reasoning": "Brief explanation"
}}"""

        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract JSON from response
        # Type ignore for Anthropic SDK content block types
        response_text = message.content[0].text  # type: ignore
        
        # Find JSON in response
        import json
        import re   
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if not json_match:
            raise ValueError("Failed to extract JSON from AI response")
        
        classification = json.loads(json_match.group(0))
        
        # Validate response
        if not classification.get("primary_stat") or not classification.get("difficulty") or not classification.get("effort_score"):
            raise ValueError("Invalid classification response from AI")
        
        # Normalize stat names (convert to camelCase)
        classification["primary_stat"] = normalize_stat_name(classification["primary_stat"])
        
        if classification.get("secondary_stat") and classification["secondary_stat"] != "null":
            classification["secondary_stat"] = normalize_stat_name(classification["secondary_stat"])
        else:
            classification["secondary_stat"] = None
        
        # Ensure effort_score is within bounds
        classification["effort_score"] = max(1, min(10, classification["effort_score"]))
        
        # Add confidence score
        classification["confidence"] = 0.85
        
        return classification
        
    except Exception as e:
        print(f"AI Classification Error: {e}")
        
        # Fallback to default classification
        return {
            "primary_stat": "discipline",
            "secondary_stat": None,
            "difficulty": "medium",
            "effort_score": 5,
            "reasoning": "Default classification due to AI error",
            "confidence": 0.3,
            "error": str(e)
        }


def normalize_stat_name(stat_name: str) -> str:
    """
    Normalize stat names to camelCase
    
    Args:
        stat_name: Stat name in any format
        
    Returns:
        Normalized stat name
    """
    stat_map = {
        "strength": "strength",
        "stamina": "stamina",
        "mind": "mind",
        "discipline": "discipline",
        "self_care": "selfCare",
        "selfcare": "selfCare",
        "self-care": "selfCare",
        "social": "social"
    }
    
    normalized = stat_name.lower().replace(" ", "_")
    return stat_map.get(normalized, "discipline")

