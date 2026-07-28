#!/usr/bin/env python3
"""Build index.html from index.src.html.

index.src.html is the source of truth - edit THAT, never index.html, which is
generated and overwritten by this script.

    python3 build.py

Transforms applied: light/dark themed hero rebuilt from the CORTEX creative
(headline, benefit row, tagline and curves become live text/SVG, only the
clinician stays raster), icon sets on the platform + patient-path cards,
supporting imagery, and the theme toggle.
"""
import json, pathlib

REPO = pathlib.Path('/Users/luisocadiz/cortexhealthai.com')
src = (REPO / 'index.src.html').read_text(encoding='utf-8')

CSS = """
<style id="cortex-theme">
/* ============================================================
   PREVIEW - light theme keyed to the CORTEX Health creative.
   Palette sampled from the source art:
     azure  #0048cc   "One Login" glyphs + dominant swoosh
     violet #483cb4   gradient terminus, lower right
     abyss  #000c30   deep curve along the bottom edge
     paper  #fdfdfd   the white field behind the logo
   ============================================================ */
:root {
  --paper:#fdfdfd; --mist:#e8edf9; --azure:#0048cc; --violet:#483cb4;
  --abyss:#000c30; --ink:#0a1020;
  --bg:var(--paper); --surface:#f6f8fd; --surface-2:#eef2fa; --surface-3:#e6ecf7;
  --border:#d7dded; --border-soft:rgba(10,16,40,0.10); --border-strong:rgba(10,16,40,0.18);
  --text:var(--ink); --muted:#55607a; --dim:#8891a8;
  --accent:var(--azure); --accent-hot:#1f63e0; --accent-deep:#00329a;
  --glow:rgba(0,72,204,0.22); --glow-soft:rgba(0,72,204,0.07);
}
body { background:var(--paper); color:var(--ink); }
::selection { background:rgba(0,72,204,0.20); color:var(--ink); }
::-webkit-scrollbar-thumb { background:rgba(0,72,204,0.35); }

/* ---------- nav ---------- */
.nav.on { background:rgba(253,253,253,0.88); border-bottom:1px solid rgba(10,16,40,0.07); }
.nav-links a { color:rgba(10,16,32,0.62); }
.nav-links a:hover { color:var(--ink); }
/* .nav-links a (0,1,1) outranks .nav-cta (0,1,0), so the button needs to be
   matched at equal-or-higher specificity or its label goes dark on blue */
.nav-links a.nav-cta, .nav-links a.nav-cta:hover { color:#fff; }
.nav-toggle { border-color:var(--border-soft); }
.nav-toggle span { background:var(--ink); }
.nav.open .nav-links { background:rgba(253,253,253,0.97); border-bottom-color:var(--border-soft); }
.brand-mark { filter:none; }
.nav-cta { background:linear-gradient(135deg,#1f63e0,var(--azure) 55%,#00329a); }

/* ---------- hero shell ---------- */
.hero {
  position:relative; min-height:0; display:block;
  padding:calc(var(--nav-h) + 18px) 0 0;
  background:radial-gradient(80% 60% at 3% 24%, var(--mist), transparent 56%), var(--paper);
  overflow:hidden;
}
.hero-inner {
  position:relative; z-index:2;
  display:grid;
  grid-template-columns:minmax(0,1.02fr) minmax(0,0.98fr);
  align-items:end;
  gap:clamp(20px,3vw,48px);
  padding-bottom:0;
}
.hero-copy { padding-bottom:clamp(28px,4vw,64px); }

/* ---------- type: matched to the grotesque baked into the art ---------- */
.hero h1 {
  font-size:clamp(2.5rem,5.4vw,4.4rem);
  font-weight:800;
  letter-spacing:-0.048em;
  line-height:0.98;
  margin-bottom:14px;
  max-width:12ch;
}
/* background-clip:text only paints inside the box, and line-height 0.98 makes
   the box shorter than the glyphs - without this the "g" descender is clipped.
   The negative margin cancels the padding so layout is unchanged. */
.hero h1 .grad { display:block; padding-bottom:0.16em; margin-bottom:-0.16em; }
.hero h1 .grad {
  background:linear-gradient(104deg,var(--azure) 4%,#2f39b8 54%,var(--violet) 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.hero-lede {
  font-size:clamp(1.25rem,2.1vw,1.75rem);
  font-weight:700;
  letter-spacing:-0.03em;
  line-height:1.15;
  margin-bottom:18px;
  max-width:16ch;
}
.hero-lede b { color:var(--azure); font-weight:800; }
.hero-sub { color:var(--muted); font-size:1rem; max-width:46ch; margin-bottom:26px; }
.hero-sub strong { color:var(--ink); font-weight:600; }
.hero-badge { border-color:rgba(0,72,204,0.28); background:rgba(0,72,204,0.06); color:var(--azure); }
.trust-pill { background:rgba(255,255,255,0.85); border-color:var(--border-soft); color:var(--muted); }
.btn-ghost { color:var(--ink); border-color:var(--border-strong); }
.btn-ghost:hover { border-color:rgba(0,72,204,0.45); background:var(--glow-soft); }

/* ---------- the clinician, lifted out of the creative ---------- */
.hero-figure { position:relative; display:flex; justify-content:center; align-items:flex-end; }
/* height-bound, not width-bound, so she seats on the benefit rule */
.hero-figure img {
  height:clamp(430px,52vw,700px); width:auto; max-width:100%; display:block;
  filter:drop-shadow(0 26px 54px rgba(10,20,60,0.14));
  /* nudged left, out of the far-right corner and closer to the copy */
  transform:translateX(calc(-1 * clamp(26px,8.5vw,128px)));
}

/* ---------- benefit row, rebuilt as text + inline SVG ---------- */
.benefits {
  position:relative; z-index:2;
  display:grid; grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--border-soft);
}
.benefit {
  position:relative;
  display:flex; flex-direction:column; align-items:center; text-align:center;
  gap:9px; padding:24px 14px 18px;
}
.benefit + .benefit::before {
  content:''; position:absolute; left:0; top:24px; bottom:18px;
  width:1px; background:var(--border-soft);
}
.benefit svg { width:29px; height:29px; color:var(--azure); }
.benefit .t {
  font-size:0.76rem; font-weight:700; letter-spacing:0.13em;
  text-transform:uppercase; color:var(--ink);
}
.benefit .s {
  font-size:0.7rem; letter-spacing:0.11em; text-transform:uppercase; color:var(--muted);
}
.tagline {
  position:relative; z-index:2; text-align:center;
  font-family:var(--mono); font-size:0.68rem; letter-spacing:0.24em;
  text-transform:uppercase; color:var(--muted);
  padding:4px 0 26px;
}
.tagline b { color:var(--azure); font-weight:500; }

/* ---------- the blend into the next section ---------- */
/* -1px kills the hairline seam where the SVG's fractional height rounds
   against the next section's background */
.blend { position:relative; line-height:0; z-index:1; margin-bottom:-1px; }
.blend svg { display:block; width:100%; height:clamp(80px,10vw,172px); }

#deployments {
  background:linear-gradient(180deg,var(--abyss),#04154a 55%,#071c58);
  padding-top:clamp(12px,2vw,28px) !important;
  padding-bottom:0; position:relative;
}
#deployments .section-head h2 { color:#fff; }
#deployments .section-head p { color:rgba(255,255,255,0.68); }
#deployments .eyebrow { color:#8fb4ff; }
#deployments .eyebrow .dot { background:#8fb4ff; box-shadow:0 0 10px #4f86ff; }
#deployments .deploy { background:rgba(255,255,255,0.055); border-color:rgba(255,255,255,0.13); }
#deployments .deploy:hover { background:rgba(255,255,255,0.09); border-color:rgba(143,180,255,0.4); }
#deployments .deploy h3 { color:#fff; }
#deployments .deploy p { color:rgba(255,255,255,0.64); }
#deployments .deploy-tag { color:#8fb4ff; }

/* ---------- remaining surfaces ---------- */
.module,.price,.comply-card,.deploy,.faq-item,.billing-toggle { background:#fff; border-color:var(--border-soft); }
.module { background:linear-gradient(180deg,#ffffff,#f7f9fe); }
.module:hover { border-color:rgba(0,72,204,0.3); box-shadow:0 20px 46px -24px rgba(6,16,60,0.26),0 0 34px -18px var(--glow); }
.deploy:hover { background:var(--surface); }
/* compliance cards run on the deep navy from the creative - must come after
   the shared white-surface rule above, which also matches .comply-card */
.comply-card {
  background:linear-gradient(158deg,#08215f,var(--abyss));
  border-color:rgba(255,255,255,0.10);
  box-shadow:0 20px 44px -26px rgba(6,16,60,0.55);
}
.comply-card h3 { color:#fff; }
.comply-card p { color:rgba(255,255,255,0.72); }
.chip { background:rgba(10,16,40,0.02); border-color:rgba(10,16,40,0.14); }
/* platform modules and the new-patient path carry icons, not 01..06 / T0..T4 */
#platform .module-ico, .flow-5 .module-ico { width:44px; height:44px; border-radius:12px; }
#platform .module-ico svg, .flow-5 .module-ico svg { width:22px; height:22px; display:block; }
/* with the chips gone the right column can carry a wider visual */
#problem .split { grid-template-columns:minmax(0,1fr) minmax(0,1.18fr); align-items:center; }
.stack-visual {
  margin-top:clamp(20px,3vw,30px);
  border-radius:14px;
  overflow:hidden;
  border:1px solid var(--border-soft);
  box-shadow:0 18px 44px -26px rgba(6,16,60,0.4);
  line-height:0;
}
.stack-visual img { width:100%; height:auto; display:block; }
/* .stack-visual sets line-height:0 to kill inline gaps under the image, so
   every caption has to restore it or the text collapses and clips */
.stack-visual figcaption {
  line-height:1.5;
  padding:10px 14px;
  font-family:var(--mono);
  font-size:0.64rem;
  letter-spacing:0.08em;
  text-transform:uppercase;
  color:var(--dim);
  background:var(--surface);
  border-top:1px solid var(--border-soft);
}
#thesis .split { align-items:start; }
/* cards stay full width; the panel hangs BELOW them, out of flow, so it fills
   the dead space between this section and the next without adding any height */
.thesis-modules { grid-template-columns:1fr; gap:12px; position:relative; }
.thesis-modules .help-visual {
  position:absolute;
  top:100%; left:50%;
  transform:translateX(-50%);
  margin:clamp(18px,2.4vw,30px) 0 0;
  width:clamp(200px,23vw,268px);
  z-index:2;
}
@media (max-width:980px) {
  /* stacked, there is no dead space to borrow - put it back in flow */
  .thesis-modules .help-visual {
    position:static; transform:none; width:100%; max-width:370px;
    margin-top:clamp(16px,3vw,24px);
  }
}
.vert { background:rgba(10,16,40,0.02); }
.vert:hover,.vert.active { color:var(--ink); border-color:rgba(0,72,204,0.4); }
.price.featured {
  background:linear-gradient(180deg,rgba(0,72,204,0.08),#ffffff);
  border-color:rgba(0,72,204,0.4); box-shadow:0 24px 58px -26px rgba(0,72,204,0.35);
}
.billing-toggle button.on { background:rgba(0,72,204,0.11); color:var(--ink); box-shadow:inset 0 0 0 1px rgba(0,72,204,0.32); }
.cta-band {
  background:radial-gradient(ellipse 80% 80% at 82% 16%,rgba(0,72,204,0.15),transparent 52%),
             linear-gradient(158deg,#f4f7fd,#e9eff9);
  box-shadow:0 30px 78px -36px rgba(6,16,60,0.3);
  /* two columns; the figure stands in the empty right half and is cropped by
     the card's own rounded edge, so it needs the padding removed on its side */
  display:grid;
  grid-template-columns:minmax(0,1.04fr) minmax(0,0.96fr);
  align-items:end;
  gap:clamp(12px,2.5vw,36px);
  padding-bottom:0;
}
.cta-copy { padding-bottom:clamp(40px,6vw,64px); }
/* orb sits in the top-left corner and runs off the card; .cta-band already
   has position:relative + overflow:hidden, so the rounded edge crops it */
.cta-orb { position:absolute; z-index:0; pointer-events:none; display:block; }
.cta-orb img { width:100%; height:auto; display:block; }
/* three sizes so the scatter reads as depth rather than repetition. each one
   is cropped by an edge of the card, which is what keeps them from looking
   like stickers dropped on top. */
/* full opacity on every one - fading the small ones read as washed out,
   not distant. scale alone carries the depth. */
.orb-a { top:-104px; left:-86px;  width:clamp(150px,14vw,200px); }
.orb-b { bottom:-72px; left:36%;  width:clamp(84px,9vw,122px); }
.orb-c { top:46px; left:45%;      width:clamp(46px,5vw,70px); }
/* clear of her silhouette, cropped by the card edge instead - overlapping
   her put the orb against the cutout's edge and exposed it */
.orb-d { top:25%; right:-72px;    width:clamp(112px,13vw,178px); }
.orb-e { bottom:25%; right:43%;   width:clamp(38px,4.4vw,62px); }
@media (max-width:860px) {
  .orb-b { left:auto; right:-30px; bottom:auto; top:38%; }
  .orb-c, .orb-e { display:none; }
  .orb-d { top:auto; bottom:8%; right:-46px; width:120px; }
}
.cta-copy, .cta-figure { position:relative; z-index:1; }
.cta-band h2, .cta-band p { max-width:none; }
.cta-figure { align-self:end; display:flex; justify-content:center; align-items:flex-end; }
.cta-figure img {
  height:clamp(360px,39vw,545px); width:auto; max-width:100%; display:block;
  filter:drop-shadow(0 22px 44px rgba(10,20,60,0.16));
}
@media (max-width:860px) {
  .cta-band { grid-template-columns:1fr; padding-bottom:0; }
  .cta-copy { padding-bottom:24px; }
  .cta-figure img { height:300px; }
}
div[style*="rgba(18,19,23,0.9)"] {
  background:linear-gradient(180deg,#ffffff,#f6f8fd) !important;
  border-color:var(--border-soft) !important;
}
/* real artwork per theme - no filter trickery */
.vmark { display:block; }
.vmark-on-dark { display:none; }

.flow-5 { grid-template-columns:repeat(5,1fr); }

@media (max-width:980px) {
  .hero-inner { grid-template-columns:1fr; }
  .hero-copy { padding-bottom:8px; }
  .hero h1 { max-width:none; }
  .hero-lede { max-width:none; }
  .benefits { grid-template-columns:1fr 1fr; }
  .benefit:nth-child(3)::before { display:none; }
  .flow-5 { grid-template-columns:1fr 1fr; }
  #problem .split, #thesis .split { grid-template-columns:1fr; }
  .stack-visual { max-width:560px; }
}
@media (max-width:620px) {
  /* height-bound sizing forces her wider than the column on a phone, so
     switch to width-bound here */
  .hero-figure img { height:auto; width:100%; max-width:330px; margin:0 auto; }
  .hero { padding-top:calc(var(--nav-h) + 10px); }
  .hero h1 { font-size:clamp(2.1rem,10.5vw,2.9rem); }
  .hero-lede { font-size:1.15rem; }
  .flow-5 { grid-template-columns:1fr; }
  .benefit { padding:18px 8px 14px; }
  .benefit .t { font-size:0.7rem; letter-spacing:0.1em; }
  .benefit .s { font-size:0.64rem; }
  .tagline { font-size:0.6rem; letter-spacing:0.14em; }
  .cta-band { padding:32px 22px 0; }
  .cta-copy { padding-bottom:26px; }
  .proof-visual figcaption { font-size:0.58rem; letter-spacing:0.05em; }
  /* the orbs are decoration - on a phone they crowd the copy */
  .orb-a { top:-64px; left:-56px; width:124px; }
  .orb-b { display:none; }
}
@media (max-width:560px) {
  /* "by Innovative Blockchain Solutions" wraps to three lines and doubles the
     nav height. The brand name alone carries it at this size. */
  .brand-sub { display:none; }
  .brand-name { font-size:0.95rem; }
}

/* ============================================================
   SVG colours that have to be themeable. These live in markup,
   not CSS, so they cannot follow the custom properties on their
   own - each one is driven by a class instead.
   ============================================================ */
.blend .to-paper { fill:var(--paper); }

/* ---------- theme toggle ---------- */
.theme-toggle {
  width:38px; height:38px; flex-shrink:0;
  display:inline-flex; align-items:center; justify-content:center;
  border-radius:10px;
  border:1px solid var(--border-soft);
  background:transparent;
  color:var(--muted);
  transition:color .2s, border-color .2s, background .2s;
}
.theme-toggle:hover { color:var(--ink); border-color:var(--border-strong); background:var(--glow-soft); }
.theme-toggle svg { width:17px; height:17px; display:block; }
.theme-toggle .ico-moon { display:none; }
[data-theme="dark"] .theme-toggle .ico-sun { display:none; }
[data-theme="dark"] .theme-toggle .ico-moon { display:block; }
.nav-inner { gap:14px; }
/* push the links + toggle into one right-hand group, otherwise space-between
   strands the toggle on its own at the far edge */
.nav-links { margin-left:auto; }
.nav-side { display:flex; align-items:center; gap:10px; }

/* ============================================================
   DARK THEME
   ============================================================ */
[data-theme="dark"] {
  --paper:#05070f;
  --mist:#0e1730;
  --ink:#f2f5ff;
  --muted:#9aa4c0;
  --dim:#6d7794;
  --surface:#0a0f1f;
  --surface-2:#111830;
  --surface-3:#18203c;
  --border:#242c47;
  --border-soft:rgba(255,255,255,0.10);
  --border-strong:rgba(255,255,255,0.20);
  --accent-hot:#5b8dff;
  --glow:rgba(59,130,246,0.30);
  --glow-soft:rgba(59,130,246,0.09);
}
[data-theme="dark"] body { background:var(--paper); color:var(--ink); }
[data-theme="dark"] ::selection { background:rgba(91,141,255,0.32); color:#fff; }

[data-theme="dark"] .hero {
  background:radial-gradient(80% 60% at 3% 24%, var(--mist), transparent 58%), var(--paper);
}
[data-theme="dark"] .hero h1 .grad {
  background:linear-gradient(104deg,#5b8dff 4%,#7b7bf0 54%,#9d7bf5 100%);
  -webkit-background-clip:text; background-clip:text;
}
[data-theme="dark"] .hero-lede b { color:#5b8dff; }
[data-theme="dark"] .nav.on { background:rgba(5,7,15,0.86); border-bottom-color:rgba(255,255,255,0.08); }
[data-theme="dark"] .nav-links a { color:rgba(242,245,255,0.62); }
[data-theme="dark"] .nav-links a:hover { color:#fff; }
[data-theme="dark"] .nav-toggle span { background:#fff; }
[data-theme="dark"] .nav.open .nav-links { background:rgba(5,7,15,0.97); }
[data-theme="dark"] .brand-mark { filter:drop-shadow(0 0 12px rgba(59,130,246,0.4)); }

[data-theme="dark"] .module,
[data-theme="dark"] .price,
[data-theme="dark"] .deploy,
[data-theme="dark"] .faq-item,
[data-theme="dark"] .billing-toggle { background:var(--surface); border-color:var(--border-soft); }
[data-theme="dark"] .module { background:linear-gradient(180deg,#0c1224,#080d1c); }
[data-theme="dark"] .module:hover { box-shadow:0 20px 46px -24px rgba(0,0,0,0.8),0 0 34px -18px var(--glow); }
[data-theme="dark"] .deploy:hover { background:var(--surface-2); }
[data-theme="dark"] .chip { background:rgba(255,255,255,0.03); border-color:rgba(255,255,255,0.14); }
[data-theme="dark"] .vert { background:rgba(255,255,255,0.03); }
[data-theme="dark"] .trust-pill { background:rgba(255,255,255,0.04); }
[data-theme="dark"] .price.featured {
  background:linear-gradient(180deg,rgba(59,130,246,0.14),var(--surface));
  border-color:rgba(91,141,255,0.45);
}
[data-theme="dark"] .billing-toggle button.on { background:rgba(59,130,246,0.18); color:#fff; }
[data-theme="dark"] .cta-band {
  background:radial-gradient(ellipse 80% 80% at 82% 16%,rgba(59,130,246,0.20),transparent 52%),
             linear-gradient(158deg,#0b1226,#060a16);
  box-shadow:0 30px 78px -36px rgba(0,0,0,0.9);
}
[data-theme="dark"] .stack-visual { border-color:rgba(255,255,255,0.10); }
[data-theme="dark"] .proof-visual figcaption { background:var(--surface); }
[data-theme="dark"] .vmark-on-light { display:none; }
[data-theme="dark"] .vmark-on-dark { display:block; }
[data-theme="dark"] div[style*="rgba(18,19,23,0.9)"] {
  background:linear-gradient(180deg,#0c1224,#070c19) !important;
  border-color:var(--border-soft) !important;
}
[data-theme="dark"] .hero-figure img { filter:drop-shadow(0 26px 54px rgba(0,0,0,0.55)); }
[data-theme="dark"] .cta-figure img { filter:drop-shadow(0 22px 44px rgba(0,0,0,0.5)); }
</style>
"""

