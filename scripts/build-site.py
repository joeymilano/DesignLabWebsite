"""Generate the brand pages: /, /studio/, /academy/ and their /en/ twins.

Content lives in scripts/site_content.py; styles and behaviour in assets/site/.
Run: python3 scripts/build-site.py
"""
import html
import json
from pathlib import Path
from seo_metadata import enrich_graph

from site_content import (
    ACADEMY_RES, ACADEMY_SERVICES, ACADEMY_STATS, ACADEMY_STEPS, BRAND_REVIEW, CATS, CREDITS, EMAIL,
    MENTOR_BIO, MENTOR_TAGS, PEOPLE, PRODUCTS, REVIEWS, SCHOOLS, SHOP, STUDENT_WORK, STUDIO_RES,
    STUDIO_SERVICES, STUDIO_STATS, STUDIO_STEPS, TB, WORK_SIZE, XHS, B,
)

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://1-design-lab.com"
VER = "20260927"
LANG = "zh"  # set per page by build()


def t(v):
    """Pick the current language from a B(zh, en) value."""
    if isinstance(v, dict) and set(v) == {"zh", "en"}:
        return v[LANG]
    return v


def e(v):
    return html.escape(str(t(v)), quote=True)


def zh():
    return LANG == "zh"


def pre():
    return "" if zh() else "/en"


def lines(*rows):
    return "".join(f'<span class="ln"><span>{r}</span></span>' for r in rows)


def ext(url, label=None):
    data = f' data-label="{e(label)}"' if label else ""
    return f'href="{url}" target="_blank" rel="noopener"{data}'


def num_fmt(n):
    return f"{n:,.1f}" if isinstance(n, float) else f"{n:,}"


# ------------------------------------------------------------------ frame

def head(path, biz, title, desc, keywords, og, ld):
    url = ORIGIN + pre() + path
    zh_url, en_url = ORIGIN + path, ORIGIN + "/en" + path
    ld = enrich_graph(ld, url, title, desc, 'zh-CN' if zh() else 'en')
    return f"""<!doctype html>
<html lang="{'zh-CN' if zh() else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="baidu-site-verification" content="codeva-Ko5wEj732h">
<meta name="renderer" content="webkit">
<meta name="applicable-device" content="pc,mobile">
<meta http-equiv="Cache-Control" content="no-transform">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="1% Design Lab 梦想管理局">
<meta name="theme-color" content="#0B0B0A">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{zh_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{zh_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="1% Design Lab">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/share/{og}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'zh_CN' if zh() else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{ORIGIN}/assets/share/{og}.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/favicon-180x180.png" sizes="180x180">
<link rel="preload" href="/assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/GeistMono-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://fonts.loli.net" crossorigin>
<link rel="stylesheet" href="https://fonts.loli.net/css2?family=Noto+Sans+SC:wght@400;500;600&amp;display=swap" media="print" onload="this.media='all'">
<link rel="stylesheet" href="/assets/site/site.css?v={VER}">
<noscript><style>[data-reveal]{{opacity:1;transform:none}}.ln>span{{transform:none}}</style></noscript>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K0742RTMPL"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-K0742RTMPL');</script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
</head>
<body data-biz="{biz}">
<a class="skip" href="#main">{'跳到正文' if zh() else 'Skip to content'}</a>
"""


def dot_span(d):
    return f'<span class="dot {d}"></span>' if d else ""


def nav_items():
    p = pre()
    return [
        (f"{p}/studio/", B("产品工作室", "Product Studio"), "s", "studio"),
        (f"{p}/academy/", B("作品集学院", "Portfolio Academy"), "a", "academy"),
        (f"{p}/#work", B("作品", "Work"), None, "work"),
        (f"{p}/#people", B("团队", "People"), None, "people"),
        ("/blog/", B("文章", "Journal"), None, "blog"),
    ]


def header(path, cur):
    items = []
    for href, label, dot, key in nav_items():
        c = ' aria-current="page"' if key == cur else ""
        items.append(f'<a href="{href}"{c}>{dot_span(dot)}{e(label)}</a>')
    mitems = [f'<a href="{h}">{dot_span(d)}{e(l)}</a>' for h, l, d, _ in nav_items()]
    zh_href, en_href = path, "/en" + path
    lang = (f'<span aria-current="true">中</span> / <a href="{en_href}" hreflang="en">EN</a>' if zh()
            else f'<a href="{zh_href}" hreflang="zh-CN">中</a> / <span aria-current="true">EN</span>')
    talk = "聊聊" if zh() else "Let's talk"
    return f"""
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="wm" href="{pre() or '/'}{'/' if pre() else ''}" >1% Design Lab<small>{'梦想管理局' if zh() else 'SHANGHAI'}</small></a>
    <nav class="nav" aria-label="{'主导航' if zh() else 'Main'}">
      {''.join(items)}
    </nav>
    <div class="hdr-r">
      <span class="clock mono" data-clock>SHA 00:00 GMT+8</span>
      <span class="lang">{lang}</span>
      <button class="btn btn-solid" data-consult data-from="header">{talk} <span class="arr">↗</span></button>
      <button class="burger" aria-label="{'菜单' if zh() else 'Menu'}" aria-expanded="false"><i></i><i></i></button>
    </div>
  </div>
</header>
<nav class="mnav" aria-label="{'移动导航' if zh() else 'Mobile'}">
  {''.join(mitems)}
  <div class="mnav-foot"><span class="lang">{lang}</span><button class="btn btn-solid" data-consult data-from="menu">{talk} <span class="arr">↗</span></button></div>
</nav>
<main id="main">
"""


