#!/bin/bash
# fix_competitors28_responsive.sh
# Injects responsive CSS into competitors28.html
# Run from the root of the repo (or pages/ if already reorganized)

set -e

TARGET="competitors28.html"
[ -f "pages/$TARGET" ] && TARGET="pages/$TARGET"
[ -f "$TARGET" ] || { echo "❌ $TARGET not found. Run from repo root."; exit 1; }

echo "💉 Patching $TARGET with responsive styles..."

# ── The responsive CSS block to inject ───────────────────────────
PATCH='<style>
/* ── RESPONSIVE PATCH ── competitors28 ─────────────────────── */

/* Root box model reset */
*, *::before, *::after { box-sizing: border-box; }

html, body {
  max-width: 100vw;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

/* Main container: constrain width */
body > *,
main,
.container,
.report-container,
.intelligence-container,
section,
article {
  max-width: 100%;
}

/* Tables: scroll horizontally on small screens */
table {
  width: 100%;
  border-collapse: collapse;
  display: block;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  white-space: nowrap;
}

/* Restore normal table layout on wide screens */
@media (min-width: 900px) {
  table {
    display: table;
    white-space: normal;
  }
}

/* Cards grid: responsive columns */
.cards-grid,
.competitor-grid,
.candidates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 0 1rem;
}

/* Individual cards */
.card,
.competitor-card,
.candidate-card {
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

/* Nav: wrap on mobile */
nav,
.nav,
.navbar {
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* Stat counters row */
.stats-row,
.counters,
.metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

/* Filter buttons row */
.filters,
.filter-row,
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/* Long URLs / links inside table cells don't overflow */
td a {
  word-break: break-all;
}

/* Headings scale down on mobile */
@media (max-width: 600px) {
  h1 { font-size: clamp(1.4rem, 5vw, 2.5rem); }
  h2 { font-size: clamp(1.1rem, 4vw, 1.8rem); }
  h3 { font-size: clamp(1rem, 3.5vw, 1.4rem); }

  .stats-row .stat,
  .counter {
    min-width: 120px;
    text-align: center;
  }
}
/* ── END RESPONSIVE PATCH ─────────────────────────────────────── */
</style>'

# Inject before </head>
if grep -q '</head>' "$TARGET"; then
  # Use python for safe multi-line replacement
  python3 - <<PYEOF
import re

with open("$TARGET", "r", encoding="utf-8") as f:
    html = f.read()

patch = '''$PATCH'''

# Avoid double-injection
if "RESPONSIVE PATCH" in html:
    print("⚠️  Patch already present in $TARGET, skipping.")
else:
    html = html.replace("</head>", patch + "\n</head>", 1)
    with open("$TARGET", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Responsive patch injected into $TARGET")
PYEOF
else
  echo "❌ No </head> tag found in $TARGET. Check the file manually."
  exit 1
fi

echo ""
echo "Preview locally with:"
echo "  open $TARGET   # macOS"
echo "  xdg-open $TARGET  # Linux"
echo ""
echo "Commit with:"
echo "  git add $TARGET && git commit -m 'fix: make competitors28 responsive (overflow, grid, table scroll)'"