HERO = """<!-- HERO -->
<section class="hero">
 <div class="wrap-wide hero-inner">
  <div class="hero-copy">
   <h1>Your entire practice.<span class="grad">One login.</span></h1>
   <p class="hero-lede">Replace complexity with <b>Cortex.</b></p>
   <p class="hero-sub">
    <strong>CORTEX Health AI</strong> replaces the SaaS vendors clinics stitch together: CRM, intake, voice, scheduling, retention, and at full tier the EHR itself.
    We integrate when we must. We build around blockers when vendors fail. Everything stays legal, compliant, and under medical scrutiny.
   </p>
   <div class="hero-actions">
    <a class="btn btn-primary" href="#start">Request a practice build</a>
    <a class="btn btn-ghost" href="#platform">See what we replace</a>
   </div>
  </div>

  <div class="hero-figure">
   <picture>
    <source srcset="/assets/clinician.webp" type="image/webp">
    <img src="/assets/clinician.png" alt="Physician in a white coat holding the CORTEX mark between her hands" width="774" height="882" fetchpriority="high" decoding="async">
   </picture>
  </div>
 </div>

 <div class="wrap-wide">
  <div class="benefits">
   <div class="benefit">
    <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
     <circle cx="13" cy="11.5" r="4.3"/>
     <path d="M4.8 25.5c0-4.5 3.7-7.3 8.2-7.3s8.2 2.8 8.2 7.3"/>
     <path d="M22.4 8.4a4.1 4.1 0 0 1 0 7.7"/>
     <path d="M24.6 18.9c2.7.9 4.6 3.3 4.6 6.6"/>
    </svg>
    <span class="t">More patients</span>
    <span class="s">Less hassle</span>
   </div>
   <div class="benefit">
    <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
     <circle cx="16" cy="16" r="11.2"/>
     <path d="M16 9.2V16.4l4.8 2.9"/>
    </svg>
    <span class="t">Less admin</span>
    <span class="s">More time</span>
   </div>
   <div class="benefit">
    <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
     <path d="M16 26.4C16 26.4 5.6 20.2 5.6 13.6A5.9 5.9 0 0 1 16 10.2a5.9 5.9 0 0 1 10.4 3.4c0 6.6-10.4 12.8-10.4 12.8Z"/>
    </svg>
    <span class="t">Better care</span>
    <span class="s">Happier patients</span>
   </div>
   <div class="benefit">
    <svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
     <path d="M6.5 26.5v-5.2"/><path d="M13 26.5v-8.8"/><path d="M19.5 26.5v-12"/><path d="M26 26.5v-15.6"/>
     <path d="M5.6 15.4 12.4 9l4.6 4.1L26.4 5"/>
     <path d="M21.6 5h4.8v4.8"/>
    </svg>
    <span class="t">Stronger practice</span>
    <span class="s">Higher revenue</span>
   </div>
  </div>
  <p class="tagline">Simplify. Automate. Grow. <b>All in one platform.</b></p>
 </div>

 <div class="blend">
  <svg viewBox="0 0 1440 200" preserveAspectRatio="none" aria-hidden="true">
   <defs>
    <linearGradient id="sweep" x1="0" y1="1" x2="1" y2="0">
     <stop offset="0" stop-color="#0048cc"/>
     <stop offset="0.52" stop-color="#2f39b8"/>
     <stop offset="1" stop-color="#483cb4"/>
    </linearGradient>
   </defs>
   <path d="M0,200 L0,150 C 260,164 560,132 820,88 C 1050,50 1250,20 1440,4 L1440,200 Z" fill="url(#sweep)"/>
   <path d="M0,200 L0,182 C 280,192 580,164 840,124 C 1070,88 1258,58 1440,42 L1440,200 Z" fill="#000c30"/>
  </svg>
 </div>
</section>

<!-- DEPLOYMENTS -->
<section class="section" id="deployments">
 <div class="wrap-wide">
  <div class="section-head center" style="margin-bottom: 28px;">
   <h2>Already running in real practices</h2>
   <p>Not a concept deck. Live builds across weight loss, wellness, massage, and multi-site clinical operations. Vitality is the flagship path: separate from the vendor maze and keep the clinic inside one ecosystem.</p>
  </div>
  <div class="deploys">
   <div class="deploy">
    <div class="deploy-tag">Weight loss</div>
    <h3>Vitality</h3>
    <p>Full practice OS. Facilitating separation from Athena and the SaaS stack, with compliant workarounds wherever a vendor blocked the clinic.</p>
   </div>
   <div class="deploy">
    <div class="deploy-tag">Academies</div>
    <h3>Vitality Academies</h3>
    <p>Multi-track patient engine and the reference Practice OS sandbox for the full CORTEX Health build.</p>
   </div>
   <div class="deploy">
    <div class="deploy-tag">Massage</div>
    <h3>Arron Lakey</h3>
    <p>Book ownership, scheduling, and client retention for a premium practice without a pile of disconnected tools.</p>
   </div>
   <div class="deploy">
    <div class="deploy-tag">Relationships</div>
    <h3>Rekindle</h3>
    <p>Counseling intake, continuum of care, and private client management inside one controlled system.</p>
   </div>
   <div class="deploy">
    <div class="deploy-tag">Spa tech</div>
    <h3>Body Language</h3>
    <p>TouchPrint capture plus spa enterprise CRM so guest preference lives with the business, not a single therapist.</p>
   </div>
  </div>
 </div>
 <div class="blend" style="margin-top: clamp(40px, 6vw, 88px);">
  <svg viewBox="0 0 1440 150" preserveAspectRatio="none" aria-hidden="true">
   <path d="M0,150 L0,72 C 380,150 940,138 1440,44 L1440,150 Z" class="to-paper"/>
  </svg>
 </div>
</section>

"""

