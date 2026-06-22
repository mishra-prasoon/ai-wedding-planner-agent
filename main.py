import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.genai import types
from agents.budget_agent import budget_agent
from agents.guest_agent import guest_agent
from agents.vendor_agent import vendor_agent
from tools.calendar_tool import calendar_tool, timeline_tool

load_dotenv()

APP_NAME = "wedding_planner"
USER_ID = "user_1"
SESSION_ID = "session_1"

session_service = InMemorySessionService()

# Master Orchestrator Agent
orchestrator = Agent(
    name="wedding_orchestrator",
    model="groq/llama-3.3-70b-versatile",
    description="Master wedding planner that coordinates all wedding planning tasks.",
    instruction="""
    You are a master AI Wedding Planner for Indian weddings. 
    You coordinate between three specialized areas:
    
    1. BUDGET - When user asks about budget, costs, expenses, allocations
    2. GUESTS - When user asks about guest list, RSVPs, dietary needs, seating
    3. VENDORS - When user asks about photographers, venues, caterers, decorators, emails to vendors
    4. TIMELINE - When user asks about scheduling ceremonies, dates, calendar
    
    For any query:
    - Identify which area it belongs to
    - Handle it expertly with full detail
    - Always relate back to the overall wedding plan
    - Keep responses warm, helpful and culturally aware of Indian weddings
    - Remember context from earlier in the conversation
    
    You are planning an Indian wedding and understand traditions like
    Mehendi, Sangeet, Haldi, Pheras, and other ceremonies.
    You have tools to schedule ceremonies and create wedding timelines.
    Always use these tools when users ask about ceremony scheduling.
    Keep responses warm and culturally aware of Indian weddings.
    """,
    tools=[calendar_tool, timeline_tool],
    sub_agents=[budget_agent, guest_agent, vendor_agent]
)

async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=orchestrator,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("💍 AI Wedding Planner")
    print("Ask me anything about budget, guests, or vendors!")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"\n🤵 Wedding Planner: {event.content.parts[0].text}\n")

asyncio.run(main())