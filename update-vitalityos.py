#!/usr/bin/env python3
"""Re-apply this site's integration to a fresh Vitality OS case study export.

The case study is authored elsewhere and arrives as a standalone HTML file
(by email, into ~/Downloads). It is written as a self-contained document with
no knowledge of this site, so every export ships the same gaps:

  1. The CTA is a mailto: to fcorona@vitalityacademies.health. It hands the
     visitor to whatever mail client their machine has and captures nothing
     in the CRM.
  2. The expansion grid carries grid-template-columns as an INLINE style,
     which outranks every media query, so the page scrolls sideways on
     phones. Two more grids floor at min-content for the same reason.
  3. No head meta, no canonical, no share card, so links preview as a bare
     text row.
  4. The brand mark is a dead div, so the page never points back to us.

This script applies all of it in one pass. Every patch asserts its anchor
appears exactly once: if a future export rewrites one of these blocks, this
fails loudly naming the patch rather than silently shipping a half-wired page.

Usage:
    python3 update-vitalityos.py ~/Downloads/vitality_os_case_study.html
    git diff vitalityos/index.html     # review, then commit
"""

import sys
import pathlib

REPO = pathlib.Path(__file__).resolve().parent
DEST = REPO / 'vitalityos' / 'index.html'

SB_URL = 'https://jtifhcvbgxqwlywugvjv.supabase.co'
ANON = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6'
        'Imp0aWZoY3ZiZ3hxd2x5d3Vndmp2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MDc5'
        'NTgsImV4cCI6MjA4ODA4Mzk1OH0.UfRVLuvM8_HPvKXUEDXb0cxR50znv16L5Tf99AnSc7g')

HEAD_META = '''<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vitality OS Case Study | CORTEX Health AI</title>
<meta name="description" content="How Vitality Weight Loss replaced a dozen disconnected subscriptions with one physician-led operating system that acquires the patient, treats them, bills them, and keeps them. Built and deployed by CORTEX Health AI.">
<meta name="author" content="Innovative Blockchain Solutions">
<meta name="theme-color" content="#0B1220">
<link rel="canonical" href="https://cortexhealthai.com/vitalityos/">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CORTEX Health AI">
<meta property="og:url" content="https://cortexhealthai.com/vitalityos/">
<meta property="og:title" content="Vitality OS: from struggling startup to a finely-tuned machine">
<meta property="og:description" content="A stack of a dozen silos replaced by one owned operating system: CRM, EHR, billing, clearinghouse, AI scribe, patient app, and Academy on a single record.">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="https://cortexhealthai.com/assets/og-vitalityos.png">
<meta property="og:image:secure_url" content="https://cortexhealthai.com/assets/og-vitalityos.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vitality OS case study by CORTEX Health AI: from struggling startup to a finely-tuned machine.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Vitality OS Case Study | CORTEX Health AI">
<meta name="twitter:description" content="One spine, four surfaces, zero seams. The operating system behind Vitality, and what it does to a clinic\'s margins.">
<meta name="twitter:image" content="https://cortexhealthai.com/assets/og-vitalityos.png">
<meta name="twitter:image:alt" content="Vitality OS case study by CORTEX Health AI.">'''

FORM_JS = '''  /* Strategy-session form. Posts to the IBS CRM (ibs_prospects) via the
     cortexhealth-lead edge function, tagged source=cortexhealth_vitalityos so
     these separate from campaign leads in the CRM source filter. This used to
     be a mailto:, which handed the visitor to whatever mail client their
     machine had and captured nothing on our side. */
  var CH_SB   = \'''' + SB_URL + '''\';
  var CH_ANON = \'''' + ANON + '''\';

  function cortexSubmit(e){
    e.preventDefault();
    var f    = e.target;
    var btn  = document.getElementById(\'ctaBtn\');
    var sent = document.getElementById(\'ctaSent\');
    var err  = document.getElementById(\'ctaErr\');

    err.style.display = \'none\';
    btn.disabled = true;
    btn.textContent = \'Sending...\';

    /* Attribution, so marketing can trace the lead inside the CRM. */
    var qs  = new URLSearchParams(location.search);
    var utm = [\'utm_source\',\'utm_medium\',\'utm_campaign\',\'utm_term\',\'utm_content\']
      .map(function(k){ var v = qs.get(k); return v ? k + \'=\' + v : null; })
      .filter(Boolean).join(\' | \');

    fetch(CH_SB + \'/functions/v1/cortexhealth-lead\', {
      method: \'POST\',
      headers: { \'Content-Type\': \'application/json\', \'apikey\': CH_ANON },
      body: JSON.stringify({
        first_name: f.fn.value,
        last_name:  f.ln.value,
        email:      f.email.value,
        phone:      f.phone.value,
        clinic:     f.clinic.value,
        comment:    f.comment.value,
        website:    f.website.value,
        page:       location.href.split(\'#\')[0],
        referrer:   document.referrer ? document.referrer.slice(0, 300) : \'\',
        utm:        utm
      })
    })
    .then(function(r){ return r.json().catch(function(){ return {}; }).then(function(d){ return { ok: r.ok, d: d }; }); })
    .then(function(res){
      if (!res.ok || !res.d.ok) throw new Error(res.d.error || \'Something went wrong. Please try again.\');
      f.reset();
      btn.style.display = \'none\';
      sent.style.display = \'block\';
    })
    .catch(function(ex){
      /* A rejected fetch is a TypeError and its message ("Failed to fetch") is
         not something to show a clinic owner. Only our own errors carry copy
         worth reading. */
      var msg = (ex && ex.name === \'TypeError\')
        ? \'We could not reach our server. Please check your connection and try again.\'
        : ((ex && ex.message) || \'Something went wrong. Please try again.\');
      err.textContent = msg + \' You can also email support@innovativeblockchainsolutions.live.\';
      err.style.display = \'block\';
      btn.disabled = false;
      btn.textContent = \'Request my free strategy session\';
    });

    return false;
  }'''

