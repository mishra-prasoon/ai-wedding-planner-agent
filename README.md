# 💍 AI Wedding Planner Agent

An intelligent multi-agent system for planning Indian weddings, built with Google ADK and Groq LLM.

## 🎯 Problem Statement
Planning an Indian wedding involves coordinating hundreds of tasks — managing budgets across categories, tracking 200+ guests, negotiating with vendors, and scheduling multiple ceremonies. This AI agent makes it effortless.

## 🤖 Solution
A multi-agent AI system where specialized agents handle different aspects of wedding planning, coordinated by a master orchestrator.

## 🏗️ Architecture

User
↓
Orchestrator Agent (Master Planner)
├── Budget Agent    → Budget allocation, expense tracking
├── Guest Agent     → Guest list, RSVPs, dietary preferences
└── Vendor Agent    → Vendor search, comparison, email drafting

## ✨ Features
- 💰 Smart budget splitting across wedding categories
- 👥 Guest list management with RSVP and dietary tracking
- 🏛️ Venue and vendor recommendations for Indian cities
- 📧 Professional vendor inquiry email drafting
- 🎊 Indian wedding ceremony awareness (Mehendi, Sangeet, Haldi, Pheras)

## 🛠️ Tech Stack
- **Google ADK** - Multi-agent orchestration
- **Groq + Llama 3.3** - LLM backbone
- **Python 3.13** - Core language
- **LiteLLM** - Model integration

## 🚀 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/mishra-prasoon/ai-wedding-planner-agent.git
cd ai-wedding-planner-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file:

GROQ_API_KEY=your_groq_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE

Get a free Groq API key at: https://console.groq.com

### 4. Run the agent
```bash
python3 main.py
```

## 💬 Example Interactions

**Budget Planning:**
You: My wedding budget is ₹20 lakhs. Split it across all categories.

**Guest Management:**
You: Add guest: Rahul Sharma, groom's brother, confirmed, vegetarian

**Vendor Search:**
You: Find me a photographer in Lucknow with budget ₹1.5 lakhs

## 📁 Project Structure
ai-wedding-planner-agent/
├── main.py              # Entry point + Orchestrator
├── agents/
│   ├── budget_agent.py  # Budget management agent
│   ├── guest_agent.py   # Guest list agent
│   └── vendor_agent.py  # Vendor management agent
├── requirements.txt
└── .gitignore

## 🏆 Kaggle Competition
Built for the AI Agents: Intensive Vibe Coding Capstone Project
Track: Concierge Agents