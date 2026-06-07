from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Sequence


TEMPLATE_DIR = Path(__file__).resolve().parent / "template"
PLACEHOLDERS = ("{{PROJECT_NAME}}", "{{Project_Name}}")


class ScaffoldError(Exception):
    """Raised when a new project cannot be scaffolded."""


def render_template_text(text: str, project_name: str) -> str:
    for placeholder in PLACEHOLDERS:
        text = text.replace(placeholder, project_name)
    return text


def copy_template(
    template_dir: Path,
    destination_dir: Path,
    project_name: str,
    allow_existing_destination: bool = False,
) -> None:
    if not template_dir.is_dir():
        raise ScaffoldError(f"template folder not found: {template_dir}")

    if destination_dir.exists():
        if not allow_existing_destination or not destination_dir.is_dir():
            raise ScaffoldError(f"destination already exists: {destination_dir}")
    else:
        destination_dir.mkdir(parents=True)

    for source_path in template_dir.rglob("*"):
        relative_path = source_path.relative_to(template_dir)
        destination_path = destination_dir / relative_path

        if source_path.is_dir():
            if destination_path.exists() and not destination_path.is_dir():
                raise ScaffoldError(f"destination already exists: {destination_path}")
            destination_path.mkdir(exist_ok=True)
            continue

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if destination_path.exists():
            raise ScaffoldError(f"destination already exists: {destination_path}")

        source_bytes = source_path.read_bytes()

        try:
            rendered_text = render_template_text(
                source_bytes.decode("utf-8"), project_name
            )
        except UnicodeDecodeError:
            shutil.copy2(source_path, destination_path)
        else:
            destination_path.write_bytes(rendered_text.encode("utf-8"))


def resolve_scaffold_target(
    project_name_argument: str, base_dir: Path | None = None
) -> tuple[Path, str, bool]:
    project_path_text = project_name_argument.strip()
    if not project_path_text:
        raise ScaffoldError("project name cannot be empty")

    current_dir = base_dir or Path.cwd()
    if project_path_text == ".":
        destination_dir = current_dir
        allow_existing_destination = True
    else:
        project_path = Path(project_path_text)
        destination_dir = project_path if project_path.is_absolute() else current_dir / project_path
        allow_existing_destination = False

    project_name = destination_dir.name
    if not project_name:
        raise ScaffoldError("project name cannot be empty")

    return destination_dir, project_name, allow_existing_destination


def scaffold_project(project_name: str, base_dir: Path | None = None) -> Path:
    destination_dir, resolved_project_name, allow_existing_destination = (
        resolve_scaffold_target(project_name, base_dir)
    )
    copy_template(
        TEMPLATE_DIR,
        destination_dir,
        resolved_project_name,
        allow_existing_destination=allow_existing_destination,
    )
    return destination_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python-ai-new",
        description="Scaffold a new Python AI repo from the bundled template.",
    )
    parser.add_argument("project_name", help="Name of the project folder to create.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        destination_dir = scaffold_project(args.project_name)
    except ScaffoldError as exc:
        parser.exit(1, f"error: {exc}\n")

    print(f"Created {destination_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
