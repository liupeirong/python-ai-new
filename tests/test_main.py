import pytest

import main


def test_scaffold_project_copies_template_and_replaces_placeholders(
    tmp_path, monkeypatch
):
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("# {{PROJECT_NAME}}\n", encoding="utf-8")
    (template_dir / "legacy.md").write_text("# {{Project_Name}}\n", encoding="utf-8")
    (template_dir / "data.bin").write_bytes(b"\xff\xfe")
    monkeypatch.setattr(main, "TEMPLATE_DIR", template_dir)

    destination_dir = main.scaffold_project("demo-project", base_dir=tmp_path)

    assert destination_dir == tmp_path / "demo-project"
    assert (destination_dir / "README.md").read_text(
        encoding="utf-8"
    ) == "# demo-project\n"
    assert (destination_dir / "legacy.md").read_text(
        encoding="utf-8"
    ) == "# demo-project\n"
    assert (destination_dir / "data.bin").read_bytes() == b"\xff\xfe"


def test_scaffold_project_fails_when_destination_exists(tmp_path, monkeypatch):
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    monkeypatch.setattr(main, "TEMPLATE_DIR", template_dir)
    (tmp_path / "existing-project").mkdir()

    with pytest.raises(main.ScaffoldError, match="destination already exists"):
        main.scaffold_project("existing-project", base_dir=tmp_path)


def test_scaffold_project_uses_last_path_segment_as_project_name(
    tmp_path, monkeypatch
):
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("# {{PROJECT_NAME}}\n", encoding="utf-8")
    monkeypatch.setattr(main, "TEMPLATE_DIR", template_dir)

    destination_dir = main.scaffold_project("parent/demo-project", base_dir=tmp_path)

    assert destination_dir == tmp_path / "parent" / "demo-project"
    assert (destination_dir / "README.md").read_text(
        encoding="utf-8"
    ) == "# demo-project\n"


def test_scaffold_project_dot_scaffolds_current_directory(tmp_path, monkeypatch):
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("# {{PROJECT_NAME}}\n", encoding="utf-8")
    monkeypatch.setattr(main, "TEMPLATE_DIR", template_dir)
    destination_dir = tmp_path / "demo-project"
    destination_dir.mkdir()

    assert main.scaffold_project(".", base_dir=destination_dir) == destination_dir
    assert (destination_dir / "README.md").read_text(
        encoding="utf-8"
    ) == "# demo-project\n"


def test_main_returns_success(tmp_path, monkeypatch, capsys):
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("# {{PROJECT_NAME}}\n", encoding="utf-8")
    monkeypatch.setattr(main, "TEMPLATE_DIR", template_dir)
    monkeypatch.chdir(tmp_path)

    assert main.main(["demo-project"]) == 0
    assert (tmp_path / "demo-project" / "README.md").read_text(
        encoding="utf-8"
    ) == "# demo-project\n"
    assert "Created" in capsys.readouterr().out