start = src.index('<!-- HERO -->')
end = src.index('<!-- PROBLEM -->')
out = src[:start] + HERO + src[end:]

# ---- vendor chips: drop one so they settle into two even rows, then fill
#      the dead space below them with the platform overview -------------------
# ---- platform modules: numerals -> icons ----------------------------------
# 01..06 aren't a sequence - these are six parallel capabilities, so numbering
# them implied an order that doesn't exist. Icons drawn to match the line
# language already used by the hero benefit row and the platform image.
_ICO = json.loads((REPO / 'assets' / 'platform-icons.json').read_text(encoding='utf-8'))
for num, svg in _ICO.items():
    old = f' <div class="module-ico">{num}</div>'
    assert old in out, f'platform module {num} not found'
    out = out.replace(old, f' <div class="module-ico">{svg}</div>', 1)

# ---- keep "Desk free." together so it wraps as a unit onto the second line
_H2_OLD = '<h2>Inquiry in. Chart ready. Desk free.</h2>'
assert _H2_OLD in out, 'flow headline not found'
out = out.replace(_H2_OLD, '<h2>Inquiry in. Chart ready. Desk&nbsp;free.</h2>', 1)

# ---- real per-theme vendor marks, replacing the invert() hack -------------
# xAI/Grok ship official Dark (#0A0A0A, for light backgrounds) and Light
# (white, for dark) variants; Anthropic's wordmark is recoloured from the same
# artwork. Both are in the DOM and CSS shows the right one per theme.
def _mark(slug, label, dark, light, h):
    return (f'<img class="vmark vmark-on-light" src="/assets/{dark}" alt="{label}" '
            f'style="height:{h}px; width:auto;">'
            f'<img class="vmark vmark-on-dark" src="/assets/{light}" alt="" aria-hidden="true" '
            f'style="height:{h}px; width:auto;">')

