import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
from google.genai import types
from agents.budget_agent import budget_agent
from agents.guest_agent import guest_agent
from agents.vendor_agent import vendor_agent

load_dotenv()

APP_NAME = "wedding_planner"
USER_ID = "user_1"
SESSION_ID = "session_1"

session_service = InMemorySessionService()

async def main():
    print("🔌 Connecting to MCP Server...")

    mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
        )
    )
)

    mcp_tools = await mcp_toolset.get_tools()
    print("✅ MCP Server connected!")

    orchestrator = Agent(
        name="wedding_orchestrator",
        model="groq/llama-3.3-70b-versatile",
        description="Master wedding planner that coordinates all wedding planning tasks.",
        instruction="""
        You are a master AI Wedding Planner for Indian weddings.
        You coordinate between specialized areas:
        
        1. BUDGET - budget allocation → use set_budget tool
        2. GUESTS - guest list, RSVPs → use add_guest, get_guest_list tools
        3. VENDORS - photographers, venues → use vendor_agent
        4. SCHEDULE - ceremonies, dates → use schedule_ceremony, get_wedding_schedule tools
        
        Always use the available tools when users ask to add/get data.
        Keep responses warm and culturally aware of Indian weddings.
        You understand Mehendi, Sangeet, Haldi, Pheras, and other ceremonies.
        """,
        tools=mcp_tools,
        sub_agents=[budget_agent, guest_agent, vendor_agent]
    )

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

    print("\n💍 AI Wedding Planner")
    print("Ask me anything about budget, guests, vendors or schedule!")
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