def footer():
    p = pre()
    cols = [
        (B("产品工作室", "Product Studio"), "s", [
            ("/services/ai-app-development", B("AI 应用开发", "AI app development")),
            (f"{p}/studio/#services", B("产品设计 × 全栈", "Product × full-stack")),
            ("/services/logo-branding", B("LOGO / 品牌 VI", "Brand identity")),
            ("/services/industrial-design", B("工业设计 / 3D", "Industrial / 3D")),
            ("/tools/landing-page-audit", B("Landing Page 审计", "Landing page audit")),
        ]),
        (B("作品集学院", "Portfolio Academy"), "a", [
            (B("/services/portfolio-design", "/en/design-portfolio/"), B("作品集设计", "Portfolio design")),
            ("/services/phd-research-proposal", B("博士研究计划", "PhD proposal")),
            (f"{p}/academy/#stories", B("录取故事", "Admission stories")),
            ("/portfolio/", B("作品集案例", "Portfolio cases")),
            ("/tools/portfolio-reviewer", B("AI 作品集诊断", "AI portfolio review")),
        ]),
        (B("资源", "Resources"), None, [
            ("/blog/", B("文章", "Journal")),
            ("/tools/", B("免费工具", "Free tools")),
            (B("/careers/", "/en/careers/"), B("加入我们", "Careers")),
            (B("/en/", "/"), B("English", "中文")),
        ]),
    ]
    html_cols = []
    for title, dot, links in cols:
        d = f'<span class="dot {dot}"></span>' if dot else ""
        lis = "".join(f'<li><a href="{t(h)}">{e(l)}</a></li>' for h, l in links)
        html_cols.append(f'<div><h3>{d}{e(title)}</h3><ul>{lis}</ul></div>')
    contact = f"""<div><h3>{'联系' if zh() else 'Contact'}</h3><ul>
      <li><button data-consult data-from="footer">{'微信咨询' if zh() else 'WeChat'}</button></li>
      <li><a {ext(XHS, 'xiaohongshu')}>{'小红书' if zh() else 'Xiaohongshu'} ↗</a></li>
      <li><a {ext(SHOP, 'taobao-shop')}>{'淘宝店铺' if zh() else 'Taobao shop'} ↗</a></li>
      <li><a href="mailto:{EMAIL}">Email</a></li>
    </ul></div>"""
    intro = B("上海光有序科技有限公司旗下的设计与创意技术品牌。一支团队，两种交付：为创业者把产品做上线，为申请者把作品集做出来。",
              "A design and creative-technology studio in Shanghai. One team, two deliverables: products that go live for founders, portfolios that get remembered for applicants.")
    addr = B("上海市黄浦区北京东路 668 号裙楼<br>黄浦汇数智心城", "668 East Beijing Rd, Huangpu<br>Shanghai, China")
    return f"""</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-cols">
      <div class="ftr-intro"><h3>1% Design Lab · {'梦想管理局' if zh() else 'Dream Bureau'}</h3><p>{e(intro)}</p><p class="muted" style="margin-top:18px">{t(addr)}</p></div>
      {''.join(html_cols)}
      {contact}
    </div>
    <p class="ftr-wm" aria-hidden="true">1%<span> </span>Design Lab</p>
  </div>
  <div class="ftr-base"><div class="wrap" style="display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;width:100%">
    <span class="label">© 2026 {'上海光有序科技有限公司' if zh() else 'Shanghai LightOrder Technology Co., Ltd.'}</span>
    <span class="label"><a class="link" {ext('https://joeyzhao.cc')}>joeyzhao.cc</a> · <a class="link" {ext('https://finfold.app')}>Finfold</a> · <a class="link" {ext('https://billvampire.com')}>BillVampire</a> · <a class="link" {ext('https://github.com/joeymilano')}>GitHub</a></span>
    <span class="label" data-clock>SHA 00:00 GMT+8</span>
  </div></div>
</footer>
{dialog()}
<script src="/assets/site/site.js?v={VER}" defer></script>
</body>
</html>
"""


def dialog():
    def pane(key, dot, label, title, body, subject):
        mail = f"mailto:{EMAIL}?subject={html.escape(subject)}"
        back = "← 换一个方向" if zh() else "← Choose another"
        return f"""
  <div class="c-body" data-pane="{key}" hidden style="--accent:var(--{key})">
    <p class="label" style="display:flex;gap:10px;align-items:center;margin-bottom:14px"><span class="dot {dot}"></span>{label}</p>
    <h2>{title}</h2>
    <div class="c-detail">
      <img src="/assets/site/img/wechat-qr-code.png" width="150" height="150" alt="{'微信二维码' if zh() else 'WeChat QR code'}" loading="lazy">
      <div>
        <p>{body}</p>
        <div class="c-links">
          <a href="{mail}"><span>Email</span><span class="muted">{EMAIL}</span></a>
          <a {ext(XHS, 'xiaohongshu')}><span>{'小红书' if zh() else 'Xiaohongshu'}</span><span>↗</span></a>
          <a {ext(SHOP, 'taobao-shop')}><span>{'淘宝店铺 · 旺旺客服' if zh() else 'Taobao shop'}</span><span>↗</span></a>
        </div>
      </div>
    </div>
    <button class="c-back" data-go="choose">{back}</button>
  </div>"""

    s = pane("studio", "s", "PRODUCT STUDIO", "聊聊你的产品" if zh() else "Tell us about your product",
             "微信扫码，发来一句话需求：做什么、给谁用、希望何时上线。我们会给出可行方案与报价区间。" if zh()
             else "Scan to add us on WeChat, or email a one-line brief: what it is, who it's for, when it should launch. We'll reply with a plan and a price range.",
             "[产品工作室] 项目咨询" if zh() else "[Studio] Project enquiry")
    a = pane("academy", "a", "PORTFOLIO ACADEMY", "聊聊你的作品集" if zh() else "Tell us about your portfolio",
             "微信扫码，告诉我们你的专业方向、目标院校和截止时间。我们会先帮你评估现有素材。" if zh()
             else "Scan to add us on WeChat, or email your discipline, target schools and deadline. We'll start by reviewing what you already have.",
             "[作品集学院] 申请咨询" if zh() else "[Academy] Portfolio enquiry")
    return f"""<dialog id="consult" class="consult" aria-label="{'咨询' if zh() else 'Contact'}">
  <div class="c-top"><span class="label">1% Design Lab · {'咨询' if zh() else 'Contact'}</span><button class="c-x" aria-label="{'关闭' if zh() else 'Close'}">✕</button></div>
  <div class="c-body" data-pane="choose">
    <h2>{'你想聊哪件事？' if zh() else 'What are you working on?'}</h2>
    <div class="c-choices">
      <button class="pick" data-go="studio" style="--pc:var(--studio)"><span class="label"><span class="dot s"></span>{'产品工作室' if zh() else 'Product Studio'}</span><strong>{'我要做一个产品' if zh() else 'I want to build a product'} <span class="arr">→</span></strong></button>
      <button class="pick" data-go="academy" style="--pc:var(--academy)"><span class="label"><span class="dot a"></span>{'作品集学院' if zh() else 'Portfolio Academy'}</span><strong>{'我要准备作品集' if zh() else 'I need a portfolio'} <span class="arr">→</span></strong></button>
    </div>
  </div>{s}{a}
</dialog>"""


# ------------------------------------------------------------------ blocks

def sec_head(n, label, title_rows, lead=None, act=None, dot=True):
    d = '<span class="dot"></span>' if dot else ""
    lead_html = f'<p class="lead" data-reveal>{t(lead)}</p>' if lead else ""
    act_html = f'<div class="sec-act" data-reveal>{act}</div>' if act else ""
    return f"""<div class="sec-head">
      <p class="label">{d}[{n}] {label}</p>
      <h2 class="h2" data-lines>{lines(*[t(r) for r in title_rows])}</h2>
      {lead_html}{act_html}
    </div>"""