MAILTO_JS = '''  function cortexSubmit(e){
    e.preventDefault();
    var f = e.target;
    var name = (f.fn.value + \' \' + f.ln.value).trim();
    var subject = \'Free strategy session request: \' + name + \' (\' + f.clinic.value + \')\';
    var lines = [
      \'Name: \' + name,
      \'Email: \' + f.email.value,
      \'Phone: \' + f.phone.value,
      \'Clinic / practice: \' + f.clinic.value,
      \'\',
      \'What they want to fix or build:\',
      f.comment.value || \'(none provided)\'
    ];
    var href = \'mailto:fcorona@vitalityacademies.health\'
      + \'?subject=\' + encodeURIComponent(subject)
      + \'&body=\' + encodeURIComponent(lines.join(\'\\n\'));
    document.getElementById(\'ctaSent\').style.display = \'block\';
    window.location.href = href;
    return false;
  }'''

# (label, find, replace). Each `find` must occur exactly once.
PATCHES = [
    ('head meta + share card',
     '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
     '<title>Vitality OS, Case Study: Zero to a Finely-Tuned Machine</title>',
     HEAD_META),

    ('brand styles',
     ' .brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em}',
     ' .brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:-.02em;color:var(--ink)}\n'
     ' .brand:hover{color:var(--blue)}\n'
     ' .brand small{display:block;font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}'),

    ('brand links home',
     '  <div class="brand">\n'
     '   <span class="spark" role="img" aria-label="Vitality Weight Loss"></span>\n'
     '   Vitality&nbsp;OS\n'
     '  </div>',
     '  <a class="brand" href="/">\n'
     '   <span class="spark" role="img" aria-label="Vitality Weight Loss"></span>\n'
     '   <span>Vitality&nbsp;OS<small>CORTEX Health AI</small></span>\n'
     '  </a>'),

    ('grid tracks may shrink below min-content',
     ' @media(max-width:880px){.g2,.g3,.g4{grid-template-columns:1fr}}',
     " /* minmax(0,...) not 1fr: a bare 1fr floors at the track's min-content, so a\n"
     '    wide child like the 3-column economics table drags the column past the\n'
     '    viewport instead of being allowed to scroll inside it. */\n'
     ' @media(max-width:880px){.g2,.g3,.g4{grid-template-columns:minmax(0,1fr)}}'),

    ('vendor cloud fits a 320px phone',
     ' @media(max-width:880px){.surfaces4{grid-template-columns:repeat(2,1fr)}.arch-before .hubcloud{grid-template-columns:repeat(3,1fr)}}',
     ' @media(max-width:880px){.surfaces4{grid-template-columns:repeat(2,1fr)}.arch-before .hubcloud{grid-template-columns:repeat(3,1fr)}}\n'
     ' /* 1fr floors at min-content, and vendor names like athenaOne cannot wrap, so\n'
     '    three columns push wider than their own container on a 320px phone. Two\n'
     '    columns of minmax(0,1fr) let the track shrink and keep the page in bounds. */\n'
     ' @media(max-width:400px){.arch-before .hubcloud{grid-template-columns:repeat(2,minmax(0,1fr))}}'),

    ('flow-3 class the media query can beat',
     ' .flow{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;align-items:stretch}\n'
     ' @media(max-width:880px){.flow{grid-template-columns:1fr}}',
     ' .flow{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;align-items:stretch}\n'
     ' .flow-3{grid-template-columns:repeat(3,1fr)}\n'
     ' @media(max-width:880px){.flow,.flow-3{grid-template-columns:1fr}}'),

    ('economics table scrolls in its own cell',
     ' .econ-table tr:last-child td{border-bottom:0}',
     ' .econ-table tr:last-child td{border-bottom:0}\n'
     ' /* Below ~520px the three money columns cannot fit. Scroll the table inside\n'
     '    its own cell rather than letting it widen the page. */\n'
     ' @media(max-width:520px){#economics .grid.g2>div{overflow-x:auto}}'),

    ('inline grid override -> class',
     '<div class="flow" style="grid-template-columns:repeat(3,1fr)">',
     '<div class="flow flow-3">'),

    ('form states',
     '  .cta-note{font-size:12px;color:var(--muted)}\n'
     '  .cta-sent{display:none;margin-top:12px;font-size:13.5px;font-weight:700;color:var(--green)}',
     '  .cta-note{font-size:12px;color:var(--muted)}\n'
     '  .cta-submit button[disabled]{opacity:.6;cursor:default}\n'
     '  .cta-sent{display:none;margin-top:12px;font-size:13.5px;font-weight:700;color:var(--green)}\n'
     '  .cta-err{display:none;margin-top:12px;font-size:13.5px;font-weight:700;color:var(--red)}\n'
     '  .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}'),

    ('honeypot + CRM copy',
     '        </div>\n'
     '        <div class="cta-submit">\n'
     '          <button type="submit">Request my free strategy session</button>\n'
     '          <span class="cta-note">Opens a prefilled email to our team at fcorona@vitalityacademies.health.</span>\n'
     '        </div>\n'
     '        <div class="cta-sent" id="ctaSent">Thanks. Your email draft is ready, just hit send and we will be in touch.</div>\n'
     '      </form>',
     '        </div>\n'
     '        <div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>\n'
     '        <div class="cta-submit">\n'
     '          <button type="submit" id="ctaBtn">Request my free strategy session</button>\n'
     '          <span class="cta-note">Goes straight to our team. We reply within one business day.</span>\n'
     '        </div>\n'
     '        <div class="cta-sent" id="ctaSent">Thanks, we have it. A real person reviews it and reaches out to schedule, usually within one business day. Check your inbox for the confirmation.</div>\n'
     '        <div class="cta-err" id="ctaErr"></div>\n'
     '      </form>'),

    ('mailto -> cortexhealth-lead', MAILTO_JS, FORM_JS),
]

