# Hades OS — Visual Walkthrough & Demo Recording

This artifact contains the visual proof of the Hades Intelligence Operating System running in its current state.

## Full Video Walkthrough

The following recording demonstrates:
1. The cinematic, single-viewport dashboard loading on `http://localhost:5173/`.
2. The user interacting with the main conversation composer.
3. The Settings Modal opening to reveal the dynamic skill registry health checks populated from the backend.

![Hades OS Video Walkthrough](C:\Users\HP\.gemini\antigravity-ide\brain\3298d95c-67e9-43b4-b020-54d233910f65\hades_os_demo_walkthrough.webp)

## Interaction Snapshots

### 1. Conversation Error State
As noted in the Knowledge Base's "Brutal Truth" section, the frontend chat architecture perfectly renders responses and error boundaries. Currently, communicating with Hades triggers a developer error due to a mismatch between LiteLLM and Google's `v1beta` endpoint for the `gemini-1.5-flash` alias.

![Message Error State](C:\Users\HP\.gemini\antigravity-ide\brain\3298d95c-67e9-43b4-b020-54d233910f65\message_sent_success_1786787959532.png)

### 2. Live Capability Registry
The Settings modal successfully connects to `/api/config/status` and reads the initialization state of all capabilities without crashing, ensuring secrets remain purely backend-managed.

![Capabilities Registry Status](C:\Users\HP\.gemini\antigravity-ide\brain\3298d95c-67e9-43b4-b020-54d233910f65\capabilities_modal_open_1786788534812.png)