def stats(items):
    out = []
    for p, n, suf, label in items:
        n = t(n)
        dec = 1 if isinstance(n, float) else 0
        out.append(f'<div data-reveal><p class="stat-n">{p}<span data-count="{n}" data-dec="{dec}">{num_fmt(n)}</span><em>{e(suf)}</em></p><p class="stat-l">{e(label)}</p></div>')
    return "".join(out)


def work_img(slug, size="sm"):
    h = WORK_SIZE[slug]
    if size == "sm":
        return f"/assets/work/sm/{slug}.webp", 900, round(h * 900 / 1600)
    return f"/assets/work/{slug}.webp", 1600, h


def student(slug):
    for s, zt, et, cat in STUDENT_WORK:
        if s == slug:
            return dict(slug=s, title=zt if zh() else et, cat=cat)
    raise KeyError(slug)


def product(slug):
    return next(p for p in PRODUCTS if p["slug"] == slug)


def marquee():
    names = "".join(f"<span>{s[0]}</span>" for s in SCHOOLS)
    label = ("学员录取院校：" if zh() else "Where our students got in: ") + ", ".join(x[0] for x in SCHOOLS)
    return f'<div class="marquee" role="img" aria-label="{e(label)}"><div class="marquee-track" aria-hidden="true">{names}{names}</div></div>'


def price_list(services, biz):
    rows = []
    for i, s in enumerate(services, 1):
        price = f'¥{s["price"]}<small>起</small>' if zh() else f'<small>from</small> ¥{s["price"]}'
        tags = "".join(f'<span class="tag">{e(tg)}</span>' for tg in s["tags"])
        acts = []
        if s["detail"]:
            acts.append(f'<a class="btn btn-line" href="{t(s["detail"])}">{"查看详情" if zh() else "Details"} <span class="arr">→</span></a>')
        if s["tb"]:
            acts.append(f'<a class="btn btn-solid" {ext(TB + s["tb"], "taobao-" + s["tb"])}>{"淘宝下单" if zh() else "Order on Taobao"} <span class="arr">↗</span></a>')
        acts.append(f'<button class="btn btn-line" data-consult="{biz}" data-from="pricing">{"先聊聊" if zh() else "Ask first"}</button>')
        rows.append(f"""
      <details{' open' if i == 1 else ''}>
        <summary><span class="row-n">{i:02d}</span><span class="row-t">{e(s['name'])}</span><span class="p-desc">{e(s['desc'])}</span><span class="p-price">{price}</span><span class="p-x" aria-hidden="true"></span></summary>
        <div class="p-body"><div><p class="p-lead">{e(s['desc'])}</p><div class="caps" style="margin-top:0">{tags}</div><div class="p-acts">{''.join(acts)}</div></div></div>
      </details>""")
    note = ("起步价对应最小规模的需求，最终报价取决于范围与周期；淘宝下单与微信咨询享受同样的服务。" if zh()
            else "Starting prices cover the smallest scope; final quotes depend on scope and timeline. Taobao orders and direct enquiries get identical service.")
    return f'<div class="plist" data-reveal>{"".join(rows)}</div><p class="plist-note">{note}</p>'


def steps(items):
    out = []
    for i, (title, body) in enumerate(items, 1):
        out.append(f'<div class="step" data-reveal><p class="label mono">STEP {i:02d}</p><h3>{e(title)}</h3><p>{e(body)}</p></div>')
    return f'<div class="steps">{"".join(out)}</div>'


def quote(r, solo=False):
    mentor = f'{"导师" if zh() else "Mentor"} · {e(r["mentor"])}'
    read = "阅读案例" if zh() else "Read the case"
    return f"""<figure class="quote{' solo' if solo else ''}" data-reveal>
      <blockquote>{e(r['text'])}</blockquote>
      <footer><div><strong>{e(r['who'])}</strong><span>{e(r['result'])}</span><br><span class="label" style="display:inline-block;margin-top:6px">{mentor}</span></div><a class="link" href="{r['case']}">{read} <span class="arr">→</span></a></footer>
    </figure>"""


def resources(items):
    out = []
    for href, title, desc, kind in items:
        out.append(f'<a href="{href}" data-reveal><span class="label">{e(kind)}</span><h3>{e(title)}<span class="arr">↗</span></h3><p>{e(desc)}</p></a>')
    return f'<div class="res">{"".join(out)}</div>'


def cta(biz, n):
    if biz == "home":
        lead = B("不确定属于哪条业务？直接告诉我们你想做什么，我们来判断。", "Not sure which side you need? Tell us what you're making — we'll route it.")
        btns = f"""<button class="pick" data-consult="studio" data-from="cta" style="--pc:var(--studio)"><span class="label"><span class="dot s"></span>{'产品工作室' if zh() else 'Product Studio'}</span><strong>{'我要做产品' if zh() else 'Build a product'} <span class="arr">↗</span></strong></button>
        <button class="pick" data-consult="academy" data-from="cta" style="--pc:var(--academy)"><span class="label"><span class="dot a"></span>{'作品集学院' if zh() else 'Portfolio Academy'}</span><strong>{'我要准备作品集' if zh() else 'Prepare a portfolio'} <span class="arr">↗</span></strong></button>"""
    else:
        lead = (B("一句话需求就够了。做什么、给谁用、何时上线——剩下的我们来问。", "A one-line brief is enough. What, for whom, by when — we'll ask the rest.") if biz == "studio"
                else B("告诉我们你的专业、目标院校和截止时间。先评估，再决定。", "Your discipline, target schools and deadline. We assess first, then you decide."))
        btns = f"""<button class="btn btn-solid" data-consult="{biz}" data-from="cta">{'微信咨询' if zh() else 'WeChat'} <span class="arr">↗</span></button>
        <a class="btn btn-line" {ext(SHOP, 'taobao-shop')}>{'淘宝店铺' if zh() else 'Taobao shop'} <span class="arr">↗</span></a>
        <a class="btn btn-line" href="mailto:{EMAIL}">Email</a>"""
    return f"""
<section class="cta" id="contact">
  <div class="wrap">
    <p class="label" style="margin-bottom:28px;display:flex;gap:10px;align-items:center"><span class="dot"></span>[{n}] {'联系' if zh() else 'Contact'}</p>
    <button class="cta-big" data-consult data-from="cta-big">{'聊聊吧' if zh() else "Let's talk"}<span class="arr">↗</span></button>
    <div class="cta-row">
      <p class="lead" data-reveal>{e(lead)}</p>
      <div class="cta-btns" data-reveal>{btns}</div>
    </div>
  </div>
</section>"""