for old, new in [
    ('<img src="/assets/xai-logomark.png" alt="xAI" height="28" style="height:28px; width:auto;">',
     _mark('xai', 'xAI', 'xai-mark-dark.svg', 'xai-mark-light.svg', 28)),
    ('<img src="/assets/anthropic-logo.png" alt="Anthropic" height="22" style="height:22px; width:auto;">',
     _mark('anthropic', 'Anthropic', 'anthropic-mark-dark.png', 'anthropic-logo.png', 22)),
]:
    assert old in out, f'vendor mark not found: {old[:46]}'
    out = out.replace(old, new, 1)

# ---- drop the named physician from the copy, keep the claim ---------------
for old, new in [
    ('under strict medical scrutiny from Dr. DeBry.',
     'under strict medical scrutiny.'),
    ('<p>Workarounds and clinical workflows go under medical scrutiny (as with Dr. DeBry on Vitality) so we ship what a real practice can defend.</p>',
     '<p>Workarounds and clinical workflows go under physician review so we ship what a real practice can defend.</p>'),
]:
    assert old in out, f'copy not found: {old[:50]}'
    out = out.replace(old, new, 1)

# ---- help panel beside the A/B/C cards (not under them, which added 475px)
_TM_OLD = '<div class="modules" style="grid-template-columns: 1fr; gap: 12px;">'
assert _TM_OLD in out, 'thesis modules div not found'
out = out.replace(_TM_OLD, '<div class="modules thesis-modules">', 1)

