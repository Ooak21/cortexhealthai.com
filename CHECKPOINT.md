# Checkpoint — 2026-07-27 landing page rebuild

State of `cortexhealthai.com` at commit `910d653`. Live on GitHub Pages.

## The one thing to know first

**`index.html` is generated. Do not edit it.**

```bash
python3 build.py     # index.src.html + build.py -> index.html
```

- `index.src.html` — source of truth, the original page structure and copy
- `build.py` — every transform applied on top of it
- `assets/platform-icons.json` — converted icon set the build reads

Editing `index.html` directly works until the next build, then it is silently
overwritten.

## What changed in this pass

**Hero rebuilt from the CORTEX creative rather than embedding it flat.**
Headline, subline, benefit row, tagline and all curves are live text or SVG.
Only the clinician stays raster — a transparent cutout lifted with macOS
Vision (`VNGenerateForegroundInstanceMaskRequest`).

**Light + dark themes** with a nav toggle. Persisted to `localStorage`,
seeded from `prefers-color-scheme` by an inline script in `<head>` that runs
before first paint — without it, dark-preference visitors get a white flash.

**Icon sets** on the platform modules and the new-patient path, from the
`100-search-engine-optimization-icons-line` pack. The `01..06` numerals are
gone: six parallel capabilities were never a sequence. `T0..T4` are gone too,
though that section genuinely is one. `A/B/C` in the thesis cards remain,
because integrate → bypass → replace really is ordered.

**Imagery added:** platform overview (vendor chips removed, the image says it
better), Vitality provider view, in-system help panel, CTA card figure, and
the decorative orbs.

**Compliance cards** now run on the deep navy sampled from the creative.

**Vendor marks** use real per-theme artwork instead of a CSS `invert()`.
Grok was dropped — it is xAI's model, so listing both was like listing
Anthropic and Claude separately.

**Copy:** the named physician is out of the body copy. Still present in
`AGENTS.md` and `README.md`.

## Bugs fixed that were live

- **Horizontal scroll on every viewport under ~700px.** The patient-path grid
  set `grid-template-columns: repeat(5, 1fr)` via an *inline style*, which
  outranks media queries, so it stayed 5-up on phones and pushed the page
  ~250px wider than the viewport.
- **Nav CTA label went dark on blue** in light theme. `.nav-links a` (0,1,1)
  outranks `.nav-cta` (0,1,0), so the link colour captured the button.
- **Clipped `g` descender** in the hero headline. `background-clip: text` only
  paints inside the box and `line-height: 0.98` made the box shorter than the
  glyphs.
- **Hairline seam** where the hero curve met the deployments band — the SVG's
  `clamp()` height landed on a fractional pixel.

## Palette

Sampled from the source creative, not chosen:

| token | hex | where it came from |
|---|---|---|
| `--azure` | `#0048cc` | "One Login" glyphs, dominant swoosh |
| `--violet` | `#483cb4` | gradient terminus, lower right |
| `--abyss` | `#000c30` | deep curve along the bottom edge |
| `--paper` | `#fdfdfd` | the white field behind the logo |

## Open items

1. **The theme is an override layer**, not a rebuilt stylesheet — ~250 lines
   of rules stacked on the original dark CSS. Both specificity bugs above came
   from that. Rebuilding it properly is the next structural job.
2. **Hero clinician is 882px rendering at 700** — sharp at 1x, soft on retina.
   Needs a larger source render; the export script takes any transparent PNG.
3. **Anthropic's mark is a wordmark** that spells ANTHROPIC, sitting beside a
   label that also says ANTHROPIC. xAI's glyph needs its label; this one does
   not.
4. `AGENTS.md` and `README.md` still name the physician and still describe the
   site as having no build step.

## Cleared

- Licensing: Envato Elements covers the photography, orb, and icon packs.
- The Vitality provider screenshot is Luis's own test profile, not a patient.