def org_ld():
    return {
        "@type": "Organization",
        "@id": f"{ORIGIN}/#organization",
        "name": "1%DesignLab 梦想管理局",
        "legalName": "上海光有序科技有限公司",
        "alternateName": ["1% Design Lab", "梦想管理局"],
        "url": ORIGIN,
        "logo": f"{ORIGIN}/logo.jpg",
        "email": EMAIL,
        "founder": {"@type": "Person", "@id": "https://joeyzhao.cc/#person", "name": "Joey Zhao", "url": "https://joeyzhao.cc"},
        "address": {"@type": "PostalAddress", "streetAddress": "北京东路668号裙楼 黄浦汇数智心城",
                    "addressLocality": "上海市", "addressRegion": "黄浦区", "addressCountry": "CN"},
        "knowsAbout": ["AI product design", "full-stack development", "industrial design", "brand identity", "portfolio design"],
    }


def service_ld(path, name, services):
    offers = [{"@type": "Offer", "priceCurrency": "CNY", "price": s["price"].replace(",", ""),
               "itemOffered": {"@type": "Service", "name": t(s["name"]), "description": t(s["desc"])}} for s in services]
    return {"@type": "Service", "@id": f"{ORIGIN}{pre()}{path}#service", "name": name,
            "provider": {"@id": f"{ORIGIN}/#organization"}, "areaServed": "CN",
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": name, "itemListElement": offers}}


def crumbs_ld(path, name):
    home = f"{ORIGIN}{pre()}/"
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "1% Design Lab", "item": home},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{ORIGIN}{pre()}{path}"}]}


# ------------------------------------------------------------------ pages

def page_home():
    p = pre()
    title = ("1% Design Lab 梦想管理局 — 产品工作室 × 作品集学院 | 上海" if zh()
             else "1% Design Lab — Product Studio × Portfolio Academy | Shanghai")
    desc = ("1% Design Lab 梦想管理局是上海的设计与工程团队：产品工作室为创业者交付 AI 应用开发、全栈开发、品牌与工业设计；作品集学院为艺术设计申请者提供留学作品集、博士研究计划、个展与求职辅导。成员来自硅谷、米兰理工、RCA 与伯克利。" if zh()
            else "1% Design Lab is a Shanghai design and engineering team. The Product Studio ships AI apps, full-stack builds, brands and industrial design for founders; the Portfolio Academy builds art and design portfolios, PhD proposals and exhibitions for applicants.")
    kw = "1% Design Lab,梦想管理局,AI产品开发,AI应用开发,全栈开发,品牌设计,工业设计,作品集设计,留学作品集,博士研究计划,上海设计工作室"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), {
        "@type": "WebSite", "@id": f"{ORIGIN}/#website", "name": "1% Design Lab", "url": ORIGIN,
        "inLanguage": ["zh-CN", "en"], "publisher": {"@id": f"{ORIGIN}/#organization"}}]}

    studio_imgs = ["finfold-live", "joeyzhao-live", "billvampire-live"]
    academy_imgs = ["e-motorcycle", "wearable-memory", "mars-research", "vehicle-lighting"]

    def door_media(imgs, kind):
        out = []
        for i, im in enumerate(imgs):
            if kind == "s":
                src, srcset = f"/assets/site/img/{im}.webp", ""
            else:
                src = f"/assets/work/sm/{im}.webp"
                srcset = f' srcset="/assets/work/sm/{im}.webp 900w, /assets/work/{im}.webp 1600w" sizes="(max-width:860px) 100vw, 62vw"'
            lazy = ' fetchpriority="high"' if i == 0 else ' loading="lazy"'
            cls = " ".join(c for c in ["is-on" if i == 0 else "", "crop-top" if im == "wearable-memory" else ""] if c)
            cls = f' class="{cls}"' if cls else ""
            out.append(f'<img{cls} src="{src}"{srcset} alt=""{lazy} decoding="async">')
        return "".join(out)

    def tags(items):
        return "".join(f'<span class="tag">{x}</span>' for x in items)

    doors = f"""
  <div class="doors">
    <a class="door" href="{p}/studio/" style="--accent:var(--studio)">
      <div class="door-media framed" aria-hidden="true">{door_media(studio_imgs, 's')}</div>
      <div class="door-top"><span class="label"><span class="dot s"></span>&nbsp; [A] Product Studio</span><span class="door-count">01 / 03</span></div>
      <div>
        <p class="door-for">{'给创业者与企业' if zh() else 'For founders and companies'}</p>
        <h2>{'产品设计与开发' if zh() else 'Product & Engineering'}<span class="arr">↗</span></h2>
        <div class="door-tags">{tags(['AI 应用' if zh() else 'AI apps', 'Full-stack', 'Brand' if not zh() else '品牌 VI', '3D' if not zh() else '工业 / 3D'])}</div>
      </div>
    </a>
    <a class="door" href="{p}/academy/" style="--accent:var(--academy)">
      <div class="door-media" aria-hidden="true">{door_media(academy_imgs, 'a')}</div>
      <div class="door-top"><span class="label"><span class="dot a"></span>&nbsp; [B] Portfolio Academy</span><span class="door-count">01 / 04</span></div>
      <div>
        <p class="door-for">{'给艺术设计申请者' if zh() else 'For art and design applicants'}</p>
        <h2>{'艺术设计作品集' if zh() else 'Design Portfolios'}<span class="arr">↗</span></h2>
        <div class="door-tags">{tags(['作品集', '作业辅导', '博士 RP', '个展'] if zh() else ['Portfolio', 'Coursework', 'PhD RP', 'Exhibitions'])}</div>
      </div>
    </a>
  </div>"""

    hero = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-meta label">
      <span><span class="dot"></span>Shanghai 31.23°N 121.47°E</span>
      <span>Est. 2020</span>
      <span>{'产品工作室 × 作品集学院' if zh() else 'Product Studio × Portfolio Academy'}</span>
    </div>
    <div class="hero-row">
      <h1 class="display hero-now" data-lines>{lines('只做那 1%。') if zh() else lines('Only the 1%.')}</h1>
      <p class="lead" data-reveal>{'一支设计与工程团队。<strong>为创业者把产品做上线，为申请者把作品集做出来。</strong>' if zh() else 'One design and engineering team. <strong>We ship products for founders, and build portfolios for applicants.</strong>'}</p>
    </div>
  </div>
  {doors}
</section>
<section class="proof" aria-label="{'数据' if zh() else 'Numbers'}">
  <div style="--accent:var(--studio)"><p class="label"><span class="dot s"></span>Product Studio</p>{stats(STUDIO_STATS)}</div>
  <div style="--accent:var(--academy)"><p class="label"><span class="dot a"></span>Portfolio Academy</p>{stats(ACADEMY_STATS)}</div>
