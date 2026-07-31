# RH custom-agent profiles

These profiles mirror the durable roles in `AGENTS.md`.  The primary session
may load them through Codex custom-agent support when available; otherwise it
must pass the same profile text to spawned subagents explicitly.

The concurrency ceiling is three subagents because the primary agent occupies
the fourth session slot.  `rh-release-qa` replaces another station after a
draft; it is not a fourth concurrent subagent.

The profiles never grant commit, push, handoff-edit, or cross-paper write
authority.  Runtime permissions and the primary agent's explicit task remain
authoritative over these descriptive manifests.
