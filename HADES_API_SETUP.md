# Hades API Configuration Setup

This document provides instructions for developers and administrators on configuring the API keys and credentials required for the Hades Skill System.

## IMPORTANT SECURITY NOTICE
**THE USER MUST NOT ENTER API KEYS INTO THE HADES APPLICATION UI.**
All API credentials must be added into the project's secure local configuration. The frontend Settings panel is strictly read-only for verifying connection status.

## 1. Project Root & Environment Files

- **Project Root:** `d:\Hades` (or the directory where `main.py` is located)
- **Environment Template:** `<PROJECT_ROOT>/.env.example`
- **Active Environment File:** `<PROJECT_ROOT>/.env`

You must create the `.env` file manually. Do not commit `.env` to version control. 

```bash
# In the project root
cp .env.example .env
```

## 2. Supported Environment Variables

### Core AI Models
Required for Hades to reason, understand intents, and route skills.

#### `GEMINI_API_KEY`
- **Location:** `.env`
- **Format:** `GEMINI_API_KEY=your_key_here`
- **Status:** **REQUIRED** (Primary Intelligence)
- **Cost:** Free tier available
- **Used by:** Partner Brain, Model Router, Research, Execution

#### `OPENAI_API_KEY`
- **Location:** `.env`
- **Format:** `OPENAI_API_KEY=your_key_here`
- **Status:** OPTIONAL (Fallback Intelligence)
- **Cost:** Paid (Pay-as-you-go)
- **Used by:** Model Router (Fallback)

### Research Capabilities

#### `SEARCH_API_KEY`
- **Location:** `.env`
- **Format:** `SEARCH_API_KEY=your_key_here`
- **Status:** OPTIONAL (Unlocks dedicated web search APIs like Tavily/Brave)
- **Cost:** Varies (Free tiers available)
- **Used by:** Web Search Skill

### Presentation & Creation

#### `GAMMA_EMAIL` & `GAMMA_PASSWORD`
- **Location:** `.env`
- **Status:** OPTIONAL
- **Cost:** Free tier / Paid API if officially available
- **Used by:** Presentation Creation (via Browser Automation fallback if API isn't public)

#### `CANVA_CLIENT_ID` & `CANVA_CLIENT_SECRET`
- **Location:** `.env`
- **Status:** OPTIONAL
- **Cost:** Varies
- **Used by:** Presentation Creation (Fallback)

## 3. Applying Changes

If you update the `.env` file while the backend is running, you must restart the backend server for the changes to take effect:

```bash
# Stop the uvicorn process and restart it
python -m uvicorn main:app --reload
```

## 4. Testing Your Configuration

You can verify the health of all skills and their credentials by running the automated skill verification suite:

```bash
# From the project root
python scripts/verify_skills.py
```

This will output a report showing exactly which skills are `READY`, `PARTIAL`, `FAILED`, or `CONFIGURATION REQUIRED`.
