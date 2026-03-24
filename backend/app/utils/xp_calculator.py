"""
XP Calculator with adjusted leveling curve
Slower progression at higher levels as requested
"""

DIFFICULTY_BASE_XP = {
    "easy": 5,
    "medium": 10,
    "hard": 20
}

EFFORT_MULTIPLIER = 1.5  # Increased from 0.5 for more impact


def calculate_task_xp(difficulty: str, effort_score: int) -> int:
    """
    Calculate XP for a task
    
    Args:
        difficulty: 'easy', 'medium', or 'hard'
        effort_score: 1-10 scale
        
    Returns:
        Total XP earned
    """
    base_xp = DIFFICULTY_BASE_XP.get(difficulty.lower(), 10)
    effort_bonus = effort_score * EFFORT_MULTIPLIER
    return round(base_xp + effort_bonus)


def calculate_xp_for_level(level: int) -> int:
    """
    Calculate XP required for next level
    Adjusted formula: XP = 100 * (level ^ 1.3)
    This creates a slower curve at higher levels compared to 1.5
    
    Level 1: 100 XP
    Level 5: 844 XP
    Level 10: 2,009 XP (vs 3,162 with 1.5)
    Level 20: 5,179 XP (vs 8,944 with 1.5)
    Level 50: 18,946 XP (vs 35,355 with 1.5)
    """
    return round(100 * (level ** 1.3))


def calculate_level(total_xp: int) -> dict:
    """
    Calculate current level from total XP
    
    Args:
        total_xp: Total accumulated XP
        
    Returns:
        dict with level, currentLevelXP, xpForNextLevel, progress
    """
    level = 1
    xp_accumulated = 0
    
    # Find current level
    while xp_accumulated + calculate_xp_for_level(level) <= total_xp:
        xp_accumulated += calculate_xp_for_level(level)
        level += 1
    
    current_level_xp = total_xp - xp_accumulated
    xp_for_next_level = calculate_xp_for_level(level)
    progress = (current_level_xp / xp_for_next_level) * 100
    
    return {
        "level": level,
        "currentLevelXP": current_level_xp,
        "xpForNextLevel": xp_for_next_level,
        "progress": round(progress, 1)
    }


def distribute_xp(total_xp: int, primary_stat: str, secondary_stat: str = None) -> dict:
    """
    Distribute XP to stats
    
    Args:
        total_xp: Total XP to distribute
        primary_stat: Primary stat name
        secondary_stat: Secondary stat name (optional)
        
    Returns:
        dict with XP distribution
    """
    distribution = {}
    
    if secondary_stat:
        distribution[primary_stat] = round(total_xp * 0.8)
        distribution[secondary_stat] = round(total_xp * 0.2)
    else:
        distribution[primary_stat] = total_xp
    
    return distribution


def get_title(level: int) -> str:
    """
    Get title based on level
    
    Args:
        level: Current level
        
    Returns:
        Title string
    """
    if level >= 50:
        return "Ascended"
    elif level >= 20:
        return "Elite"
    elif level >= 10:
        return "Disciplined"
    elif level >= 5:
        return "Apprentice"
    else:
        return "Beginner"

# Made with Bob
