# Graphs, Designs, and Patterns

This folder collects visual documentation for how `pygame_handler` currently works and the design ideas visible in the code.

> The diagrams describe the current implementation, not a guarantee that every planned feature is complete. Known implementation gaps are called out explicitly.

## Contents

- [Graphs](graphs.md) — runtime frame flow, component relationships, and event dispatch.
- [Design overview](designs.md) — component responsibilities, scene lifecycle, and safe extension points.
- [Design patterns](patterns.md) — patterns used or approached by the implementation, with caveats where behavior is incomplete.

The graphs use Mermaid inside Markdown, so GitHub can render them directly without maintaining exported image files. When a diagram changes, update the corresponding Mermaid source in this folder.
