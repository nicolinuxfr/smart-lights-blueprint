# Instructions

- For any requested blueprint change, always apply the change in `template.yaml`.
- Always update all translation files in parallel when a blueprint text/key is changed.
- Update also all the README files accordingly.
- Only change the README files if instructed or if it wad changed in the other languages. Otherwise, left it untouched.
- Change the version number inside the `VERSION` file only when asked to. Do not change it if I did not ask first, but you can suggest to update it when big changes are done.
- Respect this CalVer format: `YYYY.m.x`
  - Do not zero-pad the month: use `2026.7`, not `2026.07`.
  - First release of the month: `YYYY.m` (no suffix)
  - Subsequent releases same month: `YYYY.m.2`, `YYYY.m.3`, etc.
- If we change the version number, automatically add it to the `CHANGELOG` file and add a bullet point of main changes but always let me verify and edit them.

## Include system

Reusable YAML snippets live in `includes/`. The build script (`scripts/generate_blueprints.py`) resolves `[[include:filename.yaml]]` directives in `template.yaml` **before** i18n placeholder substitution.

- Include paths are relative to `--includes-dir` (default: `includes/`).
- Indentation is automatic: the snippet is indented to match the column where the `[[include:...]]` token appears.
- Include files may contain `[[i18n.key]]` placeholders — they are resolved in the next pass.
- Includes are resolved in a single pass. Do not put `[[include:...]]` directives inside included files.
- Current include layout:
  - `inputs.yaml` — all blueprint inputs and sections in one file.
  - `variables.yaml` — shared runtime variables and feature-flag derivation from public inputs.
  - `triggers.yaml` — all auto on/off and adaptive trigger blocks.
  - `conditions.yaml` — top-level guard conditions for event validity and adaptive gating.
  - `adaptive_variables.yaml` — shared adaptive runtime variables reused in several action branches.
  - Context-specific adaptive per-light logic and switch-toggle state stay directly in `template.yaml` to avoid over-splitting includes.
