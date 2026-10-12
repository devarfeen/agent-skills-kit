# Design-system source selection

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

- **DESIGN-SYSTEM SOURCE (required)** — a source the user names wins. Otherwise discover in order; use the first found and name it in `Found:`:
  1. A root `DESIGN.md` (workspace or project) — link it from the doc.
  2. A brand, UI, or UI/UX skill (surveyed per **The project UI skill**) or a component library in the codebase; read it as the written source.
  3. A **Figma** file/URL (via the Figma MCP companion — not installed → say so and ask for exported frames/tokens or a written spec); a **written design spec / brand guide**; **reference screens or a reference app**; or, when none exists, a **guided-definition session** — open with the one thing a user should remember, then propose colours, neutrals, typography, type scale, spacing, radius, shadow, and base components, each with a reason; build only after **explicit user approval**.

  A source that already holds tokens stays the single token source of truth; never create a second token set beside it. **Never fabricate a whole design system silently.** No source and no approved guided session → stop and ask.
