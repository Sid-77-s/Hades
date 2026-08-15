# Hades OS — State of the Union & Knowledge Base

This document provides a comprehensive overview of the Hades Intelligence Operating System, its underlying philosophy, a brutal assessment of its current demo state, and a complete file-by-file manifest of the project.

---

## 1. The Brief Working of Hades

Hades is not a chatbot; it is an **Intelligence Operating System**. The core philosophy is that Hades acts as a single, persistent intelligence that sits *between* the user and the complexity of the internet, APIs, and local systems.

### Core Architecture

1.  **The Partner Brain (`src/core/partner_brain.py`)**: This is the conversational interface. It extracts intent, decides if a task requires a "Mission" (background execution) or just a conversational response, and maintains the persistent relationship with the user.
2.  **The Execution Brain (`src/core/execution/execution_brain.py`)**: When the Partner Brain decides a task is too complex for chat, it creates a Mission. The Execution Brain takes this mission, selects the appropriate "Skill" from the `SkillRegistry`, executes the skill in the background, and returns the result to the Partner Brain.
3.  **The Skill System (`src/skills/`)**: Instead of hardcoded integrations, Hades dynamically discovers capabilities. Skills are categorized (Core AI, Computer, Browser, Research, Creation, Real World) and each skill manages its own health checks and fallback strategies.
4.  **The UI (`frontend/src/`)**: A cinematic, edge-to-edge React/Vite dashboard that displays real-time missions, the core conversational thread, and the status of the underlying skill system without feeling like a generic "chat app".

---

## 2. The Brutal Truth: Current State of the Demo

While the architectural bones are incredibly solid and futuristic, here is the honest truth about the current execution state:

*   **The UI is Beautiful but Partially Stubbed:** The frontend scrolling issues are fixed and the cinematic design is intact. The Settings Modal successfully reads live data from the backend. However, things like "Recent Activity", "System Metrics", and "Agenda" are currently populated with static mockup data.
*   **The Skill System is Real but Shallow:** The `SkillRegistry` works perfectly. It dynamically discovers skills and checks their `.env` credentials.
    *   `TerminalSkill` & `FilesystemSkill` are highly functional.
    *   `BrowserNavigateSkill` (Playwright) is wired up but requires a robust orchestration loop to navigate complex DOMs reliably.
    *   `PresentationCreationSkill` works via Gamma, but correctly defaults to a local Python `pptx` fallback when Gamma credentials are missing.
    *   `RestaurantReservationSkill` is a complete stub waiting for an OpenTable/Resy integration.
*   **The Chat Routing Needs Updating:** The core API uses `litellm` to route requests to Gemini. Currently, chatting with Hades returns a developer error: `litellm.NotFoundError: GeminiException - "models/gemini-1.5-flash is not found for API version v1beta..."`. This means the chosen model alias in the backend needs to be updated to match Google's latest endpoint requirements.
*   **The Orchestration Loop Needs Work:** The `ExecutionBrain` can select a skill and fire it, but the `ReviewEngine` and `UncertaintyEngine` (which allow Hades to gracefully fail, try another skill, or ask the user for help mid-mission) are still in early conceptual stages.

**Conclusion:** Hades currently works as a highly polished "Wizard of Oz" prototype. The *structure* to make it a fully autonomous OS is implemented, but the individual capabilities need deeper API wiring to be considered production-ready.

---

## 3. Project File Manifest

Below is the complete list of critical files currently comprising the Hades repository and what they do.

### Root Level
*   `main.py`: The FastAPI backend entry point. Wires up the REST endpoints (chat, memory, status) and initializes the EventBus and Brains.
*   `.env`: The secure credential store. (Never commit this).
*   `.env.example`: Template for required credentials.
*   `HADES_API_SETUP.md`: Documentation on how to acquire and inject the necessary API keys.
*   `package.json`: NPM configuration for running verification scripts.
*   `config.json`: Persistent non-sensitive application settings.

### Core Intelligence (`src/core/`)
*   `partner_brain.py`: The conversational core. Evaluates user input and routes to execution or conversation.
*   `config_manager.py`: Securely loads `.env` secrets into the application environment.
*   `event_bus.py`: The pub/sub system allowing the backend to push real-time mission updates to the frontend.
*   `memory_manager.py`: Handles persistent context and user facts.
*   `intent_classifier.py` & `mission_extractor.py`: Utility classes that parse raw user text into structured JSON goals using LiteLLM.
*   `execution/execution_brain.py`: The orchestration engine that takes a mission and runs it against the Skill Registry.
*   `execution/review_engine.py` & `execution/uncertainty_engine.py`: Systems designed to verify skill outputs and handle failures gracefully (currently WIP).

### The Skill System (`src/skills/`)
*   `base.py`: Defines the `BaseSkill` abstract class and `SkillStatus` enums. Every capability inherits from this.
*   `registry.py`: The `SkillRegistry`. Automatically scans the `src/skills` tree and loads any class inheriting from `BaseSkill`.
*   `browser/browser_manager.py` & `browser_skills.py`: Playwright integration allowing Hades to open headless browsers, navigate, and extract DOM trees.
*   `computer/filesystem.py` & `terminal.py`: Gives Hades the ability to read/write local files and execute local CMD/Bash scripts.
*   `core_ai/model_router.py`: Determines whether a task should use a fast model (Gemini Flash) or a reasoning model (OpenAI o1).
*   `creation/presentation_creation.py`: Integrates with the Gamma API to build slide decks, with a graceful fallback to the `python-pptx` library.
*   `real_world/restaurant_reservation.py`: Stubbed capability demonstrating real-world API routing.
*   `research/web_search.py`: Tavily API integration for live internet access.

### Scripts
*   `scripts/verify_skills.py`: A diagnostic tool that forces the `SkillRegistry` to load and ping every skill's health check, outputting a clear terminal report.

### Frontend (`frontend/src/`)
*   `App.tsx`: The root application component managing the cinematic layout.
*   `index.css`: Defines the global variables, Tailwind overrides, and custom `scroll-thin` classes.
*   `services/HadesService.ts` & `useHades.ts`: The data layer that communicates with the FastAPI backend.
*   `components/SettingsModal.tsx`: The overlay that reads `/api/config/status` to display real-time credential health.
*   `components/ChatPanel.tsx` & `Composer.tsx`: The primary interaction zone for the user.
*   `components/MissionCard.tsx`: The UI representation of a background task executing via the `ExecutionBrain`.
*   `components/TopBar.tsx`, `HeroCore.tsx`, `SystemMetrics.tsx`: Layout and atmosphere components that solidify the "OS" feel.