_ABC_OLD = """ <p>Highest tier replaces the full set, including EHR. The clinic keeps the data and the control plane.</p>
 </article>
 </div>"""
_ABC_NEW = """ <p>Highest tier replaces the full set, including EHR. The clinic keeps the data and the control plane.</p>
 </article>
 <figure class="stack-visual help-visual">
 <picture>
 <source srcset="/assets/cortex-help.webp" type="image/webp">
 <img src="/assets/cortex-help.png" alt="CORTEX Help panel: system how-to answered instantly, with suggested questions about patient portal logins, patient tasks, sequences, and booking an InBody scan." width="370" height="522" loading="lazy" decoding="async">
 </picture>
 </figure>
 </div>"""
assert _ABC_OLD in out, 'thesis A/B/C block not found'
out = out.replace(_ABC_OLD, _ABC_NEW, 1)

# ---- flow grid: inline style beats every media query, so it stayed 5-up on
#      phones and forced ~600px of horizontal overflow. Move it into CSS. -----
_FLOW_OLD = '<div class="modules flow-5" style="grid-template-columns: repeat(5, 1fr);">'
assert _FLOW_OLD in out, 'flow grid not found'
out = out.replace(_FLOW_OLD, '<div class="modules flow-5">', 1)

# ---- thesis: real Vitality provider UI under the paragraph -----------------
_TH_ANCHOR = """ That is how we know what a clinic can remove, what must stay, and how to confine almost 100% of operations inside CORTEX Health.
 </p>"""
