#!/usr/bin/env python3
"""
Usage
-----
```bash
# Preview what would happen
python git_clean.py --dry-run

# Actually un‑track the files (keeps them on disk)
python git_clean.py

# Non‑interactive
python git_clean.py --yes
```

Install requirements:
```
pip install rich click pathspec
```
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from typing import List

import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

console = Console()

# ─── Git Helpers ──────────────────────────────────────────────────────────────

def git_root() -> Path:
    """Return Path to repository root or exit."""
    try:
        root = subprocess.check_output([
            "git", "rev-parse", "--show-toplevel"], text=True).strip()
        return Path(root)
    except subprocess.CalledProcessError:
        console.print("[red]Error:[/red] Not a git repository.")
        sys.exit(1)


def git_tracked_files() -> List[Path]:
    out = subprocess.check_output(["git", "ls-files", "--cached"], text=True)
    return [Path(p) for p in out.splitlines() if p]


def git_rm_cached(paths: List[Path]):
    if not paths:
        return
    subprocess.run(["git", "rm", "--cached", "--"] + [str(p) for p in paths])

# ─── Ignore Pattern Loader ────────────────────────────────────────────────────

def load_gitignore(root: Path) -> PathSpec:
    ignore_file = root / ".gitignore"
    patterns: List[str] = []
    if ignore_file.exists():
        patterns.extend(ignore_file.read_text().splitlines())

    # Also respect .git/info/exclude if present
    exclude = root / ".git" / "info" / "exclude"
    if exclude.exists():
        patterns.extend(exclude.read_text().splitlines())

    # Filter empty/comment lines
    patterns = [p for p in patterns if p and not p.lstrip().startswith("#")]

    return PathSpec.from_lines(GitWildMatchPattern, patterns)

# ─── CLI ──────────────────────────────────────────────────────────────────────

@click.command(help="Remove already‑tracked files that match .gitignore patterns.")
@click.option("--dry-run", is_flag=True, help="Show what would be removed without doing it.")
@click.option("--yes", "confirm", is_flag=True, help="Skip confirmation prompt (non‑interactive).")
def main(dry_run: bool, confirm: bool):
    root = git_root()
    console.print(f"[bold green]Git‑Clean[/bold green] at [cyan]{root}[/cyan]\n")

    spec = load_gitignore(root)
    tracked = git_tracked_files()

    matches = [p for p in tracked if spec.match_file(str(p))]

    if not matches:
        console.print("🎉 Nothing to clean — no tracked files match .gitignore.")
        return

    table = Table(title="Files to un‑track", show_lines=True)
    table.add_column("#", justify="right")
    table.add_column("Path", overflow="fold")
    for i, path in enumerate(matches, 1):
        table.add_row(str(i), str(path))
    console.print(table)
    console.print(f"[yellow]{len(matches)}[/yellow] tracked file(s) match .gitignore.")

    if dry_run:
        console.print("\n[green]Dry‑run:[/green] no changes made.")
        return

    if not confirm:
        proceed = Confirm.ask("Proceed with [red]git rm --cached[/red] on these files?", default=False)
        if not proceed:
            console.print("Aborted.")
            return

    git_rm_cached(matches)
    console.print("[green]Done.[/green] The files remain on disk but are no longer in the index.\n")
    console.print("Remember to commit the changes: [bold]git commit -m 'chore: clean ignored files'[/bold]")


if __name__ == "__main__":
    main()