# Nothing on this list may survive into the deployed file.
FORBIDDEN = [
    ('mailto:fcorona', 'the CTA still opens a mail client'),
    ('style="grid-template-columns:repeat(3,1fr)"', 'the inline grid override is still present'),
]

# These must all be present when we are done.
REQUIRED = [
    ('cortexhealth-lead', 'form is not wired to the CRM'),
    ('og:image', 'no share card'),
    ('class="brand" href="/"', 'brand does not link home'),
    ('flow flow-3', 'expansion grid will not collapse on phones'),
    ('minmax(0,1fr)', 'grid tracks cannot shrink'),
    ('id="website"', 'honeypot missing'),
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().split('Usage:')[-1].strip())

    src = pathlib.Path(sys.argv[1]).expanduser()
    if not src.is_file():
        sys.exit(f'not a file: {src}')

    html = src.read_text(encoding='utf-8')
    print(f'read {src}  ({len(html):,} bytes)')

    for label, old, new in PATCHES:
        n = html.count(old)
        if n != 1:
            sys.exit(
                f'\nFAILED on patch: {label}\n'
                f'  expected its anchor exactly once, found {n}.\n'
                f'  The export changed shape here. Re-read the block in\n'
                f'  {src} and update this patch before deploying.\n'
                f'  Anchor started: {old[:90]!r}'
            )
        html = html.replace(old, new, 1)
        print(f'  applied  {label}')

    problems = [why for token, why in FORBIDDEN if token in html]
    problems += [why for token, why in REQUIRED if token not in html]
    if problems:
        sys.exit('\nFAILED verification:\n  ' + '\n  '.join(problems))

    DEST.write_text(html, encoding='utf-8')
    print(f'\nwrote {DEST}  ({len(html):,} bytes)')
    print('all patches applied and verified. review with:  git diff vitalityos/index.html')


if __name__ == '__main__':
    main()
