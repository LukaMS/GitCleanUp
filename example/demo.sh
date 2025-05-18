#!/usr/bin/env bash
set -e

# --- 1. Initialise a fresh sandbox repo ----------------------
rm -rf demo-repo
mkdir  demo-repo && cd demo-repo
git init -q
cp -r ../app.log ../build ../src .
git add .
git commit -qm "feat: initial commit with bad tracked files"

# --- 3. Now (too late!) we add the .gitignore --------------------------------
cp -r ../.gitignore .
git add .gitignore
git commit -qm "chore: add .gitignore"

echo
echo "== BEFORE git_clean =="
git ls-files --cached

# --- 2. Run git_clean.py (dry-run then real) ----------------
python ../../git_clean.py --dry-run
python ../../git_clean.py --yes

echo
echo "== AFTER git_clean =="
git ls-files --cached
