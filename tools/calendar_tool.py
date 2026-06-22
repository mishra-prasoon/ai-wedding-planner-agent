from google.adk.tools import FunctionTool
from datetime import datetime

def add_wedding_event(
    ceremony_name: str,
    date: str,
    time: str,
    location: str,
    description: str
) -> dict:
    """
    Adds a wedding ceremony event to the planner calendar.
    
    Args:
        ceremony_name: Name of the ceremony (e.g. Mehendi, Sangeet, Wedding)
        date: Date in format YYYY-MM-DD
        time: Time in format HH:MM
        location: Venue or location name
        description: Additional details about the ceremony
    
    Returns:
        Confirmation of the event being added
    """
    # Security: sanitize inputs
    ceremony_name = ceremony_name.strip()[:100]
    location = location.strip()[:200]
    description = description.strip()[:500]
    
    event = {
        "ceremony": ceremony_name,
        "date": date,
        "time": time,
        "location": location,
        "description": description,
        "status": "scheduled",
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "message": f"✅ '{ceremony_name}' scheduled on {date} at {time} at {location}",
        "event": event
    }

def get_wedding_timeline(ceremonies: list) -> dict:
    """
    Creates a full wedding timeline from a list of ceremonies.
    
    Args:
        ceremonies: List of ceremony names to include in timeline
    
    Returns:
        A structured wedding timeline
    """
    standard_timeline = {
        "Haldi": {"typical_time": "Morning", "duration": "2-3 hours"},
        "Mehendi": {"typical_time": "Afternoon", "duration": "3-4 hours"},
        "Sangeet": {"typical_time": "Evening", "duration": "4-5 hours"},
        "Wedding": {"typical_time": "Morning/Evening", "duration": "3-4 hours"},
        "Reception": {"typical_time": "Evening", "duration": "4-6 hours"},
    }
    
    timeline = []
    for ceremony in ceremonies:
        if ceremony in standard_timeline:
            timeline.append({
                "ceremony": ceremony,
                **standard_timeline[ceremony]
            })
    
    return {
        "success": True,
        "timeline": timeline,
        "total_ceremonies": len(timeline)
    }

# Wrap as ADK tools
calendar_tool = FunctionTool(func=add_wedding_event)
timeline_tool = FunctionTool(func=get_wedding_timeline)