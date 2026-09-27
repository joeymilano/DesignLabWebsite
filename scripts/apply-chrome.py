"""Put the new global header, footer and consult dialog on the older subpages.

The markup comes from build-site.py so the chrome matches the brand pages exactly;
assets/site/chrome.css styles it without touching each page's own styles.
Idempotent: injected blocks sit between <!--dl:*--> markers and are replaced on re-run.
Run: python3 scripts/apply-chrome.py
"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("build_site", ROOT / "scripts" / "build-site.py")
bs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bs)

STUDIO = {"services/ai-mvp.html", "services/logo-branding.html", "services/industrial-design.html",
          "tools/landing-page-audit.html", "cases/branding-fashion.html"}
STUDIO_TOPICS = {"blog/ai-agent-mvp-guide.html", "blog/ai-app-builder-vs-custom-development.html",
                 "blog/vibe-coding-to-production.html"}
NEUTRAL = {"blog/design-agency-how-to-choose.html", "blog/index.html", "tools/index.html",
           "careers/index.html", "en/careers/index.html"}
# language twins; pages without one switch to the other language's home
TWINS = {"careers/index.html": "/en/careers/", "en/careers/index.html": "/careers/",
         "services/portfolio-design.html": "/en/design-portfolio/",
         "en/design-portfolio/index.html": "/services/portfolio-design"}
# pages whose content starts too close to the top once their old sticky bar is gone
PAD_TOP = {"blog/index.html", "tools/index.html", "careers/index.html", "en/careers/index.html"}
# pages that translate themselves client-side via switchLang()
JS_LANG = {"blog/index.html", "tools/index.html"}

MARK = re.compile(r"\s*<!--dl:(head|hdr|ftr)-->.*?<!--/dl:\1-->", re.S)


def pages():
    for d in ("services", "cases", "blog", "tools"):
        yield from sorted(str(p.relative_to(ROOT)) for p in (ROOT / d).glob("*.html"))
    yield from ("careers/index.html", "portfolio/index.html", "en/careers/index.html", "en/design-portfolio/index.html")


def config(rel):
    lang = "en" if rel.startswith("en/") else "zh"
    if rel in STUDIO:
        biz, cur, consult = "studio", "studio", "studio"
    elif rel in NEUTRAL:
        biz, cur, consult = "home", "blog" if rel.startswith("blog/") else None, ""
    elif rel in STUDIO_TOPICS:
        biz, cur, consult = "home", "blog", "studio"
    elif rel.startswith("blog/"):
        biz, cur, consult = "home", "blog", "academy"
    else:
        biz, cur, consult = "academy", "academy", "academy"
    return lang, biz, cur, consult


def lang_switch(rel, lang):
    if rel in JS_LANG:
        return ('<button data-lang="zh" aria-current="true" onclick="switchLang(\'zh\')">中</button> / '
                '<button data-lang="en" onclick="switchLang(\'en\')">EN</button>')
    other = TWINS.get(rel, "/" if lang == "en" else "/en/")
    if lang == "zh":
        return f'<span aria-current="true">中</span> / <a href="{other}" hreflang="en">EN</a>'
    return f'<a href="{other}" hreflang="zh-CN">中</a> / <span aria-current="true">EN</span>'


def chrome(rel):
    lang, biz, cur, _ = config(rel)
    bs.LANG = lang
    hdr = bs.header("/", cur).replace('<main id="main">', "").strip()
    hdr = re.sub(r'<span class="lang">.*?</span>(?=\s*<(?:button|/div))',
                 lambda m: f'<span class="lang">{lang_switch(rel, lang)}</span>', hdr)
    hdr = hdr.replace('<header class="hdr">', '<header class="hdr dl-c">').replace('<nav class="mnav"', '<nav class="mnav dl-c"')
    ftr = bs.footer()
    ftr = ftr[ftr.index('<footer class="ftr">'):ftr.index("</body>")].strip()
    ftr = ftr.replace('<footer class="ftr">', '<footer class="ftr dl-c">').replace('class="consult"', 'class="consult dl-c"')
    return lang, biz, hdr, ftr


def old_footer(m):
    """Keep page-specific disclaimers from article/tool footers; drop generic copyright lines."""
    cls, inner = m.group(1), m.group(2)
    if "©" not in inner and "&copy;" not in inner:
        return m.group(0)  # already reduced on a previous run
    note = re.search(r"(?:·|&middot;)\s*(.+?)\s*</p>", inner, re.S)
    if cls in ("article-footer", "tool-footer") and note and "设计服务" not in note.group(1):
        return f'<footer class="{cls}"><p>{note.group(1).strip()}</p></footer>'
    return ""


def apply(rel):
    path = ROOT / rel
    s = path.read_text(encoding="utf-8")
    s = MARK.sub("", s)
    lang, biz, hdr, ftr = chrome(rel)
    consult = config(rel)[3]

    # old top bars and their stylesheet
    s = re.sub(r'\s*<header class="(?:topbar|site-header)">.*?</header>', "", s, flags=re.S)
    s = re.sub(r'\s*<a class="skip-link"[^>]*>.*?</a>', "", s)
    s = re.sub(r'\s*<link rel="stylesheet" href="[./]*subpage-nav\.css[^"]*">', "", s)
    # old footers
    s = re.sub(r'<footer class="(page-footer|case-footer|tool-footer|article-footer|site-footer)">(.*?)</footer>',
               old_footer, s, flags=re.S)
    s = re.sub(r"\n\s*\n\s*\n", "\n\n", s)
    # contact CTAs open the shared dialog
    attr = f' data-consult="{consult}"' if consult else " data-consult"
    s = re.sub(r'(<a href="\.\./#contact")(?! data-consult)', r"\1" + attr + ' data-from="page"', s)
    s = s.replace('onclick="openWechatModal()"', attr.strip() + ' data-from="page"')
    if rel in JS_LANG:
        s = s.replace("document.getElementById('lang-zh').classList.toggle('active', lang === 'zh');",
                      "document.querySelectorAll('[data-lang]').forEach(b => b.toggleAttribute('aria-current', b.dataset.lang === lang));")
        s = s.replace("document.getElementById('lang-en').classList.toggle('active', lang === 'en');\n", "")

    # body attributes
    body = re.search(r"<body([^>]*)>", s)
    attrs = re.sub(r'\s*data-biz="[^"]*"', "", body.group(1))
    attrs = re.sub(r'\s*class="dl-pad"', "", attrs)
    attrs += f' data-biz="{biz}"' + (' class="dl-pad"' if rel in PAD_TOP else "")
    s = s[:body.start()] + f"<body{attrs}>" + s[body.end():]

    head = (f'\n    <!--dl:head--><link rel="preload" href="/assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="stylesheet" href="/assets/site/chrome.css?v={bs.VER}"><!--/dl:head-->')
    s = s.replace("</head>", head + "\n</head>", 1)
    body = re.search(r"<body[^>]*>", s)
    s = s[:body.end()] + f"\n<!--dl:hdr-->\n{hdr}\n<!--/dl:hdr-->" + s[body.end():]
    i = s.rindex("</body>")
    s = s[:i].rstrip() + f'\n<!--dl:ftr-->\n{ftr}\n<!--/dl:ftr-->\n' + s[i:]
    path.write_text(s, encoding="utf-8")
    print(f"{rel:52s} {lang} {biz}")


if __name__ == "__main__":
    for rel in pages():
        apply(rel)
