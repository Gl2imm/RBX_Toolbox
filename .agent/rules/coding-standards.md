---
trigger: always_on
---

# Coding Standards

This document defines coding standards for the Blender-to-Roblox integration project. All code changes should follow these guidelines.

---

## 1. Naming Conventions (Multi-Language)

### Python (Blender Addon)
* **Variables/Functions:** `snake_case` (e.g., `def export_mesh():`)
* **Classes:** `PascalCase` (strictly for `bpy` types like `class ROBLOX_OT_Export(bpy.types.Operator):`)
* **Constants:** `UPPER_SNAKE_CASE` (e.g., `ROBLOX_API_URL`)

### Luau (Roblox)
* **Variables/Parameters:** `camelCase` (e.g., `local playerPosition`)
* **Services/Classes:** `PascalCase` (e.g., `ReplicatedStorage`)

---

## 2. Code Readability

### Break Long Lines
Split long statements into multiple lines for clarity (applies to both Lua and Python).

**Luau Example:**
```lua
-- ✅ CORRECT
local mainLabel = Instance.new("TextLabel", screenGui)
mainLabel.Name = "MainStatus"
mainLabel.Size = UDim2.new(0.6, 0, 0.1, 0)
mainLabel.Position = UDim2.new(0.2, 0, 0.1, 0)
mainLabel.BackgroundTransparency = 1

-- ❌ AVOID
local mainLabel = Instance.new("TextLabel", screenGui); mainLabel.Name = "MainStatus"; mainLabel.Size = UDim2.new(0.6, 0, 0.1, 0)
```

**Python Example:**
```python
# ✅ CORRECT
bpy.ops.mesh.primitive_cube_add(
    size=2, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0)
)
```

### Split Complex Conditionals
Do not combine complex logic into single lines.

```lua
-- ✅ CORRECT
if isSpectating then
    lobbyActionEvent:FireServer("Spectate")
    spectateButton.Text = "TO LOBBY"
else
    lobbyActionEvent:FireServer("ToLobby")
    spectateButton.Text = "SPECTATE"
end
```

---

## 3. Blender & API Specifics

### Context Safety
* **Validation:** Never assume `bpy.context.active_object` exists. Always check `if obj is not None:` before operations.
* **Operators:** Avoid `bpy.ops` in loops where possible. Use direct data manipulation (`obj.data.vertices[0].co`) or `bmesh` for performance.

### API Error Handling
* **Network Calls:** All Roblox API requests from Python must be wrapped in `try/except` blocks to handle connection failures or 403 errors gracefully.

---

## 4. Documentation & Comments

### Add Comments For:
* **Coordinate Conversion:** Explicitly comment where Z-up (Blender) is converted to Y-up (Roblox).
* **Bug fixes:** Explain what was broken and why the fix works.
* **Non-obvious logic:** Complex calculations or state management.

### Examples:

```python
# BUG FIX: Ensure mode is explicitly set to OBJECT before export
bpy.ops.object.mode_set(mode='OBJECT')
```

---

## 5. Indentation

* **Python:** Use **4 spaces** (Standard PEP 8).
* **Luau:** Use **Tabs** (Roblox Standard).
* **Consistency:** Do not mix tabs and spaces in the same file.