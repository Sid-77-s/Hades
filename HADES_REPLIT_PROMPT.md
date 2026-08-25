# HADES PRESENTATION — COMPLETE REPLIT PROMPT
## Copy this ENTIRE block into Replit Agent / Replit AI

---

```
Build a stunning, self-contained single HTML file (index.html) that is a 13-slide 
hackathon presentation for Project HADES — an AI Operating System prototype.

Use reveal.js (loaded from CDN). Do NOT use any build tools or npm. 
The file must open directly in any browser by double-clicking it.

==============================================
DESIGN SYSTEM — APPLY TO EVERY SLIDE
==============================================

CSS Variables to define:
  --void:    #09090f   (near-black background)
  --abyss:   #0f0f1a   (slide background)
  --panel:   #14142a   (card backgrounds)
  --ion:     #7c3aed   (primary indigo/violet accent)
  --signal:  #6d28d9   (darker violet)
  --glow:    #a78bfa   (soft lavender, text highlights)
  --online:  #10b981   (green — for IMPLEMENTED)
  --amber:   #f59e0b   (amber — for PARTIAL)
  --danger:  #ef4444   (red — for MISSING/risk)
  --muted:   #6b7280   (muted gray)
  --text:    #e2e8f0   (primary text)
  --subtle:  #94a3b8   (secondary text)

Font: Import "Inter" from Google Fonts (weights 300, 400, 600, 700, 800, 900)

Global styles:
- body and .reveal: background #09090f, font-family Inter
- All slides: background #09090f
- section: display flex, flex-direction column, justify-content center
- h1, h2, h3: font-weight 900, color white, text-transform uppercase, letter-spacing 0.05em
- p, li: font-weight 300, color #e2e8f0
- No bullet points on any slide — use custom layout cards instead
- Slide transition: "fade" — duration 600ms
- Add a subtle repeating grid pattern to every slide background using CSS:
  background-image: linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
- Add a glowing bottom border to every slide: 
  box-shadow: inset 0 -1px 0 rgba(124,58,237,0.3)
- Status badge styles:
  .badge-green  { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.4); border-radius: 6px; padding: 3px 10px; font-size: 0.65em; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
  .badge-amber  { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.4); ... same pattern }
  .badge-red    { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.4);  ... same pattern }
  .badge-violet { background: rgba(124,58,237,0.2);  color: #a78bfa; border: 1px solid rgba(124,58,237,0.5); ... same pattern }
- Cards: background #14142a, border 1px solid rgba(124,58,237,0.25), border-radius 12px, padding 20px
- Glow accent text: color #a78bfa
- Divider lines: 1px solid rgba(124,58,237,0.2)

Navigation: minimal dots at bottom. Arrow keys + space to advance.
Add slide numbers (bottom-right): "01 / 13" style in --muted color.

==============================================
SLIDE 01 — TITLE SLIDE
==============================================

Full-screen layout. Everything centered vertically and horizontally.

TOP: Small label in violet badge: "HACKATHON BUILD · AI SYSTEMS ENGINEERING"

CENTER TOP: 
  Monospace-style label: "PROJECT"
  Giant text (font-size: clamp(5rem, 12vw, 9rem), font-weight: 900): 
  "HADES"
  — letter-spacing: 0.15em
  — apply a violet text-shadow glow: text-shadow: 0 0 80px rgba(124,58,237,0.6), 0 0 160px rgba(124,58,237,0.2)
  — the H, A, D, E, S letters should each be a span, alternating between white and --glow color

BELOW TITLE:
  Subtitle (font-size: 1.2rem, font-weight: 300, color: --subtle, letter-spacing: 0.3em, text-transform: uppercase):
  "FROM AI ASSISTANT  TO  AI OPERATING SYSTEM"

VISUAL FLOW (horizontal, centered, margin-top: 3rem):
  Show this as a glowing pipeline row with arrows between:
  [ HUMAN ] →→ [ HADES ] →→ [ MODELS + TOOLS + SYSTEM ] →→ [ REAL RESULT ]
  
  Style: Each node is a rounded pill.
  [ HUMAN ] — border: 1px solid #6b7280, text: white
  [ HADES ] — background: linear-gradient(135deg, #7c3aed, #6d28d9), text: white, box-shadow: 0 0 30px rgba(124,58,237,0.5)
  [ MODELS + TOOLS + SYSTEM ] — border: 1px solid rgba(124,58,237,0.4), text: #a78bfa
  [ REAL RESULT ] — border: 1px solid #10b981, text: #10b981
  Arrows between: → in --glow color, animated with a CSS keyframe pulse

BOTTOM STATEMENT (margin-top: 3rem):
  Thin horizontal violet line above.
  Text (font-size: 0.85rem, color: --subtle, font-style: italic, max-width: 600px, text-align: center):
  "The user should manage the goal — not the intelligence required to achieve it."

==============================================
SLIDE 02 — THE PROBLEM: ORCHESTRATION COLLAPSE
==============================================

HEADLINE: "THE AI PROBLEM IS NO LONGER CAPABILITY."
SUBHEAD (violet): "IT IS ORCHESTRATION."

TWO-COLUMN layout:

LEFT COLUMN — "TODAY'S AI STACK" (messy scattered layout):
  Show 7 floating service cards in a scattered/chaotic grid (use CSS transform: rotate):
  Each card: small icon emoji + service name + task label
  
  🔍 GEMINI     → Research
  💻 CLAUDE     → Coding  
  ✍️ CHATGPT    → Writing
  📝 NOTION     → Notes
  ⚡ ZAPIER     → Automation
  📅 CALENDAR   → Scheduling
  📧 GMAIL      → Email
  
  In the CENTER of the chaos: a pulsing red/amber circle labeled
  "YOU" — with lines radiating out to each tool card.
  Label under: "The human IS the orchestration layer."

RIGHT COLUMN — "THE HIDDEN TAX":
  6 items in a vertical list, each as a card row:
  🔴  Context switching between tools
  🔴  Repeating yourself to every model
  🔴  Manually selecting the right AI
  🔴  Managing workflow and sequencing
  🔴  Context lost between sessions
  🔴  Decision fatigue from tool sprawl

BOTTOM FULL-WIDTH statement (centered, violet text):
  "Today's AI gives humans MORE capabilities."
  White text on next line: "Hades is designed to REMOVE the burden of coordinating them."

==============================================
SLIDE 03 — COMPETITIVE GAP MATRIX
==============================================

HEADLINE: "WHERE EXISTING AI SYSTEMS STOP"

Create a full comparison matrix table:

Rows (left column, white text):
  Conversation
  Persistent Identity
  Long-Term Memory
  Goal Understanding
  Human Alignment Gate
  Multi-Model Orchestration
  Tool Orchestration
  Background Execution
  Output Validation
  Human Goal Authority
  Continuous Relationship

Columns (3):
  TRADITIONAL AI ASSISTANT | AI AGENT | HADES

Cells content — use emoji icons:
  ✅ = Implemented/Yes
  ⚡ = Partial  
  ❌ = No/Missing

Fill values:
Traditional AI:
  Conversation ✅ | Persistent Identity ❌ | Long-Term Memory ❌ | Goal Understanding ⚡ | 
  Human Alignment ❌ | Multi-Model ❌ | Tool Orch ❌ | Background Exec ❌ | 
  Output Validation ❌ | Human Goal Authority ❌ | Continuous Relationship ❌

AI Agent:
  Conversation ⚡ | Persistent Identity ❌ | Long-Term Memory ⚡ | Goal Understanding ⚡ | 
  Human Alignment ❌ | Multi-Model ⚡ | Tool Orch ✅ | Background Exec ✅ | 
  Output Validation ❌ | Human Goal Authority ❌ | Continuous Relationship ❌

HADES:
  Conversation ✅ | Persistent Identity ✅ | Long-Term Memory ⚡ | Goal Understanding ✅ | 
  Human Alignment ✅ | Multi-Model ✅ | Tool Orch ✅ | Background Exec ✅ | 
  Output Validation ✅ | Human Goal Authority ✅ | Continuous Relationship ⚡

Style: HADES column has a violet left-border accent, slightly glowing background.
Mark ⚡ cells in amber color. ✅ in green. ❌ in red.

BOTTOM: 
  Violet box (full width, centered):
  "RESEARCH / DESIGN GAP:"
  White text: "Persistent understanding + mutual alignment + intelligence orchestration + verified execution"
  "— No existing system combines all four. Hades targets this gap."

==============================================
SLIDE 04 — MISSION LOCK: THE EXECUTION GATE
==============================================

HEADLINE: "HADES DOESN'T START WITH A TASK."
SUBHEAD (violet): "IT STARTS WITH UNDERSTANDING."

MAIN VISUAL: Vertical pipeline (centered, large, takes most of the slide):

Step pills connected by animated vertical lines:

  ① USER INTENT        [badge: INPUT]
       ↓
  ② CONVERSATION       [badge: IMPLEMENTED ✅]
       ↓
  ③ CLARIFICATION      [badge: IMPLEMENTED ✅]
       ↓  
  ④ PUSHBACK / ALIGN   [badge: IMPLEMENTED ✅]
       ↓
  ⑤ MUTUAL UNDERSTANDING [badge: IMPLEMENTED ✅]
       ↓
  ████████████████████████████████
  ⑥  🔒  MISSION LOCK  [badge: IMPLEMENTED ✅]
  ████████████████████████████████
       ↓
  ⑦ PLANNING           [badge: PARTIAL ⚡]
       ↓
  ⑧ EXECUTION          [badge: IMPLEMENTED ✅]
       ↓
  ⑨ REVIEW             [badge: IMPLEMENTED ✅]
       ↓
  ⑩ DELIVERY           [badge: IMPLEMENTED ✅]

Style for MISSION LOCK step:
- Full-width highlight box, violet gradient background
- Large lock emoji 🔒
- Text: "MISSION LOCK" in white, font-weight 900
- Subtitle: "No execution without mutual understanding"
- Glowing border: box-shadow: 0 0 40px rgba(124,58,237,0.6)

LEFT SIDE annotation (small vertical text or callout):
  "BEFORE LOCK: Hades can reason, clarify, push back — but CANNOT execute."

RIGHT SIDE annotation:
  "AFTER LOCK: Execution Brain takes control. User controls the goal, not the process."

BOTTOM statement (centered, italic, subtle):
  "Conversation is the authorization layer between intent and action."
  File reference: "understanding_evaluator.py · mission.py → MissionStatus.AUTHORIZED_EXECUTION"

==============================================
SLIDE 05 — LAYERED ARCHITECTURE
==============================================

HEADLINE: "ONE PARTNER."
SUBHEAD: "MULTIPLE BRAINS. MANY CAPABILITIES."

MAIN VISUAL: Horizontal layer stack (like OS layers), full width.
Each layer is a full-width panel with rounded corners, distinct background shade.

Layer 1 (top): USER
  Background: rgba(255,255,255,0.03)
  Label: "USER"  Subtitle: "Goal • Context • Decisions"
  Right badge: [HUMAN IN CONTROL]

Layer 2: PARTNER BRAIN
  Background: rgba(124,58,237,0.15), border: 1px solid rgba(124,58,237,0.4)
  Label: "PARTNER BRAIN"
  Sub-items in a row: "Intent Classification" | "Mission Extraction" | "Conversational Alignment" | "Session Memory"
  Right badge: [IMPLEMENTED ✅]
  File ref: "partner_brain.py · intent_classifier.py · understanding_evaluator.py"

Layer 3: MISSION LOCK (thinner bar)
  Background: linear-gradient(90deg, rgba(124,58,237,0.4), rgba(109,40,217,0.4))
  Full-width bold bar: "🔒 MISSION LOCK — MUTUAL UNDERSTANDING GATE"
  Right badge: [IMPLEMENTED ✅]

Layer 4: EXECUTIVE BRAIN
  Background: rgba(124,58,237,0.1), border: 1px solid rgba(124,58,237,0.3)
  Label: "EXECUTIVE BRAIN"
  Sub-items: "Task Graph" | "Worker Delegation" | "Recovery/Retry"
  Right badge: [PARTIAL ⚡]
  Note below in amber: "Currently generates 1 task; dynamic decomposition is a future milestone"
  File ref: "execution_brain.py"

Layer 5: WORKERS
  Background: rgba(16,185,129,0.05), border: 1px solid rgba(16,185,129,0.2)
  Label: "WORKERS"
  Sub-items in pills: "Terminal" | "Filesystem" | "Process Manager" | "Browser (partial)" 
  Right badge: [PARTIAL ⚡]
  Note below in amber: "Current workers = model endpoints via WorkerManager; autonomous worker agents = future"
  File ref: "worker_manager.py · skills/"

Layer 6: MODELS
  Background: rgba(16,185,129,0.05)
  Label: "MODEL PROVIDERS"
  Sub-items: "Gemini (Google)" | "Llama 3.3 (Groq)" | "OpenRouter" | "Ollama (Local)"
  Right badge: [IMPLEMENTED ✅]

Layer 7: REVIEW ENGINE
  Background: rgba(124,58,237,0.08)
  Label: "REVIEW ENGINE"
  Sub-items: "Exit Code Validation" | "Artifact Check" | "Semantic Review"
  Right badge: [IMPLEMENTED ✅]
  File ref: "review_engine.py"

Layer 8 (bottom): MEMORY
  Background: rgba(245,158,11,0.05), border: 1px solid rgba(245,158,11,0.2)
  Label: "MEMORY"
  Sub-items: "Session (in-memory)" | "Mission History (JSON)"
  Right badge: [PARTIAL ⚡]
  Note in amber: "Vector/RAG memory = future milestone"
  File ref: "memory_manager.py"

==============================================
SLIDE 06 — MISSIONS, NOT PROMPTS
==============================================

HEADLINE: "HADES THINKS IN MISSIONS."
SUBHEAD (muted): "Not prompts. Not sessions. Not tabs."

TWO-COLUMN layout:

LEFT — "TRADITIONAL AI (Prompt Loop)":
  Show a simple loop diagram:
  [ USER ] → Prompt → [ AI ] → Response → [ USER ] → Prompt → ...
  
  Label: "Context: None"
  Label: "State: Disposable"
  Label: "Memory: Zero"
  Label: "Continuity: None"
  Each in red badge style.

  Annotation: "Every message starts from scratch."

RIGHT — "HADES MISSION OBJECT":
  Show a structured card with all Mission fields:
  
  Card title: "MISSION STATE OBJECT" (monospace font)
  Fields in two columns:
  
  🎯 objective:          "Build a project scaffold..."
  📋 desired_outcome:    "Working directory with..."
  ⚠️  constraints:       ["No external deps", ...]
  ✅ success_criteria:   "Directory exists, tests pass"
  📊 status:             BACKGROUND_WORK
  🔒 mutual_understanding: true
  📝 conversation_history: [14 messages]
  💾 mission_id:         "m_8f3a..."
  🏆 output_artifacts:   ["scaffold.zip", ...]
  
  Bottom: File ref: "src/models/mission.py"

BELOW THE COLUMNS — State Machine diagram (full width):

  [ CONVERSATION ] ──► [ AUTHORIZED_EXECUTION ] ──► [ BACKGROUND_WORK ] ──► [ COMPLETED ]
                                                                          └──► [ NEEDS_USER ]
  
  Each state as a rounded box. Transitions as arrows with labels.
  Color: CONVERSATION = muted, AUTHORIZED_EXECUTION = violet, BACKGROUND_WORK = amber, 
         COMPLETED = green, NEEDS_USER = amber.

BOTTOM: Two-row annotation:
  Row 1 (green badge): "Mission abstraction — IMPLEMENTED"
  Row 2 (amber badge): "Dynamic multi-step planning — FUTURE MILESTONE"

==============================================
SLIDE 07 — INTELLIGENCE ORCHESTRATION
==============================================

HEADLINE: "HADES MANAGES AI."
SUBHEAD (violet): "THE USER DOESN'T."

MAIN VISUAL: Central routing diagram.

Center: Large hexagon or circle labeled "WORKER MANAGER"
  Subtitle inside: "capability-based routing · provider fallback · model agnostic"
  File ref: "worker_manager.py"

Lines radiating from center to provider cards:

LEFT PROVIDERS (inputs):
  Card: GEMINI 2.5 Flash  | google | capability: conversational, fast
  Card: Gemini Flash Latest | google | capability: research, analysis  
  Card: Llama 3.3 70B     | groq   | capability: fast, open-source
  Card: Llama 3.2 3B      | openrouter | capability: free, public
  Card: Local Ollama       | local  | capability: private, offline
  (mark local as FAILED/partial in config)

RIGHT OUTPUTS (what routing enables):
  → Conversational response
  → Mission extraction
  → Command generation
  → Review / validation
  → Future: specialized analysis

BELOW CENTER — 3 mechanism cards (full width row):

Card 1: "INVISIBLE TO USER"
  "Users express goals. Hades selects the right model for each task internally."

Card 2: "PROVIDER FALLBACK"  
  "If primary model fails, WorkerManager automatically tries next configured provider."
  "No interruption. No manual switching."

Card 3: "REPLACEABLE"
  "Any provider can be added or removed from config.json."
  "The system is not coupled to any one vendor."

BOTTOM HONEST CALLOUT (amber border box):
  "⚡ CURRENT REALITY: Workers are model endpoints routed by LiteLLM."
  "Autonomous specialized worker agents with independent loops — FUTURE MILESTONE."

==============================================
SLIDE 08 — REVIEW ENGINE
==============================================

HEADLINE: "AI DOESN'T GET TO DECLARE ITSELF SUCCESSFUL."

This slide should feel like a strict system diagram.

SUBHEAD (violet): "GENERATION ≠ COMPLETION"

MAIN VISUAL: Vertical validation pipeline (centered, large):

[ WORKER OUTPUT ]
        ↓
┌─────────────────────────────┐
│  STAGE 1: EXIT CODE CHECK   │
│  exit_code == 0 ?           │
│  Source: review_engine.py   │
└─────────────────────────────┘
        ↓ pass →
┌─────────────────────────────┐
│  STAGE 2: ARTIFACT CHECK    │
│  Does output.txt exist?     │
│  File paths from criteria   │
└─────────────────────────────┘
        ↓ pass →
┌─────────────────────────────┐
│  STAGE 3: HEURISTIC CHECK   │
│  Output matches expectations?│
│  Sanity validation layer    │
└─────────────────────────────┘
        ↓ ambiguous →
┌─────────────────────────────┐
│  STAGE 4: SEMANTIC REVIEW   │
│  LLM validates output vs    │
│  success_criteria           │
└─────────────────────────────┘
        ↓
  ┌──────────┐    ┌──────────────┐
  │  ✅ PASS  │    │ 🔄 RETRY     │
  │  DELIVER  │    │ Re-prompt LLM│
  │  TO USER  │    │ with error   │
  └──────────┘    └──────────────┘

All boxes: dark panel cards, violet borders for passing stages, amber for RETRY path.

RIGHT SIDE — two annotation cards:

Card 1 (green):
  "WHY THIS MATTERS"
  "LLMs generate plausible output, not guaranteed correct output.
  The Review Engine is the difference between an AI assistant 
  and a reliable AI system."

Card 2 (violet):
  "RETRY MECHANISM"
  "On RETRY: the failed output + error message are fed back to the 
  ExecutionBrain as context. The LLM attempts a different command.
  Max retries enforced."

BOTTOM: Full-width statement, large font:
  "The worker delivers a result. The Review Engine determines if the 
  MISSION was actually completed."

==============================================
SLIDE 09 — THE INTERFACE
==============================================

HEADLINE: "THE INTERFACE IS A CONTROL SURFACE"
SUBHEAD (violet): "FOR A LIVING MISSION."

LEFT HALF — Interface flow diagram (vertical):

  [ VOICE INPUT ]           ← Web Speech API (browser STT)
       ↓
  [ REACT / VITE UI ]       ← frontend/src/ — IMPLEMENTED
       ↓
  POST /api/chat
       ↓
  [ FASTAPI BACKEND ]        ← main.py — IMPLEMENTED
       ↓
  [ PARTNER BRAIN ]          ← IMPLEMENTED
       ↓
  [ MISSION LOCK ]           ← IMPLEMENTED  
       ↓
  [ EXECUTION BRAIN ]        ← PARTIAL
       ↓
  SSE /api/events (real-time)← IMPLEMENTED
       ↓
  [ LIVE UI UPDATES ]        ← "System Activity" feed
       ↓
  [ HADES VOICE RESPONSE ]   ← Kokoro-ONNX TTS → Base64 → HTML5 Audio

RIGHT HALF — 4 interface capability cards:

Card 1 (green):
  "REAL-TIME EVENTS"
  "Server-Sent Events stream every background execution step to the UI.
  Task started → capability selected → task completed → mission delivered.
  User sees Hades working, not just a spinner."

Card 2 (green):  
  "BACKEND TTS"
  "Kokoro-ONNX generates local speech synthesis on the backend.
  Audio encoded as Base64 in the JSON response.
  No cloud TTS dependency."

Card 3 (amber):
  "VOICE INPUT"
  "Currently: browser window.SpeechRecognition (Web Speech API).
  Backend Whisper STT is not yet implemented."

Card 4 (green):
  "SESSION PERSISTENCE"
  "Session ID stored in localStorage.
  Conversation history maintained for current session.
  Survives page refresh — not server restart."

BOTTOM: Component ref bar (monospace, muted):
  "frontend/src/services/HadesService.ts · main.py · voice_manager.py"

==============================================
SLIDE 10 — END-TO-END MISSION PROOF
==============================================

HEADLINE: "ONE SENTENCE → REAL COMPUTER ACTION"

SUBHEAD: Mission statement (in a terminal-style card):
  > "List all files in the current directory and save them to output.txt."

MAIN VISUAL: Timeline (horizontal or stepped vertical), 13 steps, numbered.

Each step is a compact card with:
  - Step number
  - System layer (colored pill)
  - Action label
  - Code/file ref

Step 1:  [USER]         User types or speaks the command
Step 2:  [FRONTEND]     HadesService.sendMessage → POST /api/chat
Step 3:  [API]          main.py receives, looks up SessionState by UUID
Step 4:  [PARTNER]      IntentClassifier → classifies as SMALL_TASK
Step 5:  [PARTNER]      MissionExtractor → populates MissionUnderstanding fields
Step 6:  [LOCK]         UnderstandingEvaluator → all fields populated → AUTHORIZED_EXECUTION
Step 7:  [API]          asyncio.create_task(execution_brain.process_mission) — HTTP returns immediately
Step 8:  [EXEC]         ExecutionBrain._generate_plan → 1-task TaskGraph created
Step 9:  [WORKER]       WorkerManager routes to Gemini → LLM generates: "ls -la > output.txt"
Step 10: [TOOL]         TerminalSkill.execute() → asyncio.create_subprocess_shell → runs on host
Step 11: [REVIEW]       ReviewEngine: exit_code==0 ✅ · output.txt exists on disk ✅
Step 12: [MEMORY]       memory_manager.add_mission_to_history() → appends to memory.json
Step 13: [SSE]          EventSource emits MISSION_COMPLETED → UI updates → Hades speaks result

Color code each step by layer:
  USER = white | FRONTEND = violet | API = indigo | PARTNER = violet | 
  LOCK = glowing violet | EXEC = amber | WORKER = green | 
  TOOL = green | REVIEW = teal | MEMORY = muted | SSE = green

BOTTOM: Full-width pipeline summary:
  "CONVERSATION → MISSION LOCK → ASYNC EXECUTION → VERIFICATION → DELIVERY"
  Shown as connected nodes (pill chain).

==============================================
SLIDE 11 — MATURITY MATRIX
==============================================

HEADLINE: "THE PROTOTYPE IS REAL."
SUBHEAD (amber): "BUT IT IS NOT FINISHED."

Create a 3-column status matrix. Each item is a compact card row.

GREEN COLUMN — "IMPLEMENTED":
  ✅ Conversation Flow (partner_brain.py)
  ✅ Intent Classification (intent_classifier.py)
  ✅ Mission Extraction (mission_extractor.py)
  ✅ Mission State Machine (mission.py — 5 states)
  ✅ Mission Lock Gate (understanding_evaluator.py)
  ✅ WorkerManager + LiteLLM (worker_manager.py)
  ✅ Multi-Provider Routing (Gemini, Groq, OpenRouter, Ollama)
  ✅ Terminal Skill (skills/computer/terminal.py)
  ✅ Filesystem Skill (skills/computer/filesystem.py)
  ✅ Process Manager (skills/computer/process_manager.py)
  ✅ Review Engine — exit code + artifact + semantic (review_engine.py)
  ✅ Server-Sent Events stream (main.py /api/events)
  ✅ React/Vite Frontend (frontend/src/)
  ✅ Full E2E execution path
  ✅ Backend TTS — Kokoro-ONNX (voice_manager.py)
  ✅ Session persistence (localStorage)

AMBER COLUMN — "PARTIAL / IN PROGRESS":
  ⚡ Worker specialization (endpoints only; no agent loops)
  ⚡ Task decomposition (hardcoded to 1 task in execution_brain.py)
  ⚡ Session memory (in-memory only; lost on restart)
  ⚡ Mission memory (flat JSON; no semantic retrieval)
  ⚡ Voice input (browser SpeechRecognition; no Whisper)
  ⚡ Browser skill (playwright wrapper; unverified E2E)
  ⚡ Equal partnership guardrails (LLM prompt-based; not deterministic)

RED COLUMN — "NOT YET IMPLEMENTED":
  🔴 Dynamic multi-step TaskGraph decomposition
  🔴 Autonomous specialized worker agents
  🔴 RAG / Vector semantic memory
  🔴 Backend Whisper STT
  🔴 Docker/sandbox isolation for terminal
  🔴 Execution security hardening
  🔴 Deep Linux/systemd/D-Bus integration
  🔴 Structured logging and observability
  🔴 Comprehensive test suite (1 test file exists)
  🔴 Production-grade automation
  🔴 Cross-session persistent identity

BOTTOM: Large centered statement (not an apology — technical confidence):
  "Working prototype. Known gaps. Clear engineering path forward."
  Badge: "CORE LOOP: PROVEN"  |  Badge: "AI OS: IN PROGRESS"

==============================================
SLIDE 12 — NOVELTY CARDS
==============================================

HEADLINE: "WHAT HADES ACTUALLY CONTRIBUTES"

7 cards in a 3+2+2 grid layout. Each card is a dark panel.

CARD 1 — "MUTUAL UNDERSTANDING GATE"
  Large number: "01"
  Icon: 🔒
  Bold title: "MUTUAL UNDERSTANDING GATE"
  Body: "Conversation is not just UX — it is the authorization layer.
  Execution is gated by a deterministic state check: 
  objective + desired_outcome + success_criteria + mutual_understanding_reached.
  No other AI system implements explicit human-alignment verification before tool use."
  Badge: IMPLEMENTED · understanding_evaluator.py

CARD 2 — "MISSION-CENTRIC COMPUTING"
  Number: "02"  Icon: 🎯
  Title: "MISSION-CENTRIC COMPUTING"
  Body: "Prompts are disposable. Missions are persistent units of work with 
  structured fields: objective, constraints, success criteria, state, and outcome.
  The mission survives across the conversation, execution, review, and memory lifecycle."
  Badge: IMPLEMENTED · mission.py

CARD 3 — "PARTNER + EXECUTIVE DUALITY"
  Number: "03"  Icon: 🧠
  Title: "PARTNER + EXECUTIVE DUALITY"
  Body: "Two isolated cognitive systems. Partner Brain handles conversation and 
  alignment — it never touches tools. Executive Brain handles planning and execution — 
  it never engages the user directly. This prevents the classic agent failure mode 
  where execution and conversation contaminate each other."
  Badge: IMPLEMENTED · partner_brain.py + execution_brain.py

CARD 4 — "INVISIBLE INTELLIGENCE ORCHESTRATION"
  Number: "04"  Icon: ⚙️
  Title: "INVISIBLE ORCHESTRATION"
  Body: "The user expresses a goal in natural language. Hades internally classifies 
  the required capability, selects the appropriate model from multiple providers, 
  routes the prompt, collects the result, and validates it — all without the user 
  knowing which model was used or why. Intelligence becomes infrastructure."
  Badge: IMPLEMENTED · worker_manager.py + config.json

CARD 5 — "VERIFICATION-FIRST EXECUTION"
  Number: "05"  Icon: ✅
  Title: "VERIFICATION-FIRST EXECUTION"
  Body: "Workers generate output. The Review Engine determines if the mission 
  was actually completed. 4-stage validation: exit code → artifact existence → 
  heuristic check → LLM semantic review. If validation fails, the system retries 
  with the error as context. Generation is not success."
  Badge: IMPLEMENTED · review_engine.py

CARD 6 — "MODEL-AGNOSTIC AI LAYER"
  Number: "06"  Icon: 🔄
  Title: "MODEL-AGNOSTIC AI LAYER"
  Body: "LiteLLM wraps Google, Groq, OpenRouter, and local Ollama behind a 
  unified interface. Provider fallback is automatic. New models added via config.json 
  without code changes. The system is not architecturally coupled to any vendor, 
  ensuring longevity as the model landscape evolves."
  Badge: IMPLEMENTED · worker_manager.py + LiteLLM

CARD 7 — "PERSISTENT HUMAN-AI RELATIONSHIP"
  Number: "07"  Icon: 🤝
  Title: "PERSISTENT RELATIONSHIP"
  Body: "Mission history, conversation context, and user identity persist across 
  interactions. Hades addresses users by name, recalls past missions, and uses 
  that context to inform new conversations — laying the foundation for genuine 
  long-term AI partnership, not session-scoped Q&A."
  Badge: PARTIAL (JSON memory today; RAG = future)

BOTTOM (full width, centered, large italic):
  "The novelty is not another smarter model."
  Next line in violet: "It is a system that organizes intelligence around human intent."

==============================================
SLIDE 13 — ROADMAP & FINAL STATEMENT
==============================================

HEADLINE: "FROM WORKING PROTOTYPE"
SUBHEAD (violet): "TO TRUE AI OPERATING SYSTEM"

MAIN VISUAL: 3-column progression (like OS version releases)

COLUMN 1 — "TODAY · PROTOTYPE" [green top border]:
  Large label: "v0.1"
  Items (green checkmarks):
  ✅ Partner Brain conversational loop
  ✅ Mission Lock authorization
  ✅ Multi-provider model routing
  ✅ Terminal + filesystem execution
  ✅ Review Engine validation
  ✅ Real-time SSE event stream
  ✅ Backend TTS (Kokoro-ONNX)
  ✅ Complete E2E execution path
  
  Bottom badge: "CORE LOOP: PROVEN"

COLUMN 2 — "NEXT · HARDENING" [amber top border]:
  Large label: "v0.2"
  Items (amber arrows):
  → Dynamic TaskGraph decomposition
  → True multi-step mission execution
  → Docker sandbox for terminal safety
  → Whisper backend STT
  → Specialized autonomous workers
  → Vector/RAG semantic memory
  → Security hardening
  → Structured logging
  → E2E test suite

  Bottom badge: "KNOWN ENGINEERING PROBLEMS"

COLUMN 3 — "VISION · AI OS" [violet top border]:
  Large label: "v1.0"
  Items (violet diamonds):
  ◆ Persistent cross-device identity
  ◆ Autonomous mission scheduling
  ◆ Event-driven background missions
  ◆ Plugin/skill ecosystem
  ◆ Distributed multi-node execution
  ◆ Local + cloud intelligence blend
  ◆ Long-term human-AI partnership
  ◆ Deep Linux/systemd integration
  ◆ Proactive goal suggestions

  Bottom badge: "THE ACTUAL AI OS VISION"

BELOW COLUMNS — Full-screen final statement:

Thin violet line (full width)

Giant text (centered, 2 lines):
  "HUMAN SETS THE MISSION."
  (font-size: clamp(2rem, 5vw, 3.5rem), font-weight: 900, color: white)
  
  "HADES ORCHESTRATES THE INTELLIGENCE."
  (same size, color: #a78bfa — the glow/lavender)

Thin violet line (full width)

Footer (small, centered, muted):
  "Today Hades proves the loop.  The next phase proves the system."

Very bottom: "PROJECT HADES · AI OPERATING SYSTEM PROTOTYPE · 2025"

==============================================
TECHNICAL REQUIREMENTS
==============================================

1. Use reveal.js 5.x from CDN:
   https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css
   https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js
   
2. Initialize reveal.js with:
   Reveal.initialize({
     hash: true,
     transition: 'fade',
     transitionSpeed: 'slow',
     controls: false,
     progress: false,
     slideNumber: true,
     center: false
   });

3. Every animated element uses CSS animations (keyframes) not JS animations.

4. The pipeline arrows use CSS:
   content: '→' with color: #a78bfa and animation: pulse 2s infinite

5. The grid background is CSS-only, applied to body.

6. Use CSS Grid and Flexbox throughout — no tables except for the comparison matrix.

7. The comparison matrix in slide 03 uses an HTML table with custom CSS.

8. Add a tiny "HADES" wordmark in the top-left corner of every slide (position: fixed).
   Font: monospace, color: rgba(124,58,237,0.4), font-size: 0.7rem, letter-spacing: 0.2em

9. Make it fully keyboard navigable (reveal.js default).

10. Output a single complete index.html file. No external files. All CSS inline in <style>. 
    All JS inline in <script>. The file must work offline.

DO NOT USE: Bootstrap, Tailwind, jQuery, or any other framework.
DO NOT USE: placeholder images. Use CSS shapes and diagrams only.
DO NOT USE: cheesy robot emojis or generic tech stock imagery.
MAKE IT FEEL: Like a premium mission-control developer tool, not a school project.
```
