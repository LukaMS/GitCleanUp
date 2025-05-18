#!/usr/bin/env bash
set -e

# --- 1. Initialise a fresh sandbox repo ----------------------
rm -rf demo-repo
mkdir  demo-repo && cd demo-repo
git init -q
cp -r ../example/* .
git add .
git commit -qm "feat: initial commit with bad tracked files"

echo
echo "== BEFORE git_clean =="
git ls-files --cached

# --- 2. Run git_clean.py (dry-run then real) ----------------
python ../git_clean.py --dry-run
python ../git_clean.py --yes

echo
echo "== AFTER git_clean =="
git ls-files --cached
