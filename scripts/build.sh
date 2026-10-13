#!/usr/bin/env bash
# Rebuild every logo, app icon and the guidelines page from source.
# Needs: uv (for fontTools), curl, and Google Chrome (for the app icon PNGs).
set -euo pipefail
cd "$(dirname "$0")/.."

# Saira is OFL-licensed and lives in google/fonts; fetch it instead of committing it.
if [ ! -f fonts/Saira.ttf ]; then
  mkdir -p fonts
  curl -sSLo fonts/Saira.ttf "https://github.com/google/fonts/raw/main/ofl/saira/Saira%5Bwdth,wght%5D.ttf"
fi

uv run -q --with fonttools python scripts/wordmarks.py
python3 scripts/logos.py . build/wordmarks.defs.svg
python3 scripts/guidelines.py logos guidelines/template.html guidelines/brand-guidelines.html

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for v in light dark; do
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1024,1024 --screenshot="$PWD/app-icon/app-icon-$v.png" "file://$PWD/app-icon/app-icon-$v.svg" 2>/dev/null
done
echo "Built logos/, app-icon/ and guidelines/brand-guidelines.html"