_TH_NEW = _TH_ANCHOR + """
 <figure class="stack-visual proof-visual">
 <picture>
 <source srcset="/assets/vitality-provider.webp" type="image/webp">
 <img src="/assets/vitality-provider.jpg" alt="Vitality provider view inside CORTEX Health: wearable health checkpoint, resting heart rate and HRV trends, an AI clinical summary, and an InBody body composition map." width="1342" height="832" loading="lazy" decoding="async">
 </picture>
 <figcaption>Vitality provider view, running in CORTEX Health. De-identified demo tenant.</figcaption>
 </figure>"""
assert _TH_ANCHOR in out, 'thesis paragraph anchor not found'
out = out.replace(_TH_ANCHOR, _TH_NEW, 1)

# ---- eyebrow cleanup ------------------------------------------------------
# whole eyebrow removed
for gone in [
    ' <div class="eyebrow" style="margin-bottom: 14px;">What clinics pay for today</div>\n',
    ' <span class="eyebrow"><span class="dot"></span> CORTEX Health AI</span>\n',
    ' <span class="eyebrow"><span class="dot"></span> How we build</span>\n',
]:
    assert gone in out, f'eyebrow not found: {gone.strip()[:60]}'
    out = out.replace(gone, '', 1)

# eyebrow kept, only the pulsing dot dropped
for keep in [
    (' <span class="eyebrow"><span class="dot"></span> Regulated healthcare</span>',
     ' <span class="eyebrow">Regulated healthcare</span>'),
    (' <span class="eyebrow"><span class="dot"></span> Pricing</span>',
     ' <span class="eyebrow">Pricing</span>'),
]:
    assert keep[0] in out, f'eyebrow not found: {keep[0].strip()[:60]}'
    out = out.replace(keep[0], keep[1], 1)

