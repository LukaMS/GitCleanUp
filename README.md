# Git-Clean 🧹  
Retroactively remove files that **should be ignored** but are already tracked in Git.

---

## Why?

1. `git init`, happily add everything  
2. *Then* remember you needed a `.gitignore`  
3. Realise `build/`, `*.log`, or secrets are forever in the index

`git rm --cached …` fixes it, but discovering every file the **new** `.gitignore` matches is a chore. **Git-Clean** automates the busy-work.

---

## Features

|   |   |
|---|---|
| 📝 | Reads patterns from `.gitignore` **and** `.git/info/exclude` |
| 🔍 | Lists **tracked** files that match those rules |
| 🗑️ | Runs `git rm --cached` so files stay on disk but vanish from the repo |
| 🧪 | **Dry-run** preview, interactive prompt, or `--yes` |
| 🎨 | Colourful output via **Rich** |
| 🪶 | Pure-Python, lightweight deps (`rich`, `click`, `pathspec`) |

---

## Quick start

```bash
# one-time setup
python -m venv .venv && source .venv/bin/activate
pip install rich click pathspec

# preview what would be removed
python git_clean.py --dry-run

# actually un-track the files
python git_clean.py        # interactive
python git_clean.py --yes  # non-interactive

# then commit the index changes
git commit -m \"chore: clean ignored files\"
