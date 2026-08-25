# HADES — AI OPERATING SYSTEM
### *"The user should manage the goal — not the intelligence required to achieve it."*

---

## WHAT IS HADES?

HADES is an AI Operating System — a persistent, conversational AI partner that runs natively on Linux, understands your intent through conversation, locks a mission before touching your system, orchestrates multiple AI models and tools in the background, validates the result, and reports back. 

It is not a chatbot. It is not a wrapper around ChatGPT. It is not an automation script with an AI bolted on.

HADES is an attempt to build the missing layer between the human and the machine — the layer that coordinates intelligence so the user doesn't have to.

---

## THE PROBLEM HADES SOLVES

Today's AI ecosystem is fragmented by design. You use Gemini for research, Claude for code, ChatGPT for writing, Notion for notes, Zapier for automation. The models are powerful. The problem is that **you** are the orchestration layer. Every context switch, every repeated prompt, every manual workflow, every model selection decision — that cognitive load belongs to you.

This is not a capability problem. The models are smart enough. This is an **orchestration problem**.

HADES moves orchestration into the system itself. You describe what you want to achieve. HADES figures out how, which models to use, which tools to invoke, and whether the result actually meets your criteria.

---

## WHY LINUX?

HADES is built specifically for Linux. This is not an accident. Linux is the operating system for people who actually control their machines. It is the substrate of servers, developer workstations, AI infrastructure, and the open internet.

**HADES integrates with Linux at multiple levels:**

### 1. Shell & Process Control
The core execution layer — `TerminalSkill` — runs bash commands directly via Python's `asyncio.create_subprocess_shell`. This means HADES can:
- Create and manage files, directories, and archives
- Start, stop, and monitor processes
- Run scripts, compilers, build systems
- Pipe commands, redirect output, chain operations
- Execute anything a developer would type in a terminal

The entire POSIX command surface is available to the AI. When HADES decides to "run a Python server" or "compress these files" or "find all logs from today", it generates a real shell command and executes it on your Linux system.

### 2. Filesystem Operations
`FilesystemSkill` reads, writes, moves, copies, and inspects files on the local Linux filesystem. HADES can create project scaffolds, edit configuration files, search through directories, and manage artifacts from its own missions.

### 3. Process Manager
`ProcessManagerSkill` provides process-level visibility — listing running processes, checking system resource usage, and managing long-running tasks. HADES can monitor what's happening on your machine, not just inside its own execution context.

### 4. Local Model Execution
Through Ollama integration, HADES can run AI models entirely offline on your Linux machine. No cloud, no API keys, no data leaving your system. Models run locally via the Ollama API server (`localhost:11434`), making HADES viable as a fully private, air-gapped AI system.

### 5. Local TTS (Text-to-Speech)
HADES uses **Kokoro-ONNX** — an open-source neural TTS engine — running directly on the backend server. Audio is synthesized locally, encoded as Base64, and sent to the frontend. No cloud TTS dependency. No voice data transmitted externally.

### 6. Future: Deep Linux Integration
The architecture is designed to extend into `systemd` (for scheduling background missions as system services), `D-Bus` (for desktop event integration), and kernel-level event monitoring. Today HADES uses subprocess calls. Tomorrow it can integrate with the OS scheduler itself.

---

## HOW HADES WORKS

### The Core Principle: Conversation Before Execution

Most AI agents take your input and immediately start executing. HADES does the opposite. It starts with a conversation.