</section>
{marquee()}"""

    # selected work index
    rows = []
    idx = [("p", "finfold"), ("a", "wearable-memory"), ("p", "billvampire"), ("a", "e-motorcycle"),
           ("a", "mars-research"), ("p", "joeyzhao"), ("a", "dance-video-app"), ("a", "zeon-identity")]
    for i, (kind, slug) in enumerate(idx, 1):
        if kind == "p":
            pr = product(slug)
            rows.append(f'<a class="row" data-k="s" data-b="s" data-img="/assets/site/img/{pr["img"]}.webp" {ext(pr["url"], pr["name"])}>'
                        f'<span class="row-n">{i:02d}</span><span class="row-t">{pr["name"]}</span><span class="row-c">{e(pr["cat"])}</span>'
                        f'<span class="row-b"><span class="dot s"></span>{"工作室 · 自研" if zh() else "Studio"}</span><span class="row-y">{pr["year"]}</span><span class="row-a">↗</span></a>')
        else:
            w = student(slug)
            rows.append(f'<a class="row" data-k="a" data-b="a" data-img="{work_img(slug)[0]}" href="{p}/academy/#gallery">'
                        f'<span class="row-n">{i:02d}</span><span class="row-t">{e(w["title"])}</span><span class="row-c">{e(CATS[w["cat"]])}</span>'
                        f'<span class="row-b"><span class="dot a"></span>{"学院 · 学员" if zh() else "Academy"}</span><span class="row-y">{"作品集" if zh() else "Student"}</span><span class="row-a">↗</span></a>')

    def tile(kind, slug, cls):
        if kind == "p":
            pr = product(slug)
            return (f'<a class="tile {cls}" {ext(pr["url"], pr["name"])} data-reveal><div class="tile-m" style="--r:{pr["w"]}/{pr["h"]}">'
                    f'<img src="/assets/site/img/{pr["img"]}.webp" width="{pr["w"]}" height="{pr["h"]}" alt="{pr["name"]}" loading="lazy" decoding="async"></div>'
                    f'<div class="tile-cap"><h3>{pr["name"]} — {e(pr["cat"])}</h3><span class="label"><span class="dot s"></span>{"自研产品" if zh() else "Own product"}</span></div></a>')
        w = student(slug)
        src, iw, ih = work_img(slug)
        return (f'<a class="tile {cls}" href="{p}/academy/#gallery" data-reveal><div class="tile-m" style="--r:{iw}/{ih}">'
                f'<img src="{src}" width="{iw}" height="{ih}" alt="{e(w["title"])}" loading="lazy" decoding="async"></div>'
                f'<div class="tile-cap"><h3>{e(w["title"])}</h3><span class="label"><span class="dot a"></span>{"学员作品" if zh() else "Student work"} · {e(CATS[w["cat"]])}</span></div></a>')

    mosaic = "".join([
        tile("p", "finfold", "w7"), tile("a", "wearable-memory", "w5 push"),
        tile("a", "mars-research", "w5"), tile("p", "joeyzhao", "w7 push"),
        tile("p", "billvampire", "w6"), tile("a", "e-motorcycle", "w6 push"),
    ])

    tabs = (f'<div class="tabs" data-filter="#work-index" role="group" aria-label="{"筛选" if zh() else "Filter"}">'
            f'<button data-f="all" aria-pressed="true">{"全部" if zh() else "All"}</button>'
            f'<button data-f="s" aria-pressed="false"><span class="dot s"></span>{"产品工作室" if zh() else "Studio"}</button>'
            f'<button data-f="a" aria-pressed="false"><span class="dot a"></span>{"作品集学院" if zh() else "Academy"}</button></div>')

    work = f"""
<section class="sec" id="work">
  <div class="wrap">
    {sec_head('01', 'Selected work', [B('两条业务，', 'Two practices,'), B('同一套标准。', 'one standard.')],
              B('左边是我们自己设计、开发、上线的产品；右边是学员在导师带领下完成的作品集项目。', 'Products we designed, built and shipped ourselves — alongside portfolio projects our students made with their mentors.'))}
    {tabs}
    <div class="index" id="work-index">{''.join(rows)}</div>
    <div class="mosaic">{mosaic}</div>
  </div>
  <div class="peek" aria-hidden="true"><img alt=""></div>
</section>"""

    manifesto = f"""
<section class="sec sec-t">
  <div class="wrap">
    <p class="label" style="margin-bottom:40px;display:flex;gap:10px;align-items:center"><span class="dot"></span>[02] {'为什么是一个团队' if zh() else 'Why one team'}</p>
    <p class="manifesto" data-manifesto>{'做产品的人教作品集，教作品集的人做产品。同一双眼睛，两种交付：一个<span class="hl" style="--hl:var(--studio)">上线的产品</span>，一份<span class="hl" style="--hl:var(--academy)">被记住的作品集</span>。' if zh()
     else 'The people who ship products teach portfolios. The people who teach portfolios ship products. Same eye, two deliverables: a <span class="hl" style="--hl:var(--studio)">product that goes live</span>, and a <span class="hl" style="--hl:var(--academy)">portfolio that gets remembered.</span>'}</p>
  </div>
</section>"""

    ppl = []
    for person in PEOPLE:
        dots = "".join(f'<span class="dot {d}"></span>' for d in person["biz"])
        ppl.append(f"""<div class="person" data-reveal>
        <div class="person-m"><img src="/assets/site/img/{person['img']}.webp" alt="{e(person['name'])}" loading="lazy" decoding="async"></div>
        <h3>{e(person['name'])}<span>{dots}</span></h3>
        <p>{e(person['role'])}</p>
        <small>{e(person['edu'])}<br>{e(person['note'])}</small>
      </div>""")
    people = f"""
<section class="sec" id="people">
  <div class="wrap">
    {sec_head('03', 'People', [B('硅谷、米兰、奥斯陆、', 'Silicon Valley, Milan, Oslo,'), B('格拉斯哥、伯克利。', 'Glasgow, Berkeley.')],
              B('核心成员来自米兰理工、RCA、奥斯陆建筑与设计学院、格拉斯哥大学与 UC Berkeley，兼具大厂产品经验与独立上线的能力。圆点表示每个人主要负责的业务。', 'Core members trained at Politecnico di Milano, RCA, AHO Oslo, Glasgow and UC Berkeley — with big-tech product experience and the ability to ship independently. Dots mark which practice each person leads in.'))}
    <div class="people">{''.join(ppl)}</div>
  </div>
