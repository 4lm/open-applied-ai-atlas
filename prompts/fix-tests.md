# Fix Ralph Repo Consistency Tests

Tighten the non-`docs/` repo surface so the tracked guidance, Ralph controller behavior, example files, and tests all agree.

Required outcomes:

- keep Ralph unattended after the initial seed confirmation
- default to restricted sandboxing
- preserve an opt-in `dangerously-unrestricted` mode via profile
- keep the README examples runnable from tracked files
- keep `pips/PIP_001.md` as a live PIP