_cs = out.index('<div class="stack-chaos">')
_ce = out.index('</div>', out.index('<span class="chip">Spreadsheets</span>')) + len('</div>')
out = out[:_cs] + """<figure class="stack-visual">
 <picture>
 <source srcset="/assets/cortex-platform.webp" type="image/webp">
 <img src="/assets/cortex-platform.jpg" alt="CORTEX Health platform overview: EHR, scheduling, HIPAA compliance, patient engagement, reporting, and billing running as one connected system." width="1254" height="1254" loading="lazy" decoding="async">
 </picture>
 </figure>""" + out[_ce:]

# ---- CTA band: two columns, figure standing in the empty right half --------
CTA_OLD = """ <div class="cta-band">
 <span class="eyebrow"><span class="dot"></span> Your move</span>"""
_ORB = (' <picture class="cta-orb orb-{k}" aria-hidden="true">\n'
        ' <source srcset="/assets/orb.webp" type="image/webp">\n'
        ' <img src="/assets/orb.png" alt="" width="640" height="640" loading="lazy" decoding="async">\n'
        ' </picture>\n')
CTA_NEW = ' <div class="cta-band">\n' + ''.join(_ORB.format(k=k) for k in 'abcde') + ' <div class="cta-copy">'
assert CTA_OLD in out, 'CTA band opening not found'
out = out.replace(CTA_OLD, CTA_NEW, 1)