</section>"""

    wide = ' class="wide"'
    office_imgs = "".join(
        f'<img src="/assets/site/img/office-{i}.webp" width="{1200 if i == 6 else 675}" height="900" alt="{"上海工作室" if zh() else "Shanghai studio"} {i}" loading="lazy" decoding="async"{wide if i == 6 else ""} draggable="false">'
        for i in (6, 1, 2, 3, 4, 5))
    office = f"""
<section class="sec sec-t">
  <div class="wrap">
    <div class="office">
      <div class="office-txt" data-reveal>
        <p class="label" style="display:flex;gap:10px;align-items:center"><span class="dot"></span>[04] {'上海工作室' if zh() else 'The studio'}</p>
        <h2 class="h3" style="margin-top:28px">{'在外滩旁边，做能被握在手里的东西。' if zh() else 'A few streets from the Bund, making things you can hold.'}</h2>
        <address>{'上海市黄浦区北京东路 668 号裙楼<br>黄浦汇数智心城' if zh() else '668 East Beijing Road, Huangpu<br>Shanghai, China'}</address>
        <p class="muted" style="margin-top:18px;font-size:14px">{'自有原型工坊：3D 建模、3D 打印、智能穿戴与互动装置。欢迎预约到访。' if zh() else 'In-house prototyping: 3D modelling, 3D printing, wearables and interactive installations. Visits by appointment.'}</p>
      </div>
      <div class="strip" aria-label="{'工作室照片' if zh() else 'Studio photos'}">{office_imgs}</div>
    </div>
  </div>
</section>"""

    body = hero + work + manifesto + people + office + cta("home", "05")
    return head("/", "home", title, desc, kw, "og-home", ld) + header("/", "home") + body + footer()


def sub_hero(biz, name, h1_rows, lead, stat_items, caps):
    p = pre()
    dot = "s" if biz == "studio" else "a"
    btn = (B("聊聊你的产品", "Talk about your product") if biz == "studio" else B("聊聊你的作品集", "Talk about your portfolio"))
    jump = (f'<a class="btn btn-line" href="#work">{"看作品" if zh() else "See work"} <span class="arr">↓</span></a>' if biz == "studio"
            else f'<a class="btn btn-line" href="#gallery">{"看学员作品" if zh() else "Student work"} <span class="arr">↓</span></a>')
    other = (f'{p}/academy/', B('作品集学院', 'Portfolio Academy'), 'a') if biz == "studio" else (f'{p}/studio/', B('产品工作室', 'Product Studio'), 's')
    return f"""
<section class="sub-hero">
  <div class="wrap">
    <div class="crumb label"><a href="{p}/">1% Design Lab</a><span>/</span><span class="dot {dot}"></span><b>{e(name)}</b><span class="crumb-x">{'另一条业务' if zh() else 'Other practice'} → <a href="{other[0]}"><span class="dot {other[2]}"></span> {e(other[1])}</a></span></div>
    <h1 class="display hero-now" data-lines>{lines(*[t(r) for r in h1_rows])}</h1>
    <div class="sub-hero-g">
      <p class="lead">{t(lead)}</p>
      <div></div>
      <div class="acts" data-reveal><button class="btn btn-solid" data-consult="{biz}" data-from="hero">{e(btn)} <span class="arr">↗</span></button>{jump}</div>
      <div class="caps" style="grid-column:1/-1">{''.join(f'<span class="tag">{e(c)}</span>' for c in caps)}</div>
      <div class="stat-row">{stats(stat_items)}</div>
    </div>
  </div>
</section>"""


def page_studio():
    title = ("产品工作室 — AI 应用开发 · 全栈开发 · 品牌 VI · 工业设计 | 1% Design Lab" if zh()
             else "Product Studio — AI apps, full-stack, Brand & Industrial Design | 1% Design Lab")
    desc = ("1% Design Lab 产品工作室为创业者与企业把想法做成上线的产品：AI 应用开发 14 天交付（¥5,000 起），产品设计与全栈开发、LOGO 品牌 VI、工业设计与 3D 渲染。团队拥有硅谷大厂经验，独立上线 Finfold、BillVampire 等产品。" if zh()
            else "The 1% Design Lab Product Studio turns ideas into shipped products for founders: AI apps in 14 days from ¥5,000, product design and full-stack builds, brand identity, industrial design and 3D. Built by the team behind Finfold and BillVampire.")
    kw = "AI应用开发,AI产品开发,14天上线,全栈开发,产品设计,UI设计,小程序开发,官网开发,LOGO设计,VI设计,工业设计,3D建模渲染,上海产品工作室"
    name = "产品工作室" if zh() else "Product Studio"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), crumbs_ld("/studio/", name), service_ld("/studio/", name, STUDIO_SERVICES)]}

    hero = sub_hero("studio", name, [B("把想法，", "From idea"), B("做成上线的产品。", "to shipped product.")],
                    B("我们是设计师，也是工程师。从产品逻辑、界面、前后端到部署上线，<strong>一个团队从头负责到尾</strong>——不外包，不转手。",
                      "We're designers and engineers. Product logic, interface, front and back end, deployment — <strong>one team, start to finish</strong>. No hand-offs, no outsourcing."),
                    STUDIO_STATS,
                    [B("AI 产品", "AI products"), "SaaS", B("小程序", "Mini-programs"), B("官网", "Websites"), B("品牌 VI", "Identity"), B("工业设计 / 3D", "Industrial / 3D")])

    tl = [("Day 1–2", B("产品逻辑梳理", "Product logic")), ("Day 3–5", B("UI/UX 设计", "UI/UX design")),
          ("Day 6–10", B("前端开发", "Frontend build")), ("Day 11–12", B("API 与后端对接", "API & backend")),
          ("Day 13–14", B("部署与交付", "Deploy & hand-off"))]
    timeline = "".join(f'<div><span class="label mono">{d}</span><b>{e(x)}</b></div>' for d, x in tl)
    feature = f"""
<section class="sec sec-t">
  <div class="wrap">
    <div class="feature" data-reveal>
      <div class="feature-l">
        <p class="label" style="display:flex;gap:10px;align-items:center"><span class="dot"></span>[01] {'主打服务' if zh() else 'Flagship'}</p>
        <h2 class="h2">{'AI 应用开发，<br>14 天上线。' if zh() else 'AI app development,<br>live in 14 days.'}</h2>
        <p class="lead" style="font-size:17px">{'为验证想法的创业者设计：先把最小可用的产品做出来，放到真实用户面前。产品逻辑、设计、前端、API 集成与部署一次交付。' if zh() else 'Built for founders validating an idea: get the smallest useful product in front of real users. Logic, design, frontend, API integration and deployment in one delivery.'}</p>
      </div>
      <div class="feature-r">
        <div><p class="label">{'起步价' if zh() else 'From'}</p><p class="price" style="margin-top:14px">¥5,000{'<small>起</small>' if zh() else ''}</p></div>
        <div class="p-acts"><a class="btn btn-solid" href="/services/ai-app-development">{'查看详情' if zh() else 'Details'} <span class="arr">→</span></a><button class="btn btn-line" data-consult="studio" data-from="mvp">{'预约咨询' if zh() else 'Book a call'}</button></div>
      </div>
      <div class="timeline">{timeline}</div>
    </div>
  </div>
