"""Render the 1200x630 share images in assets/share/ with the site's own type and colours.

Needs Playwright + Chrome (pip install playwright). Run: python3 scripts/build-og.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = (ROOT / "assets" / "fonts").as_uri()

CSS = f"""
@font-face{{font-family:Geist;src:url({FONTS}/Geist-Variable.woff2) format("woff2");font-weight:100 900}}
@font-face{{font-family:"Geist Mono";src:url({FONTS}/GeistMono-Variable.woff2) format("woff2");font-weight:100 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#0B0B0A;color:#EDEDE8;font-family:Geist,"PingFang SC",sans-serif;
  padding:56px 64px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden;position:relative}}
.mono{{font-family:"Geist Mono",monospace;font-size:17px;letter-spacing:.06em;text-transform:uppercase;color:#9A9A93;display:flex;gap:14px;align-items:center}}
.top{{display:flex;justify-content:space-between}}
.dot{{width:12px;height:12px;border-radius:50%;background:var(--c)}}
h1{{font-weight:500;font-size:112px;line-height:1.04;letter-spacing:-.035em}}
h1 em{{font-style:normal;color:var(--c)}}
.sub{{font-size:28px;color:#9A9A93;margin-top:22px;letter-spacing:-.01em}}
.rule{{position:absolute;left:0;right:0;bottom:0;height:8px;background:var(--c)}}
.split{{position:absolute;left:0;right:0;bottom:0;height:8px;display:flex}}
.split i{{flex:1}}
"""

PAGES = {
    "og-home": ("#EDEDE8", "SHANGHAI · EST. 2020", "只做那 1%。",
                "为创业者把产品做上线，为申请者把作品集做出来。",
                '<span class="dot" style="--c:#57FFC3"></span>PRODUCT STUDIO&nbsp;&nbsp;<span class="dot" style="--c:#FF4A2E"></span>PORTFOLIO ACADEMY',
                '<div class="split"><i style="background:#57FFC3"></i><i style="background:#FF4A2E"></i></div>'),
    "og-studio": ("#57FFC3", "[A] PRODUCT STUDIO", "把想法，做成<br><em>上线的产品。</em>",
                  "AI MVP · 全栈开发 · 品牌 VI · 工业设计 / 3D",
                  '<span class="dot"></span>14 天 AI MVP · ¥5,000 起', '<div class="rule"></div>'),
    "og-academy": ("#FF4A2E", "[B] PORTFOLIO ACADEMY", "让招生官，<br><em>记住你的作品。</em>",
                   "作品集 · 留学生作业辅导 · 博士 RP · 个展 · 求职",
                   '<span class="dot"></span>6 年 · 6000+ 案例 · 600+ 名校 Offer', '<div class="rule"></div>'),
}


def page(color, label, title, sub, foot, bar):
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--c:{color}">
  <div class="top"><span class="mono">1% Design Lab · 梦想管理局</span><span class="mono">{label}</span></div>
  <div><h1>{title}</h1><p class="sub">{sub}</p></div>
  <div class="mono" style="color:#EDEDE8">{foot}</div>
  {bar}
</body></html>"""


async def main():
    out = ROOT / "assets" / "share"
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for name, args in PAGES.items():
            tmp = out / f".{name}.html"
            tmp.write_text(page(*args), encoding="utf-8")
            await pg.goto(tmp.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(out / f"{name}.png"))
            tmp.unlink()
            print("wrote", f"assets/share/{name}.png")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
