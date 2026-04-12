#!/bin/bash
# fix_links.sh
# Run AFTER reorganize_repo.sh
# Updates all href/src references across every HTML file to match new structure

set -e

echo "🔗 Fixing internal links in pages/*.html ..."

HTML_FILES=$(find pages -name "*.html")

for file in $HTML_FILES; do
  echo "  Processing $file..."

  # Fix links to other pages (href="hub.html" → href="hub.html" — they're in same folder, OK)
  # Fix image srcs that now need to go up one level: diana.png → ../assets/diana.png
  sed -i \
    -e 's|src="diana\.png"|src="../assets/diana.png"|g' \
    -e 's|src="marco\.png"|src="../assets/marco.png"|g' \
    -e 's|src="ron\.png"|src="../assets/ron.png"|g' \
    "$file"

  # Fix absolute GitHub Pages links if they reference root-level HTML
  # (only needed if you had hardcoded full URLs pointing to root)
  sed -i \
    -e 's|automated-stalker/hub\.html|automated-stalker/pages/hub.html|g' \
    -e 's|automated-stalker/index\.html|automated-stalker/pages/index.html|g' \
    -e 's|automated-stalker/competitors28\.html|automated-stalker/pages/competitors28.html|g' \
    -e 's|automated-stalker/funnelipc\.html|automated-stalker/pages/funnelipc.html|g' \
    -e 's|automated-stalker/algorithm_sop\.html|automated-stalker/pages/algorithm_sop.html|g' \
    -e 's|automated-stalker/iteration1\.html|automated-stalker/pages/iteration1.html|g' \
    -e 's|automated-stalker/iteration2\.html|automated-stalker/pages/iteration2.html|g' \
    -e 's|automated-stalker/iteration3\.html|automated-stalker/pages/iteration3.html|g' \
    "$file"
done

echo ""
echo "✅ Links updated. Review changes with:"
echo "   git diff pages/"
echo ""
echo "Then commit:"
echo "   git add pages/ && git commit -m 'fix: update internal links after folder restructure'"
