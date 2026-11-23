# 1% Design Lab · 梦想管理局

Source of **[1-design-lab.com](https://1-design-lab.com)** — the official bilingual（中文 / English）website of 1% Design Lab, a Shanghai-based design and creative-technology studio operated by 上海光有序科技有限公司.

## Two businesses, one brand

- **Product Studio** — for founders and companies: [AI app development](https://1-design-lab.com/services/ai-app-development)（单核心功能套餐 ¥18,000，标准周期 14 天）, full-stack product design & development (AI products, SaaS, mini-programs, websites), logo & brand identity, and industrial design / 3D.
- **Portfolio Academy** — for art and design applicants: portfolio mentoring for study-abroad and domestic postgraduate applications, exhibitions, and job hunting.

## Links

- 🌐 Live: <https://1-design-lab.com> · English: <https://1-design-lab.com/en/>
- 👤 Founder: [Joey Zhao](https://joeyzhao.cc)
- ✉️ Contact: super666joey@gmail.com

## Self-built products

- [Finfold](https://finfold.app) — AI marketing SaaS
- [BillVampire](https://billvampire.com) — AI bill splitting
- [joeyzhao.cc](https://joeyzhao.cc) — 3D interactive portfolio

## Tech

Pure static site — HTML/CSS/JS with `_redirects` / `_headers` rules and a few edge functions, served behind Cloudflare.

The committed HTML is the source of truth and is deployed as is; Cloudflare Pages runs no build step, so pages are edited directly. The earlier page generator scripts (`scripts/build-site.py` and its post-processing modules) were removed on 2026-11-23: they had fallen behind the committed pages, and regenerating from them would have reverted live copy. Notes under `docs/` that mention those scripts are historical.
