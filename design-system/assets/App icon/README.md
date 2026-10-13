The app icon for Evolution: the mark alone, 66% of the icon's width, centered on its ink.

- `app-icon-light.png` and `app-icon-dark.png`: 1024 × 1024 flat icons, white and navy (#0A1230) grounds. The light one is the default `icon.png` for Expo and Google Play.
- `app-icon-light.svg` and `app-icon-dark.svg`: the same icons as vector art.
- `icon-layer-o-ring.svg`, `icon-layer-e-bars.svg`, `icon-layer-v-check.svg`: the three letters on separate 1024 canvases, already in position, in their light colors. Import them into Icon Composer as three layers, O at the back and V at the front, so iOS 26 draws Liquid Glass depth and highlights on its own. Icon Composer makes the dark and tinted versions from these layers.

Keep the icon flat. The system adds the glass; never bake a gradient or shadow into these files.