Before HADES touches your system, it must understand:
- **What exactly you want to achieve** (objective)
- **What a successful result looks like** (success criteria)
- **What constraints apply** (don't use external APIs, keep it fast, etc.)
- **What the desired outcome is** (the final state you want the system in)

Only when all of these are established — and HADES has confirmed mutual understanding with you — does execution begin. This boundary is called the **Mission Lock**.

---

### The Architecture

```
USER
  │
  ▼
PARTNER BRAIN                    ← Conversation, alignment, understanding
  │    ├── Intent Classifier     ← Is this casual? A small task? A real mission?
  │    ├── Mission Extractor     ← Builds structured mission state from conversation
  │    └── Understanding Eval   ← Verifies all fields populated, mutual understanding reached
  │
  ▼
MISSION LOCK                     ← The authorization gate. No execution without this.
  │
  ▼
EXECUTIVE BRAIN                  ← Plans, delegates, orchestrates, recovers
  │    ├── Task Graph            ← Breaks mission into executable tasks
  │    └── Worker Delegation     ← Routes each task to the right capability
  │
  ▼
WORKER MANAGER                   ← Model-agnostic LLM routing via LiteLLM
  │    ├── Google Gemini         ← Conversational, fast, analysis
  │    ├── Groq / Llama 3.3     ← Ultra-fast open-source inference
  │    ├── OpenRouter            ← Free public model endpoints
  │    └── Ollama (Local)        ← 100% offline, private execution
  │
  ▼
TOOLS / SKILLS                   ← The hands of HADES
  │    ├── Terminal              ← bash command execution on Linux
  │    ├── Filesystem            ← read, write, move, inspect files
  │    └── Process Manager       ← process monitoring and control
  │
  ▼
REVIEW ENGINE                    ← Verification before delivery
  │    ├── Exit code validation  ← Did the command succeed?
  │    ├── Artifact check        ← Does the output file actually exist?
  │    ├── Heuristic check       ← Does the output look right?
  │    └── LLM semantic review   ← Does it actually satisfy the success criteria?
  │
  ▼
MEMORY MANAGER                   ← Learns from every mission
  │    ├── Session state         ← Active conversation context
  │    └── Mission history       ← Persistent JSON log of past missions
  │
  ▼
SERVER-SENT EVENTS               ← Real-time mission updates to the UI
  │
  ▼
USER ← Result delivered. HADES speaks the outcome via Kokoro TTS.
```

---

### The Mission State Machine

Every piece of work in HADES is a **Mission** — a persistent, structured object that lives across the entire lifecycle from conversation to delivery.

```
CONVERSATION
    ↓ (mutual understanding reached)
AUTHORIZED_EXECUTION      ← Mission Lock activated
    ↓ (execution begins)
BACKGROUND_WORK           ← HADES is running, UI gets live updates
    ↓                         ↘
COMPLETED                   NEEDS_USER  ← HADES needs clarification mid-task
```

A Mission contains:
- `objective` — what needs to be done
- `desired_outcome` — the end state
- `constraints` — boundaries (no internet, keep it safe, etc.)
- `success_criteria` — how to know it worked
- `conversation_history` — full context from alignment conversation
- `status` — current state in the machine
- `output_artifacts` — files, results produced
- `mission_id` — unique identifier for history

---

### The Mission Lock in Detail

The Mission Lock is the single most important architectural decision in HADES.

It is implemented in `understanding_evaluator.py`. Before execution is permitted, the system verifies:

1. `objective` is not empty
2. `desired_outcome` is not empty  
3. `success_criteria` is not empty
4. `mutual_understanding_reached` is `True`

If any of these fail, HADES continues the conversation. It asks. It clarifies. It pushes back if the request is vague or risky.

The Partner Brain's `ConversationalDecisionSystem` has three possible outputs:
- `ASK` — gather more information
- `PROPOSE` — present a plan for user review  
- `ACKNOWLEDGE` — full understanding reached → trigger Mission Lock

There is also a developer bypass (`FORCE_EXECUTE`) for rapid testing, which exists transparently in the codebase.

---

### The Review Engine in Detail

HADES does not let the AI declare its own success. The Review Engine (`review_engine.py`) validates every task output through four independent stages:

**Stage 1: Exit Code Check**
Every terminal command returns an exit code. `0` = success. Anything else = failure. This is the cheapest, most reliable signal.

**Stage 2: Artifact Existence Check**
If the success criteria mentions a file path (e.g., "output.txt should be created"), HADES checks whether that file actually exists on the Linux filesystem. The AI cannot fake this.

**Stage 3: Heuristic Validation**
Content-level sanity checks. Is the output file non-empty? Does the stdout contain expected patterns? These are fast, deterministic checks that don't require another LLM call.

**Stage 4: Semantic LLM Review**
When heuristics are insufficient, HADES calls an LLM with the task output and the original success criteria to semantically verify alignment. This is the most expensive check and only runs when earlier stages pass but confidence is low.

**On Failure:** The failed output and error context are fed back to the ExecutionBrain. The LLM is prompted to try a different approach. This loops up to `max_retries`.

---

### The Worker Manager in Detail

HADES is model-agnostic. No vendor lock-in. Every LLM is just a replaceable capability endpoint.

`WorkerManager` (backed by LiteLLM) reads from `config.json` to discover available providers. Each provider is tagged with:
- `capability` (fast, reasoning, coding, research)
- `api_key_env` (the environment variable holding the key)
- `model` (the LiteLLM model string)
- `status` (ACTIVE / FAILED)

When the ExecutionBrain needs to generate a command, it requests a `capability`. WorkerManager:
1. Filters providers by capability
2. Checks which API keys are present in the environment
3. Tries providers in priority order
4. Automatically falls back if one fails

**Currently configured providers:**
| Provider | Model | Capability |
|---|---|---|
| Google | gemini/gemini-2.5-flash-lite | Conversational, fast |
| Google | gemini/gemini-flash-latest | Research, analysis |
| Groq | llama-3.3-70b-versatile | Fast, open-source |
| OpenRouter | llama-3.2-3b-instruct | Free public endpoint |
| Ollama | (local) | Private, offline |

---

## A COMPLETE MISSION — REAL EXECUTION

**User says:** *"List all files in the current directory and save them to output.txt"*

**What actually happens:**

1. Frontend sends `POST /api/chat` with the message
2. `IntentClassifier` — classifies as `SMALL_TASK` (not a casual chat, but also not a complex mission requiring full alignment)
3. `MissionExtractor` — populates mission fields: objective = list files, success_criteria = output.txt exists
4. `UnderstandingEvaluator` — all fields satisfied → `MissionStatus.AUTHORIZED_EXECUTION`
5. `main.py` calls `asyncio.create_task(execution_brain.process_mission)` — HTTP response returns immediately (non-blocking)
6. `ExecutionBrain._generate_plan()` — creates a TaskGraph with 1 task
7. `WorkerManager` routes to Gemini → LLM generates: `ls -la > output.txt`
8. `TerminalSkill.execute()` runs: `asyncio.create_subprocess_shell("ls -la > output.txt")`
9. Command exits with code `0`
10. `ReviewEngine` checks: exit_code == 0 ✓, output.txt exists on disk ✓ → **PASS**
11. `memory_manager.add_mission_to_history()` → appended to `memory.json`
12. SSE emits `MISSION_COMPLETED` event to the frontend
13. Frontend updates UI. HADES speaks the result via Kokoro TTS.

**Total execution path:** 13 discrete system layers, all functional, all connected.

---

## TECH STACK

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite + TypeScript + Tailwind CSS |
| **Backend** | Python + FastAPI + asyncio |
| **State** | Pydantic models (mission.py, conversation.py) |
| **LLM Routing** | LiteLLM (multi-provider abstraction) |
| **AI Providers** | Google Gemini, Groq, OpenRouter, Ollama |
| **Tool Execution** | asyncio.create_subprocess_shell (Linux bash) |
| **Event Streaming** | Server-Sent Events (SSE) via FastAPI EventSourceResponse |
| **Voice Output** | Kokoro-ONNX (local neural TTS, no cloud) |
| **Voice Input** | Browser Web Speech API (SpeechRecognition) |
| **Memory** | JSON flat file (memory.json) + in-memory session state |
| **Configuration** | config.json + .env (API keys via python-dotenv) |
| **OS Target** | Linux (bash, POSIX filesystem, subprocess) |

---

## WHAT IS IMPLEMENTED

| Component | Status | File |
|---|---|---|
| Conversational alignment loop | ✅ WORKING | partner_brain.py |
| Intent classification | ✅ WORKING | intent_classifier.py |
| Mission state extraction | ✅ WORKING | mission_extractor.py |
| Mission state machine (5 states) | ✅ WORKING | mission.py |
| Mission Lock gate | ✅ WORKING | understanding_evaluator.py |
| WorkerManager + LiteLLM routing | ✅ WORKING | worker_manager.py |
| Multi-provider model fallback | ✅ WORKING | worker_manager.py |
| Terminal skill (bash execution) | ✅ WORKING | skills/computer/terminal.py |
| Filesystem skill | ✅ WORKING | skills/computer/filesystem.py |
| Process manager skill | ✅ WORKING | skills/computer/process_manager.py |
| Review Engine (4-stage) | ✅ WORKING | review_engine.py |
| Server-Sent Events stream | ✅ WORKING | main.py |
| React/Vite frontend | ✅ WORKING | frontend/src/ |
| Full E2E execution path | ✅ WORKING | all layers connected |
| Backend TTS (Kokoro-ONNX) | ✅ WORKING | voice_manager.py |
| Session persistence | ✅ WORKING | localStorage |
| Worker specialization | ⚡ PARTIAL | model endpoints only |
| Task decomposition | ⚡ PARTIAL | hardcoded 1 task |
| Long-term memory | ⚡ PARTIAL | flat JSON, no RAG |
| Voice input (STT) | ⚡ PARTIAL | browser API only |
| Dynamic multi-step planning | 🔴 FUTURE | — |
| Docker/sandbox isolation | 🔴 FUTURE | security milestone |
| Vector/RAG memory | 🔴 FUTURE | — |
| Backend Whisper STT | 🔴 FUTURE | — |
| Autonomous worker agents | 🔴 FUTURE | — |

---

## WHAT IS GENUINELY NOVEL

**1. Mutual Understanding Gate**
No mainstream AI system gates execution on explicit, structured human-alignment verification. HADES requires a deterministic state check — all mission fields populated + `mutual_understanding_reached = True` — before any tool is ever invoked.

**2. Mission-Centric Computing**
The unit of work is not a prompt. It is a Mission — a persistent object with objective, constraints, success criteria, and state. Missions survive across the entire conversation → execution → review → memory lifecycle.

**3. Partner / Executive Duality**
Two isolated cognitive systems: the Partner Brain handles conversation and never touches tools. The Executive Brain handles execution and never engages the user. This is a deliberate architectural decision that prevents the classic agent failure mode where execution and conversation contaminate each other.

**4. Verification-First Execution**
The worker generates output. The Review Engine determines if the mission was actually completed. Generation is not success. This 4-stage validation system makes HADES's execution claims trustworthy.

**5. Invisible Intelligence Orchestration**
The user expresses a goal in natural language. Which model runs, which provider is called, which tool is invoked — all of this is invisible. Intelligence becomes infrastructure.

**6. Model-Agnostic by Design**
HADES is not coupled to any AI vendor. Adding a new model requires one entry in `config.json`. Removing one requires deleting it. The system degrades gracefully through fallback.

---

## HONEST GAPS

HADES is a prototype, not a finished product. The following are known engineering gaps:

- **The planner is hardcoded to 1 task.** `ExecutionBrain._generate_plan()` does not dynamically decompose complex objectives. True multi-step planning is the most critical missing feature.
- **Terminal commands execute on the host machine.** There is no Docker sandbox. A malicious or confused LLM could execute harmful commands. Security hardening is a mandatory next milestone.
- **Memory is a flat JSON file.** It is injected blindly into the system prompt and will eventually exceed the context window. Vector/RAG memory is needed.
- **STT is browser-based.** Backend Whisper STT is not implemented. Offline voice input requires it.
- **One test file exists.** `test_partner_brain.py` tests the intent classifier. End-to-end testing is absent.

These are not excuses. They are the known engineering path from prototype to production AI OS.

---

## THE VISION

Today HADES proves the loop:
> Conversation → Mutual Understanding → Mission Lock → Background Execution → Verified Result → Delivery

Tomorrow HADES proves the system:
> Dynamic multi-step missions. Specialized autonomous workers. Persistent cross-session memory. Sandboxed execution. Deep Linux integration. Local + cloud intelligence. Long-term human-AI partnership.

**HUMAN SETS THE MISSION.**  
**HADES ORCHESTRATES THE INTELLIGENCE.**

---

*Project HADES · AI Operating System Prototype · Built on Linux · 2025*
