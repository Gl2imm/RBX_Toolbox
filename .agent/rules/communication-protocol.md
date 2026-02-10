---
trigger: always_on
---

---
trigger: always_on
---

# Communication Protocols

This document defines the required communication standards for the agent.

## 1. File Type Specification
**Rule:** When creating any new file, you MUST explicitly state which file was created and placed at which location.

**Format:**
> Created `[Filename]`
> - **Location:** `[/Folder]`

## 2. Change Summary
**Rule:** After completing a set of changes, you MUST provide a structured summary of ALL files affected.

**Format:**
### Files Changed
- path/to/file1.py
### Files Created
- path/to/newfile1.py

## 3. Execution Style (High Velocity)
**Rule:** **NO implementation plans, NO walkthroughs, and NO task plans.**
- Do not ask for permission to start; proceed straight to the code changes.
- Keep prose to an absolute minimum.
- If a technical choice is ambiguous, pick the most standard pattern and move forward.

## 4. Contextual Awareness (Blender + Roblox)
**Rule:** Clearly distinguish between the Blender environment and Roblox API calls.
- **Blender Side:** Ensure `bpy` operations are context-safe (check for active objects/correct modes).
- **Roblox Side:** Use `requests` or `aiohttp` for Python-based Roblox API calls. Ensure clear error handling for HTTP 401/403 status codes.

## 5. General
- Always check `.agent/coding-standards.md` for code style.

## 6. Git Usage
**Rule:** Git is enabled for this workspace. Use it to track changes.