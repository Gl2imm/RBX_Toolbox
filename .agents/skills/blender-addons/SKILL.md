---
name: blender-addons-reference
description: Reference library for Blender addon development. Contains examples of working code, UI patterns, and tool implementations from other addons. Use this skill when you need inspiration or working examples for specific features.
---

# Blender Addons Reference Skill

## Purpose
This skill serves as a repository of reference implementations for Blender addons. It contains examples of UI layouts, operator logic, and other common patterns used in Blender addon development.

## When to Use
- **UI Design**: When you need examples of specific UI elements (panels, menus, popups).
- **Feature Implementation**: When looking for how a specific feature was implemented in another addon.
- **Legacy Support**: When adapting code from older Blender versions to the current API.
- **Best Practices**: When looking for established patterns for structure and organization.

## Structure
The skill is organized into folders (to be populated):
- `ui_examples/`: Examples of panels, menus, and custom UI elements.
- `operators/`: Examples of specific operator implementations.
- `tools/`: Examples of complete tools or utilities.

## Instructions
1.  **Search**: Look through the examples to find relevant code.
2.  **Adapt**: Do not copy-paste directly if the code is from an older Blender version. always verify compatibility with the current `bpy` API (Blender 4.0+).
3.  **Reference**: Use the logic and structure as a guide for your implementation.
4.  **Copyright**: Make sure when you reference or copy a part of code to rename variable, rephrase or restructure code where possible and if there are notes - do not copy one to one, create your own based on context

## Contributing
- users can add new examples to the relevant folders.
- Ensure examples are well-documented and, if possible, state the Blender version they were written for.
