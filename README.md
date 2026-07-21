# CORTEX Health AI

**Medical-grade CRM · Patient management · EHR-connected practice OS**

Product site for [cortexhealthai.com](https://cortexhealthai.com) — the healthcare vertical of **Innovative Blockchain Solutions (IBS)**.

## What this is

CORTEX Health AI is the public face of IBS's medical / wellness practice systems:

- HIPAA-aware patient CRM and pipeline
- Secure digital intake
- EHR / practice-management sync
- Voice + after-hours capture
- Retention, recalls, reactivations
- Provider and patient portals

Live and in-flight deployments include **Vitality**, **Vitality Academies**, **Arron Lakey**, **Rekindle**, and **Body Language**, with additional practices in the pipeline.

## Stack

- Static HTML / CSS / JS (no build system)
- Intake → Supabase edge function `ibs-checkout-intake` → `ibs_clients` + ops tasks (IBS CRM)
- Same design language as cortexibs.com / logistixibs.com / innovativeblockchainsolutions.live (`DESIGN.md`)

## Local

```bash
# from this repo
python3 -m http.server 8765
# open http://localhost:8765
```

## Deploy

1. Connect this repo to GitHub Pages (or Netlify / Cloudflare Pages).
2. Custom domain: `cortexhealthai.com` (see `CNAME`).
3. Ensure DNS apex / www point at the host.
4. Intake already posts to production Supabase; no extra env on the frontend beyond the public anon key used by other IBS checkouts.

## Checkout → IBS CRM

| Path | Purpose |
|------|---------|
| `/checkout/get-started.html?tier=starter\|professional\|enterprise\|custom` | Intake form |
| `/checkout/success.html` | Confirmation |

Payload includes:

- Standard CRM fields (`company_name`, `contact_name`, `email`, `phone`, `tier`, `has_assets`, consent versions)
- `source: cortexhealthai.com`
- `product_line: cortex_health`
- `notes` with health tier + practice type for Miguel / Luis ops queue

Tier map:

| Marketing name | CRM `tier` |
|----------------|------------|
| Core | `starter` |
| Growth | `professional` |
| Scale | `enterprise` |
| Demand | `custom` |

## Brand

- Parent: Innovative Blockchain Solutions
- Product: CORTEX Health AI
- Logos: `/assets/ibs-mark.svg`, `/assets/ibs-logo-dark.svg`, `/assets/IBS_LOGO_WHITE.jpg`
- Design system: dark cinematic premium — see `DESIGN.md`

## Contact

- support@innovativeblockchainsolutions.live
- https://innovativeblockchainsolutions.live
- https://www.linkedin.com/company/innovative-blockchain-solutions