</section>"""

    projs = []
    for pr, cls in ((product("finfold"), "big"), (product("billvampire"), ""), (product("joeyzhao"), "")):
        projs.append(f"""<a class="proj {cls}" {ext(pr['url'], pr['name'])} data-reveal>
        <div class="tile-m"><img src="/assets/site/img/{pr['img']}.webp" width="{pr['w']}" height="{pr['h']}" alt="{pr['name']}" loading="lazy" decoding="async"></div>
        <div class="proj-cap"><h3>{pr['name']}<span class="arr">↗</span></h3><p>{e(pr['desc'])}</p><span class="label">{e(pr['cat'])} · {pr['year']}</span></div>
      </a>""")
    credit_rows = "".join(
        f'<div class="row"><span class="row-t">{e(n)}</span><span class="row-c">{e(c)}</span><span class="row-b">{e(r)}</span></div>'
        for n, c, r in CREDITS)
    work = f"""
<section class="sec" id="work">
  <div class="wrap">
    {sec_head('02', 'Selected work', [B('我们自己也做产品，', 'We ship our own products,'), B('而且真的上线了。', 'and they are live.')],
              B('同样的全栈交付能力，也用在你的项目上。', 'The same end-to-end capability goes into yours.'))}
    <div class="projects">{''.join(projs)}</div>
    <div class="credits">
      <p class="label" style="padding:22px 0 6px">{'团队成员履历 · Selected credits' if zh() else 'Team credits'}</p>
      {credit_rows}
    </div>
    <p class="credits-note">{'以上为团队成员在任职或独立期间主导的项目，并非工作室客户案例。' if zh() else 'Projects led by team members in previous roles or independently — not studio client work.'}</p>
  </div>
</section>"""

    services = f"""
<section class="sec sec-t" id="services">
  <div class="wrap">
    {sec_head('03', 'Services & pricing', [B('服务与价格。', 'Services & pricing.')],
              B('明码标价，从小需求到完整产品都可以接。点开每一行看详情，或直接在淘宝下单。', 'Transparent starting prices, from small jobs to full products. Open a row for details, or order directly on Taobao.'))}
    {price_list(STUDIO_SERVICES, 'studio')}
  </div>
</section>"""

    process = f"""
<section class="sec sec-t">
  <div class="wrap">
    {sec_head('04', 'Process', [B('五步，从一句话到上线。', 'Five steps, from one line to launch.')])}
    {steps(STUDIO_STEPS)}
  </div>
</section>
<section class="sec sec-t">
  <div class="wrap">
    <p class="label" style="margin-bottom:28px;display:flex;gap:10px;align-items:center"><span class="dot"></span>[05] {'客户怎么说' if zh() else 'Client words'}</p>
    <div class="quotes">{quote(BRAND_REVIEW, solo=True)}</div>
  </div>
</section>
<section class="sec sec-t">
  <div class="wrap">
    {sec_head('06', 'Resources', [B('免费工具与文章。', 'Free tools & notes.')])}
    {resources(STUDIO_RES)}
  </div>
</section>"""

    body = hero + feature + work + services + process + cta("studio", "07")
    return head("/studio/", "studio", title, desc, kw, "og-studio", ld) + header("/studio/", "studio") + body + footer()


def page_academy():
    title = ("作品集学院 — 艺术设计留学作品集 · 博士研究计划 · 个展 · 求职 | 1% Design Lab" if zh()
             else "Portfolio Academy — Art & Design Portfolios, PhD Proposals, Exhibitions | 1% Design Lab")
    desc = ("1% Design Lab 作品集学院专注艺术设计留学作品集 6 年：产品、交互、建筑、景观、服装作品集原创设计，留学生作业辅导，博士研究计划，上海线下个展与设计师求职。导师来自米兰理工、RCA、格拉斯哥与伯克利，学员录取 RCA、UCL、哥大、宾大等院校。" if zh()
            else "The 1% Design Lab Portfolio Academy has mentored art and design applicants for 6 years: product, interaction, architecture and fashion portfolios, coursework, PhD proposals and exhibitions. Mentors from PoliMi, RCA, Glasgow and Berkeley; students admitted to RCA, UCL, Columbia and UPenn.")
    kw = "作品集,留学作品集,艺术留学,设计作品集,建筑作品集,交互设计作品集,工业设计作品集,博士研究计划,RP写作,作品集辅导,留学生作业辅导,上海作品集机构"
    name = "作品集学院" if zh() else "Portfolio Academy"
    ld = {"@context": "https://schema.org", "@graph": [org_ld(), crumbs_ld("/academy/", name), service_ld("/academy/", name, ACADEMY_SERVICES)]}

    hero = sub_hero("academy", name, [B("让招生官，", "Make admissions"), B("记住你的作品。", "remember your work.")],
                    B("不套模板。导师从你自己的经历里提炼叙事，<strong>把每个项目讲成一个值得被记住的故事</strong>——然后在排版的每一个像素上较真。",
                      "No templates. Mentors draw the narrative out of your own experience, <strong>turning each project into a story worth remembering</strong> — then obsess over every pixel of the layout."),
                    ACADEMY_STATS,
                    [B("产品 / 工业", "Product"), B("交互", "Interaction"), B("建筑 / 景观", "Architecture"), B("服装", "Fashion"), B("视觉 / 媒体", "Visual"), B("博士 RP", "PhD RP")])

    wall = "".join(f'<div class="school" data-reveal><b>{s}</b><span>{full}<i>{city.upper()}</i></span></div>' for s, full, city in SCHOOLS)
    schools = f"""
<section class="sec sec-t">
  <div class="wrap">
    {sec_head('01', 'Admissions', [B('学员去了这些地方。', 'Where our students went.')],
              B('600+ 份名校 Offer，覆盖英、美、欧、港、澳的设计、建筑与时尚院校。', '600+ offers across design, architecture and fashion schools in the UK, US, Europe, Hong Kong and Australia.'))}
    <div class="schools">{wall}</div>
  </div>
