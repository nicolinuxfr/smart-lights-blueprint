# Instructions

- For any requested blueprint change, always apply the change in `template.yaml`.
- Always update all translation files in parallel when a blueprint text/key is changed.
- Update also all the README files accordingly.
- Change the version number inside the `VERSION` file only when asked to. Do not change it if I did not ask first, but you can suggest to update it when big changes are done.
- Respect this CalVer format: `YYYY.mm.x`
  - First release of the month: `YYYY.mm` (no suffix)
  - Subsequent releases same month: `YYYY.mm.2`, `YYYY.mm.3`, etc.
- If we change the version number, automatically add it to the `CHANGELOG` file and add a bullet point of main changes but always let me verify and edit them.

## Include system

Reusable YAML snippets live in `includes/`. The build script (`scripts/generate_blueprints.py`) resolves `[[include:filename.yaml]]` directives in `template.yaml` **before** i18n placeholder substitution.

- Include paths are relative to `--includes-dir` (default: `includes/`).
- Indentation is automatic: the snippet is indented to match the column where the `[[include:...]]` token appears.
- Include files may contain `[[i18n.key]]` placeholders — they are resolved in the next pass.
- Current includes:
  - `adaptive_variables.yaml` — sun position, weather factor, adaptive curve, brightness/kelvin computation (shared by all adaptive paths).
  - `light_capability_variables.yaml` — per-light capability detection (`supports_ct`, `supports_brightness`, `clamped_kelvin`). Expects a `current_light` variable to be set before inclusion.
  - `light_update_choose.yaml` — choose branches for per-light updates based on capabilities (brightness+CT, brightness only, CT only). Expects `current_light`, `effective_brightness`, `clamped_kelvin`, `supports_brightness`, `supports_ct`.
