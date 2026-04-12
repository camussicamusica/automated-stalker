#!/bin/bash
# reorganize_repo.sh
# Run from the root of automated-stalker repo
# Moves all loose files into clean folder structure

set -e

echo "🗂️  Reorganizing automated-stalker repo..."

# ── 1. PAGES folder ──────────────────────────────────────────────
mkdir -p pages
for f in hub.html index.html competitors28.html funnelipc.html algorithm_sop.html \
          iteration1.html iteration2.html iteration3.html; do
  [ -f "$f" ] && git mv "$f" "pages/$f" && echo "  ✓ moved $f → pages/"
done

# ── 2. ASSETS folder ─────────────────────────────────────────────
mkdir -p assets
for f in diana.png marco.png ron.png; do
  [ -f "$f" ] && git mv "$f" "assets/$f" && echo "  ✓ moved $f → assets/"
done

# ── 3. BRAIN / DATA folder ───────────────────────────────────────
mkdir -p brain
for f in nuno_brain.txt nuno_brain_preview.txt; do
  [ -f "$f" ] && git mv "$f" "brain/$f" && echo "  ✓ moved $f → brain/"
done

echo ""
echo "📁 Final structure:"
echo "  automated-stalker/"
echo "  ├── 01_Scripts/       (already clean)"
echo "  ├── 02_Data/          (already clean)"
echo "  ├── 03_Reports/       (already clean)"
echo "  ├── 04_Archive/       (already clean)"
echo "  ├── report_cards/     (already clean)"
echo "  ├── pages/            ← all .html files"
echo "  ├── assets/           ← all images (.png, etc.)"
echo "  ├── brain/            ← nuno_brain*.txt files"
echo "  ├── .gitignore"
echo "  └── README.md"
echo ""
echo "⚠️  IMPORTANT: After moving pages/, update all internal links."
echo "   Run fix_links.sh next (see companion script)."
echo ""
echo "✅ Done. Commit with:"
echo "   git commit -m 'chore: reorganize root files into pages/, assets/, brain/'"