CTA_TAIL_OLD = """ <a class="btn btn-ghost" href="mailto:support@innovativeblockchainsolutions.live?subject=CORTEX%20Health%20AI%20Practice%20build">Email the team</a>
 </div>
 </div>"""
CTA_TAIL_NEW = """ <a class="btn btn-ghost" href="mailto:support@innovativeblockchainsolutions.live?subject=CORTEX%20Health%20AI%20Practice%20build">Email the team</a>
 </div>
 </div>
 <div class="cta-figure">
 <picture>
 <source srcset="/assets/cta-figure.webp" type="image/webp">
 <img src="/assets/cta-figure.png" alt="Physician in a white coat with a stethoscope, arms folded" width="645" height="1000" loading="lazy" decoding="async">
 </picture>
 </div>
 </div>"""
assert CTA_TAIL_OLD in out, 'CTA band closing not found'
out = out.replace(CTA_TAIL_OLD, CTA_TAIL_NEW, 1)

out = out.replace('</head>', CSS + '</head>', 1)

# ---- theme toggle ---------------------------------------------------------
# set before first paint, otherwise a dark-preference visitor gets a white flash
BOOT = """<script>
(function(){try{
 var s=localStorage.getItem('cx-theme');
 var d=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
 document.documentElement.setAttribute('data-theme', s || (d?'dark':'light'));
}catch(e){document.documentElement.setAttribute('data-theme','light');}})();
</script>
"""
out = out.replace('<style id="cortex-theme">', BOOT + '<style id="cortex-theme">', 1)

TOGGLE = """ <div class="nav-side">
 <button class="theme-toggle" id="themeToggle" type="button" aria-label="Switch colour theme" aria-pressed="false">
 <svg class="ico-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
 <circle cx="12" cy="12" r="4.2"/><path d="M12 2.4v2.6"/><path d="M12 19v2.6"/><path d="M2.4 12h2.6"/><path d="M19 12h2.6"/>
 <path d="M5.2 5.2l1.9 1.9"/><path d="M16.9 16.9l1.9 1.9"/><path d="M18.8 5.2l-1.9 1.9"/><path d="M7.1 16.9l-1.9 1.9"/>
 </svg>
 <svg class="ico-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
 <path d="M20.5 14.6A8.6 8.6 0 0 1 9.4 3.5a8.6 8.6 0 1 0 11.1 11.1Z"/>
 </svg>
 </button>
 <button class="nav-toggle" id="navToggle" aria-label="Menu" type="button">
 <span></span><span></span><span></span>
 </button>
 </div>"""
_NAV_OLD = """ <button class="nav-toggle" id="navToggle" aria-label="Menu" type="button">
 <span></span><span></span><span></span>
 </button>"""
assert _NAV_OLD in out, 'nav toggle button not found'
out = out.replace(_NAV_OLD, TOGGLE, 1)

THEME_JS = """<script>
(function(){
 var root=document.documentElement, btn=document.getElementById('themeToggle');
 function sync(){ btn.setAttribute('aria-pressed', root.getAttribute('data-theme')==='dark'); }
 sync();
 btn.addEventListener('click', function(){
  var next = root.getAttribute('data-theme')==='dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  try{ localStorage.setItem('cx-theme', next); }catch(e){}
  sync();
 });
})();
</script>
</body>"""
out = out.replace('</body>', THEME_JS, 1)

(REPO / 'index.html').write_text(out, encoding='utf-8')
print('wrote index.html')
