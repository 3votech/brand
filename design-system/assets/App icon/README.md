The app icon for Evolution: the mark alone, 66% of the icon's width, centered on its ink.

- `app-icon-light.png` and `app-icon-dark.png`: 1024 × 1024 flat icons, white and navy (#0A1230) grounds. The light one is the default `icon.png` for Expo and Google Play.
- `app-icon-light.svg` and `app-icon-dark.svg`: the same icons as vector art.
- `icon-layer-o-ring.svg`, `icon-layer-e-bars.svg`, `icon-layer-v-check.svg`: the three letters on separate 1024 canvases, already in position, in their light colors. Import them into Icon Composer as three layers, O at the back and V at the front, so iOS 26 draws Liquid Glass depth and highlights on its own. Icon Composer makes the tinted and clear versions from these layers.
- `icon-layer-*-dark.svg`: the same three layers in the dark colors, made for navy. Set each as its layer's dark appearance, with a Midnight (#0A1230) fill, so the dark icon matches `app-icon-dark`.
- `android-foreground.png` and `android-monochrome.png`: Android's adaptive icon layers, on transparent 1024 canvases with a white ground set in the app. The mark is 44% of the canvas: the launcher shows only the middle two thirds, so that is 66% of what shows, as on iOS, and it stays inside the circle every launcher mask keeps. The monochrome layer is for themed icons (Android 13+), which use only its shape.
- `splash-light.png` and `splash-dark.png` (and their SVGs): Evolution's splash screen, the mark over EVOLUTION, on transparent, for white and for Midnight. EVOLUTION is cut Saira Expanded like TECH, as wide as the mark's ink, spaced like the stacked logo's TECH, in the logo's ink color.

Keep the icon flat. The system adds the glass; never bake a gradient or shadow into these files.
