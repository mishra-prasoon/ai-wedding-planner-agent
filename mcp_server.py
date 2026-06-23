from fastmcp import FastMCP
from datetime import datetime
import json
import os
from tools.security import sanitize_input, validate_date, log_security_event

# Initialize MCP Server
mcp = FastMCP("Wedding Planner MCP Server")

# In-memory storage for wedding data
wedding_data = {
    "guests": [],
    "events": [],
    "vendors": [],
    "budget": {}
}

@mcp.tool()
def add_guest(
    name: str,
    relation: str,
    side: str,
    rsvp_status: str,
    dietary_preference: str
) -> str:
    """
    Add a guest to the wedding guest list.
    
    Args:
        name: Full name of the guest
        relation: Relation to bride/groom (e.g. cousin, friend)
        side: 'bride' or 'groom'
        rsvp_status: 'confirmed', 'pending', or 'declined'
        dietary_preference: 'vegetarian', 'vegan', or 'no restrictions'
    
    Returns:
        Confirmation message
    """
    try:
        name = sanitize_input(name, 100)
        relation = sanitize_input(relation, 100)
        side = sanitize_input(side, 20)
        rsvp_status = sanitize_input(rsvp_status, 20)
        dietary_preference = sanitize_input(dietary_preference, 50)
    except ValueError as e:
        log_security_event("INVALID_GUEST_INPUT", str(e))
        return f"Error: {str(e)}"

    guest = {
        "id": len(wedding_data["guests"]) + 1,
        "name": name,
        "relation": relation,
        "side": side,
        "rsvp_status": rsvp_status,
        "dietary_preference": dietary_preference,
        "added_at": datetime.now().isoformat()
    }
    wedding_data["guests"].append(guest)
    return f"✅ Guest '{name}' added successfully. Total guests: {len(wedding_data['guests'])}"

@mcp.tool()
def get_guest_list() -> str:
    """
    Get the complete wedding guest list with summary.
    
    Returns:
        Formatted guest list with RSVP summary
    """
    if not wedding_data["guests"]:
        return "No guests added yet."
    
    confirmed = sum(1 for g in wedding_data["guests"] if g["rsvp_status"] == "confirmed")
    pending = sum(1 for g in wedding_data["guests"] if g["rsvp_status"] == "pending")
    vegetarian = sum(1 for g in wedding_data["guests"] if g["dietary_preference"] == "vegetarian")
    
    summary = f"""
📋 GUEST LIST SUMMARY
Total Guests: {len(wedding_data["guests"])}
✅ Confirmed: {confirmed}
⏳ Pending: {pending}
🥗 Vegetarian: {vegetarian}

GUEST DETAILS:
"""
    for g in wedding_data["guests"]:
        summary += f"• {g['name']} | {g['relation']} | {g['side']} side | {g['rsvp_status']} | {g['dietary_preference']}\n"
    
    return summary

@mcp.tool()
def schedule_ceremony(
    ceremony_name: str,
    date: str,
    time: str,
    location: str
) -> str:
    """
    Schedule a wedding ceremony.
    
    Args:
        ceremony_name: Name of ceremony (Mehendi, Sangeet, Haldi, Wedding, Reception)
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        location: Venue name
    
    Returns:
        Confirmation of scheduled ceremony
    """
    try:
        ceremony_name = sanitize_input(ceremony_name, 100)
        date = validate_date(date)
        time = sanitize_input(time, 10)
        location = sanitize_input(location, 200)
    except ValueError as e:
        log_security_event("INVALID_CEREMONY_INPUT", str(e))
        return f"Error: {str(e)}"

    event = {
        "id": len(wedding_data["events"]) + 1,
        "ceremony": ceremony_name,
        "date": date,
        "time": time,
        "location": location,
        "created_at": datetime.now().isoformat()
    }
    wedding_data["events"].append(event)
    return f"✅ '{ceremony_name}' scheduled on {date} at {time} at {location}"

@mcp.tool()
def get_wedding_schedule() -> str:
    """
    Get all scheduled wedding ceremonies sorted by date.
    
    Returns:
        Full wedding schedule
    """
    if not wedding_data["events"]:
        return "No ceremonies scheduled yet."
    
    sorted_events = sorted(wedding_data["events"], key=lambda x: x["date"])
    schedule = "📅 WEDDING SCHEDULE\n\n"
    for e in sorted_events:
        schedule += f"🎊 {e['ceremony']}\n"
        schedule += f"   Date: {e['date']}\n"
        schedule += f"   Time: {e['time']}\n"
        schedule += f"   Venue: {e['location']}\n\n"
    return schedule

@mcp.tool()
def set_budget(total_budget: float) -> str:
    """
    Set the total wedding budget and auto-allocate across categories.
    
    Args:
        total_budget: Total budget in INR
    
    Returns:
        Budget allocation breakdown
    """
    allocations = {
        "Venue": 0.25,
        "Catering": 0.20,
        "Decoration": 0.15,
        "Photography": 0.10,
        "Music & Entertainment": 0.08,
        "Attire": 0.08,
        "Invitations": 0.04,
        "Miscellaneous": 0.10
    }
    
    wedding_data["budget"] = {
        "total": total_budget,
        "allocations": {k: total_budget * v for k, v in allocations.items()},
        "spent": {},
        "set_at": datetime.now().isoformat()
    }
    
    result = f"💰 BUDGET SET: ₹{total_budget:,.0f}\n\n"
    for category, amount in wedding_data["budget"]["allocations"].items():
        result += f"• {category}: ₹{amount:,.0f}\n"
    
    return result

if __name__ == "__main__":
    print("🚀 Starting Wedding Planner MCP Server...")
    mcp.run()