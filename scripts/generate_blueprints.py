#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(r"\[\[([a-zA-Z0-9_.-]+)\]\]")
INCLUDE_RE = re.compile(r"\[\[include:([a-zA-Z0-9_/.-]+)\]\]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render localized blueprint YAML files from a template and i18n dictionaries."
    )
    parser.add_argument("--template", default="template.yaml", help="Path to template YAML.")
    parser.add_argument("--i18n-dir", default="languages", help="Directory with <lang>.json files.")
    parser.add_argument("--output-dir", default="dist", help="Output directory for generated files.")
    parser.add_argument(
        "--default-lang",
        default="en",
        help="Fallback language code. Must exist in languages directory.",
    )
    parser.add_argument(
        "--filename",
        default="smart_lights.yaml",
        help="Filename used for each generated blueprint.",
    )
    parser.add_argument(
        "--version-file",
        default="VERSION",
        help="Path to plain-text version file injected as [[blueprint.version]].",
    )
    parser.add_argument(
        "--includes-dir",
        default="includes",
        help="Directory with reusable YAML snippet files for [[include:...]] directives.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"Expected object at top-level in {path}")

    out: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str):
            raise SystemExit(f"Non-string key in {path}: {key!r}")
        if not isinstance(value, str):
            raise SystemExit(f"Value for key {key!r} in {path} must be a string")
        out[key] = value
    return out


def load_version(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Version file not found: {path}")
    version = path.read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit(f"Version file is empty: {path}")
    return version


def build_version_line(template_value: str, version: str, lang: str) -> str:
    try:
        return template_value.format(version=version)
    except KeyError as exc:
        missing = exc.args[0]
        raise SystemExit(
            f"Dictionary '{lang}' has invalid blueprint.version.line placeholder "
            f"'{{{missing}}}'. Use '{{version}}'."
        ) from exc


def resolve_includes(template: str, includes_dir: Path) -> str:
    """Replace ``[[include:path]]`` tokens with the content of the referenced file.

    Indentation is preserved: subsequent lines of the included content are
    indented to match the column where the ``[[include:...]]`` token appeared.
    """
    if not INCLUDE_RE.search(template):
        return template

    errors: list[str] = []

    def repl(match: re.Match[str]) -> str:
        rel_path = match.group(1)
        include_path = includes_dir / rel_path
        if not include_path.exists():
            errors.append(str(include_path))
            return match.group(0)

        content = include_path.read_text(encoding="utf-8").rstrip("\n")
        if "\n" not in content:
            return content

        line_start = template.rfind("\n", 0, match.start()) + 1
        indent = " " * (match.start() - line_start)
        lines = content.splitlines()
        return lines[0] + "\n" + "\n".join(indent + line for line in lines[1:])

    rendered = INCLUDE_RE.sub(repl, template)
    if errors:
        raise SystemExit(
            "Include file(s) not found: " + ", ".join(sorted(set(errors)))
        )
    return rendered


def render_template(template: str, values: dict[str, str]) -> str:
    errors: list[str] = []

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            errors.append(key)
            return match.group(0)

        value = values[key]
        if "\n" not in value:
            return value

        line_start = template.rfind("\n", 0, match.start()) + 1
        indent = template[line_start : match.start()]
        lines = value.splitlines()
        if not lines:
            return ""
        return lines[0] + "\n" + "\n".join(indent + line for line in lines[1:])

    rendered = TOKEN_RE.sub(repl, template)
    if errors:
        missing = ", ".join(sorted(set(errors)))
        raise SystemExit(f"Missing placeholder values for keys: {missing}")
    return rendered


def main() -> int:
    args = parse_args()

    template_path = Path(args.template)
    i18n_dir = Path(args.i18n_dir)
    output_dir = Path(args.output_dir)
    version_file = Path(args.version_file)
    includes_dir = Path(args.includes_dir)

    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    if not i18n_dir.exists() or not i18n_dir.is_dir():
        raise SystemExit(f"i18n directory not found: {i18n_dir}")

    template = template_path.read_text(encoding="utf-8")

    # Resolve [[include:...]] directives before i18n processing
    if includes_dir.is_dir():
        template = resolve_includes(template, includes_dir)

    template_keys = set(TOKEN_RE.findall(template))
    if not template_keys:
        raise SystemExit("No placeholders found in template.")
    version = load_version(version_file)
    computed_values = {
        "blueprint.version": version,
        "blueprint.version.nodots": version.replace(".", ""),
    }
    required_i18n_keys = template_keys - set(computed_values)

    dictionaries: dict[str, dict[str, str]] = {}
    for path in sorted(i18n_dir.glob("*.json")):
        dictionaries[path.stem] = load_json(path)

    if not dictionaries:
        raise SystemExit("No i18n dictionaries found.")

    if args.default_lang not in dictionaries:
        raise SystemExit(
            f"Fallback language '{args.default_lang}' not found in {i18n_dir}."
        )

    default_dict = dictionaries[args.default_lang]
    missing_default = sorted(required_i18n_keys - set(default_dict))
    if missing_default:
        raise SystemExit(
            "Fallback dictionary is missing keys required by template: "
            + ", ".join(missing_default)
        )

    unknown_in_default = sorted(set(default_dict) - required_i18n_keys)
    if unknown_in_default:
        raise SystemExit(
            f"Fallback dictionary has unknown keys not used by template: {', '.join(unknown_in_default)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    for lang, local_dict in dictionaries.items():
        unknown_keys = sorted(set(local_dict) - required_i18n_keys)
        if unknown_keys:
            raise SystemExit(
                f"Dictionary '{lang}' has unknown keys not used by template: {', '.join(unknown_keys)}"
            )

        values = default_dict | local_dict
        version_line = build_version_line(values["blueprint.version.line"], version, lang)
        render_values = computed_values | values | {"blueprint.version.line": version_line}
        rendered = render_template(template, render_values)

        lang_out_dir = output_dir / lang
        lang_out_dir.mkdir(parents=True, exist_ok=True)
        (lang_out_dir / args.filename).write_text(rendered, encoding="utf-8")

    print(
        f"Rendered {len(dictionaries)} language(s) to '{output_dir}'. "
        f"Fallback language: '{args.default_lang}'. "
        f"Version: '{computed_values['blueprint.version']}'."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
