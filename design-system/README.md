3VOtech builds Evolution, the field app technicians use to install and track work room by room: check in, finish tasks, take photos, sync. The brand is Volt: deep navy, an electric blue for anything you tap, ultraviolet for brand moments and cyan for anything live. The logo is fast on purpose, because time is money for installers.

## The name

- Write the company as **3VOtech**: a 3, capital V and O, lowercase tech. The 3 is a backward E, so 3VO reads EVO. The legal name is **3VOtech LLC**.
- Never write 3votech, 3VOTech or EVOtech in running text. The logo sets TECH in capitals; text does not.
- The app is **Evolution**. On a phone it is named "Evolution by 3VOtech".

## The logo

The mark is three letters joined into one shape. The Ǝ's spine is also the V's left stem, the V's long arm is a **check mark** crossing the O, and the Ǝ's bars are cut at the arm's angle, 54.6° from horizontal, so they read as speed lines. Every version separates the letters the same way: a thin gap around the V where it meets the bars and crosses the O. The check is the point: technicians check in and check off tasks.

| Use | File | Ground |
|---|---|---|
| Default, wherever there is width | `3votech-horizontal-color.svg` | white, `ground`, `cell` (light) |
| On dark | `3votech-horizontal-color-dark.svg` | navy: dark `ground`, dark `cell`, or `label` (#0D1530) |
| Square spaces: a sign-in screen, a slide title | `3votech-stacked-*.svg` | as above |
| App icon, avatar, favicon, anywhere under 120px wide | `3votech-mark-*.svg` | as above |
| Printing on paper in one ink: forms, receipts, stamps | `*-black.svg` | white or light paper |
| One ink on dark: shirts, hats, decals, photos | `*-white.svg` | dark grounds and photos |
| One ink in brand navy: embroidery, signage | `*-navy.svg` | light grounds |

- **Clear space:** keep empty space around the logo at least the height of one Ǝ bar (a fifth of the mark's height) on every side.
- **Minimum size:** the horizontal logo 120px wide on screen and 1in in print; the stacked logo 64px and 0.6in; the mark 24px and 0.25in. Smaller than that, use the mark alone.
- **TECH is artwork, not type.** Its T, E and C are cut at the same 54.6° as the mark. Never retype it in Saira, which has no cuts.
- **The dark color version is for navy only.** Its lighter colors are made for it. On a light ground use `3votech-*-color.svg`.
- Do not recolor the mark beyond its versions (color, color for dark, black, white, navy), add gradients, shadows or outlines, rotate it, stretch it, or place the color version on a photo. On a photo, use the one-color white version.
- Colors, for print and vendors: Ǝ `logo-e` (#2459F5), V `logo-v` (#7A3CF0), O `logo-o` (#0891B2), TECH `logo-ink` (#0D1530). On dark: #5C8DFF, #A685FF, #22D3EE and #EAF0FF.

## Color

Every color is a role, never a hex value. Code asks `useTheme()` for a token (`label`, `cell`, `tint`) and gets the value for the current scheme.

- **`tint`** (Volt Blue) is for anything you tap: buttons, selection, links. If it is not interactive, it is not tint.
- **`accent`** (Ultraviolet) is for brand moments only: the logo, progress. Never a control.
- **`spark`** (Spark Cyan) is for anything live: scanning, syncing, checked in. In light it is 3.4:1 on `ground`, so it carries icons and marks, not small text.
- **Dark mode is navy, never black.** Use `ground` and `cell`, never the system's black backgrounds.
- **The neutrals have names** for print and vendors: **Navy Ink** #0D1530 (`label` in light, TECH in the logo), **Midnight** #0A1230 (dark `ground`) and **Mist** #F3F5FB (light `ground`).
- **Text:** `label` for primary text, `label2` for secondary, `label3` for placeholders and disabled text only. `label3` is under 4.5:1 in both themes, so never put content someone must read in it.
- **Status colors come only from the `status-*` tokens** (room tiles) and `success`, `warning`, `danger` with their `*Soft` backgrounds (task chips). Never color a status any other way. Every status also carries its word ("Completed", "Issue") or an icon; color alone never says it.
- `onTint` stays white on dark `tint` at 3.1:1 to match how iOS draws a prominent button. It is fine for button labels, which are 17pt semibold, and too low for small text.

## Type

- **Brand type is Saira Expanded** (Saira at 125% width), set in capitals and tracked wide. It appears in the logo and in brand moments such as a slide title or a web heading. It never appears in the app's UI.
- **The app uses the system face**, SF Pro on iOS and Roboto on Android, through named styles: `largeTitle`, `title`, `title2`, `headline`, `body`, `subhead`, `footnote`, `caption`, `caption2`. One name maps to Apple's ramp on iOS (`ios-*`) and Material 3's on Android (`android-*`), so `body` reads as native on each.
- Never set a raw font size. Text scales with the phone's text size, so rows grow with padding or minHeight, never a fixed height.

## Layout

- Spacing steps are `space-xs` 4 through `space-xxl` 48. Use the nearest step; an odd value needs a comment saying why. `space-ms` (12) is row padding and `space-ml` (20) insets floating chrome from the screen edge.
- Radius is by role: `radius-control`, `radius-tile`, `radius-cell`, `radius-full`. The values here are iOS; Android draws them smaller (8, 16, 16). On iOS pair every radius except `radius-full` with `borderCurve: 'continuous'`.
- Tap targets are at least `min-touch`: 44pt on iOS, 48dp on Android.
- Native chrome first. iOS draws Liquid Glass and Android draws Material 3 on the system's bars, tab bars and sheets. Configure them; do not repaint them.

## Voice

Write for a technician mid-job, reading on a phone. Short sentences, plain words, active voice. Name things the way technicians do: rooms, tasks, Check In, Scan, issues. Say what changed for them, not how it was built.

> Big projects open faster. Rooms download in batches you can start working on right away, and a download that is cut off picks up where it stopped.

> If a photo cannot upload, the app tells you, instead of retrying in silence.

- Address the technician as "you". No emoji in the product.
- A button says exactly what happens ("Check In", "Clear Photo Queue"), and a destructive one asks first.
- A date a person sees is the Eastern date, with no time. A timestamp a machine compares stays UTC.
- Release notes are written for technicians. A bug found and fixed before release gets no line.

## Iconography

- Icons are SF Symbols on iOS and Material Symbols on Android, one name for both, through the app's `Icon` component (`checkIn`: `door.left.hand.open` / `door_open`).
- Never draw an icon from an emoji or a Unicode glyph (←, ✕, ⚙️). They render differently on every device and ignore the text-size settings.
- The logo mark is not an icon. Do not use it as a button or a status.
