# Renderer Vertical Slice

The Sprint 1 implementation proves the narrow renderer path before the API and persistence contracts are broadened.

The shared application layer accepts an engine-neutral request, normalizes source, selects a direct adapter, validates SVG, derives PNG/PDF, validates file signatures, and only then creates the caller's output directory. Renderer-specific command construction remains inside the adapter modules.

If the SVG-first spike clips content, changes material layout, or exceeds the approved resource envelope, the architecture keeps the direct adapters and permits engine-native PNG or PDF output for the affected format. Such a change requires an ADR update; it must not be introduced silently.