</section>"""

    counts = {}
    for _, _, _, c in STUDENT_WORK:
        counts[c] = counts.get(c, 0) + 1
    tabs = (f'<div class="tabs" data-filter="#gallery-grid" role="group" aria-label="{"筛选" if zh() else "Filter"}">'
            f'<button data-f="all" aria-pressed="true">{"全部" if zh() else "All"}<sup>{len(STUDENT_WORK)}</sup></button>'
            + "".join(f'<button data-f="{k}" aria-pressed="false">{e(v)}<sup>{counts[k]}</sup></button>' for k, v in CATS.items())
            + "</div>")
    items = []
    for slug, zt, et, cat in STUDENT_WORK:
        title_ = zt if zh() else et
        src, iw, ih = work_img(slug)
        full = work_img(slug, "full")[0]
        items.append(f"""<button class="g-item" data-k="{cat}" data-src="{full}" data-title="{e(title_)}" data-cat="{e(CATS[cat])}" data-reveal>
        <div class="tile-m"><img src="{src}" width="{iw}" height="{ih}" alt="{e(title_)}" loading="lazy" decoding="async"></div>
        <div class="tile-cap"><h3>{e(title_)}</h3><span class="label">{e(CATS[cat])}</span></div>
      </button>""")
    archive = "".join(
        f'<a {ext(f"/assets/site/img/portfolio-{i}.webp")}><img src="/assets/site/img/portfolio-{i}-sm.webp" width="480" height="1152" alt="{"作品集长图" if zh() else "Portfolio sheet"} {i}" loading="lazy"></a>'
        for i in range(1, 6))
    gallery = f"""
<section class="sec" id="gallery">
  <div class="wrap">
    {sec_head('02', 'Student work', [B('学员作品。', 'Student work.')],
              B('以下为学员在导师辅导下完成的作品集项目，作品版权归学员本人所有。点击查看大图。', 'Portfolio projects completed by students with their mentors. All rights belong to the students. Click to enlarge.'))}
    {tabs}
    <div class="gallery" id="gallery-grid">{''.join(items)}</div>
    <details class="archive">
      <summary><span>{'查看完整作品集长图' if zh() else 'Full portfolio sheets'} <span class="label">(5)</span></span><span class="arr">↓</span></summary>
      <div class="archive-g">{archive}</div>
    </details>
  </div>
  <div class="lb" role="dialog" aria-modal="true" aria-label="{'作品预览' if zh() else 'Preview'}">
    <button class="lb-x" aria-label="{'关闭' if zh() else 'Close'}">✕</button>
    <img alt="">
    <div class="lb-bar"><div><h3></h3><p class="label lb-n"></p></div><div class="lb-nav"><button data-prev aria-label="{'上一张' if zh() else 'Previous'}">←</button><button data-next aria-label="{'下一张' if zh() else 'Next'}">→</button></div></div>
  </div>
</section>"""

    order = ["xue", "jackie", "cheng", "jason", "joey"]
    mentors = []
    for key in order:
        person = next(x for x in PEOPLE if x["key"] == key)
        tags = "".join(f'<span class="tag">{tg}</span>' for tg in MENTOR_TAGS[key])
        mentors.append(f"""<div class="mentor" data-reveal>
        <div class="mentor-m"><img src="/assets/site/img/{person['img']}.webp" alt="{e(person['name'])}" loading="lazy" decoding="async"></div>
        <div class="mentor-h"><h3>{e(person['name'])}</h3><p>{e(person['role'])}</p><p class="label" style="margin-top:14px">{e(person['edu'])}</p></div>
        <p class="mentor-b">{e(MENTOR_BIO[key])}</p>
        <div class="mentor-t">{tags}</div>
      </div>""")
    mentors_sec = f"""
<section class="sec sec-t" id="mentors">
  <div class="wrap">
    {sec_head('03', 'Mentors', [B('导师自己，', 'Mentors who went'), B('就是从这些学校出来的。', 'to these schools themselves.')],
              B('每位学员按专业方向匹配导师，一对一推进。', 'Every student is matched to a mentor by discipline and works one-to-one.'))}
    <div class="mentors">{''.join(mentors)}</div>
  </div>
</section>"""

    services = f"""
<section class="sec sec-t" id="services">
  <div class="wrap">
    {sec_head('04', 'Services & pricing', [B('服务与价格。', 'Services & pricing.')],
              B('从作品集到博士研究计划、个展与求职。点开每一行看详情，或直接在淘宝下单。', 'From portfolios to PhD proposals, exhibitions and careers. Open a row for details, or order directly on Taobao.'))}
    {price_list(ACADEMY_SERVICES, 'academy')}
  </div>
</section>"""

    next_card = f"""<figure class="quote" data-reveal style="justify-content:space-between">
      <blockquote style="font-size:clamp(26px,2.6vw,40px);letter-spacing:-.03em;line-height:1.2">{'下一个故事，<br>是你的。' if zh() else 'The next story<br>is yours.'}</blockquote>
      <footer><span class="label">{'申请季名额有限' if zh() else 'Limited places each cycle'}</span><button class="btn btn-solid" data-consult="academy" data-from="stories">{'聊聊你的作品集' if zh() else 'Talk to us'} <span class="arr">↗</span></button></footer>
    </figure>"""
    stories = f"""
<section class="sec sec-t" id="stories">
  <div class="wrap">
    {sec_head('05', 'Stories', [B('录取故事。', 'Admission stories.')],
              B('来自真实学员的反馈。每一个 offer 背后，都是几个月的反复打磨。', 'In our students’ words. Behind every offer are months of revision.'))}
    <div class="quotes">{''.join(quote(r) for r in REVIEWS)}{next_card}</div>
  </div>
</section>
<section class="sec sec-t">
  <div class="wrap">
    {sec_head('06', 'Tools & guides', [B('免费工具与申请指南。', 'Free tools & guides.')])}
    {resources(ACADEMY_RES)}
  </div>
</section>
<section class="sec sec-t">
  <div class="wrap">
    {sec_head('07', 'Process', [B('五步，从第一次聊天到网申提交。', 'Five steps, from first chat to submission.')])}
    {steps(ACADEMY_STEPS)}
  </div>
</section>"""

    body = hero + schools + gallery + mentors_sec + services + stories + cta("academy", "08")
    return head("/academy/", "academy", title, desc, kw, "og-academy", ld) + header("/academy/", "academy") + body + footer()


def build():
    global LANG
    pages = [("index.html", page_home), ("studio/index.html", page_studio), ("academy/index.html", page_academy)]
    for lang in ("zh", "en"):
        LANG = lang
        for rel, fn in pages:
            out = ROOT / ("en/" + rel if lang == "en" else rel)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(fn(), encoding="utf-8")
            print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()
