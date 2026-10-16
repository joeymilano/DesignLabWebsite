"""Industrial case studies from the supplied portfolio, pages 2–15.

ScanGo public display was explicitly approved by the user on 2026-10-16.
Official film: TransFuture Aviation homepage, retrieved 2026-10-16.
"""
from site_content import B

CASES = [
    dict(slug='honghu-mark1', name=B('鸿鹄 Mark1 eVTOL', 'Honghu Mark1 eVTOL'),
         category=B('航空出行 · 工业设计', 'Aviation · Industrial design'),
         partner=B('华羽先翔', 'TransFuture Aviation'),
         cover='honghu-cover', width=1800, height=942,
         intro=B('面向城市空中出行的电动垂直起降飞行器，探索座舱、机身与六旋翼布局的整体造型。',
                 'An electric vertical take-off and landing aircraft for urban air mobility, exploring the form of the cabin, fuselage and six-rotor configuration.'),
         scope=B('外观造型 / 三维呈现', 'Exterior form / 3D visualisation')),
    dict(slug='scango', name='ScanGo',
         category=B('陆空两用无人机 · 工业设计', 'Land–air UAV · Industrial design'),
         partner=B('西北工业大学', 'Northwestern Polytechnical University'),
         cover='scango-cover', width=1800, height=1274,
         intro=B('将地面行驶与空中飞行结合的无人机概念。从形态探索、概念草图到三维渲染，呈现功能与造型的推敲。',
                 'A UAV concept combining ground travel and aerial flight. From form studies and concept sketches to 3D renders, the project explores function and aesthetics together.'),
         scope=B('概念设计 / 草图 / 三维渲染', 'Concept design / Sketches / 3D rendering')),
]


def selected(slug):
    return next(c for c in CASES if c['slug'] == slug)


def cards(g, home=False):
    out = []
    for c in CASES:
        href = f"{g.pre()}/studio/{c['slug']}/"
        cls = 'tile w6' if home else 'industrial-card'
        out.append(f'''<a class="{cls}" href="{href}" data-reveal>
          <div class="industrial-cover"><img src="/assets/industrial/{c['cover']}-sm.webp" width="{c['width']}" height="{c['height']}" alt="{g.e(c['name'])} — {g.e(c['category'])}" loading="lazy" decoding="async"></div>
          <div class="industrial-caption"><p class="label"><span class="dot s"></span> {g.e(c['category'])}</p><h3>{g.e(c['name'])}<span aria-hidden="true">↗</span></h3><p>{g.e(c['intro'])}</p></div>
        </a>''')
    return ''.join(out)


def index_rows(g, start=9):
    out = []
    for i, c in enumerate(CASES, start):
        out.append(f'''<a class="row" data-k="s" data-b="s" data-img="/assets/industrial/{c['cover']}-sm.webp" href="{g.pre()}/studio/{c['slug']}/"><span class="row-n">{i:02d}</span><span class="row-t">{g.e(c['name'])}</span><span class="row-c">{g.e(c['category'])}</span><span class="row-b"><span class="dot s"></span>{'工作室 · 工业设计' if g.zh() else 'Studio · Industrial'}</span><span class="row-y">{'案例' if g.zh() else 'Case study'}</span><span class="row-a">↗</span></a>''')
    return ''.join(out)


def studio_block(g):
    return f'''<div class="industrial-work" id="industrial-work">
      <div class="industrial-heading"><div><p class="label"><span class="dot s"></span> Industrial design</p><h2 class="h2">{'从形态，到实体。' if g.zh() else 'Form takes shape.'}</h2></div></div>
      <div class="industrial-grid">{cards(g)}</div>
    </div>'''


def assets(markup):
    return markup.replace('</head>', '<link rel="stylesheet" href="/assets/site/industrial.css?v=20261016">\n</head>')


def figure(g, name, width, height, caption, cls=''):
    return f'''<figure class="case-figure {cls}"><img src="/assets/industrial/{name}.webp" width="{width}" height="{height}" alt="{g.e(caption)}" loading="lazy" decoding="async"><figcaption>{g.e(caption)}</figcaption></figure>'''


def page(g, slug):
    c = selected(slug)
    path = f'/studio/{slug}/'
    title = g.t(c['name']) + (' — 工业设计案例 | 1% Design Lab' if g.zh() else ' — Industrial design case study | 1% Design Lab')
    desc = g.t(c['intro']) + g.t(B(' 1% Design Lab 工业设计案例展示，包含产品外观、三维渲染与设计细节。了解项目的形态探索与视觉呈现，并联系工作室讨论工业设计需求。', ' An industrial design case study by 1% Design Lab, with product form, 3D renders and design details. Explore the visual development and contact the studio to discuss a project.'))
    ld = {'@context':'https://schema.org', '@graph':[g.org_ld(), g.crumbs_ld(path, g.t(c['name']))]}
    head = g.head(path, 'studio', title, desc, '工业设计,eVTOL,无人机,3D渲染,ScanGo,鸿鹄Mark1', 'og-studio', ld)
    head = head.replace('/assets/share/og-studio.png', f"/assets/industrial/{c['cover']}.webp")
    head = head.replace('content="1200"', f'content="{c["width"]}"').replace('content="630"', f'content="{c["height"]}"')
    hero = f'''<section class="case-hero wrap">
      <a class="link case-back" href="{g.pre()}/studio/#industrial-work">← {'返回工业设计案例' if g.zh() else 'Back to industrial work'}</a>
      <p class="label"><span class="dot s"></span> {g.e(c['category'])}</p>
      <h1>{g.e(c['name'])}</h1>
      <div class="case-intro"><p class="lead">{g.e(c['intro'])}</p><dl><div><dt>{'项目关联' if g.zh() else 'Project context'}</dt><dd>{g.e(c['partner'])}</dd></div><div><dt>{'设计内容' if g.zh() else 'Design scope'}</dt><dd>{g.e(c['scope'])}</dd></div></dl></div>
      <img class="case-hero-image" src="/assets/industrial/{c['cover']}.webp" width="{c['width']}" height="{c['height']}" alt="{g.e(c['name'])} — {'整体造型' if g.zh() else 'overall form'}" fetchpriority="high">
    </section>'''
    if slug == 'honghu-mark1':
        content = f'''<section class="case-section wrap">
          <div class="case-section-heading"><p class="label">01 / Form</p><h2>{'六旋翼布局下的整体造型。' if g.zh() else 'A form built around six rotors.'}</h2><p>{g.t(B('以流线型机身连接座舱、机翼与旋翼，透过不同视角与配色呈现整体比例和体量关系。', 'A streamlined fuselage connects the cabin, wings and rotors. Different views and finishes reveal the proportions and relationship between these elements.'))}</p></div>
          <div class="case-pair">{figure(g,'honghu-studio',1800,1125,B('浅色机身 · 三维渲染','Light finish · 3D render'))}{figure(g,'honghu-dark',1800,1125,B('深色机身 · 三维渲染','Dark finish · 3D render'))}</div>
        </section>
        <section class="case-section wrap">
          <div class="case-section-heading"><p class="label">02 / Model</p><h2>{'从多角度呈现，到模型展示。' if g.zh() else 'From rendered views to a display model.'}</h2></div>
          <div class="case-pair">{figure(g,'honghu-model',1280,799,B('机身与旋翼的体量关系','Fuselage and rotor proportions'))}{figure(g,'honghu-exhibition',1080,810,B('展会模型 · 项目资料','Exhibition model · Project archive'))}</div>
        </section>
        <section class="case-section wrap" id="film">
          <div class="case-film">
            <div><p class="label">03 / In motion</p><h2>{'鸿鹄系列，实机影像。' if g.zh() else 'Honghu series, on film.'}</h2><a class="link" href="https://www.transfutureaviation.com" target="_blank" rel="noopener">{'华羽先翔官网' if g.zh() else 'TransFuture Aviation'} ↗</a></div>
            <figure><video controls playsinline preload="none" poster="/assets/industrial/honghu-film-poster.webp" width="1280" height="720" aria-label="{'华羽先翔鸿鹄系列官方展示视频' if g.zh() else 'Official TransFuture Aviation Honghu aircraft film'}"><source src="/assets/industrial/honghu-official.mp4" type="video/mp4"><a href="/assets/industrial/honghu-official.mp4">{'下载视频' if g.zh() else 'Download film'}</a></video></figure>
          </div>
        </section>'''
    else:
        content = f'''<section class="case-section wrap">
          <div class="case-section-heading"><p class="label">01 / Ideation</p><h2>{'在地面与空中之间。' if g.zh() else 'Between ground and sky.'}</h2><p>{g.t(B('围绕陆空两种工作场景展开形态探索，将轮组、主体与旋翼的组合关系逐步转化为概念方案。', 'Form exploration across two operating environments, developing the arrangement of wheels, body and rotors into a coherent concept.'))}</p></div>
          {figure(g,'scango-ideation',1800,1273,B('形态与场景探索 · 设计过程板','Form and scenario exploration · Design process board'))}
          {figure(g,'scango-sketches',1800,1273,B('概念草图 · 比例与结构关系','Concept sketches · Proportions and component relationships'))}
        </section>
        <section class="case-section wrap">
          <div class="case-section-heading"><p class="label">02 / Development</p><h2>{'用三维推敲比例与细节。' if g.zh() else 'Refining proportions in three dimensions.'}</h2><p>{g.t(B('从早期配色与体量尝试，到座舱、轮组及旋翼的多角度呈现，保留设计推进中的不同方案。', 'From early colour and volume studies to views of the cabin, wheels and rotors, these images trace the different design iterations.'))}</p></div>
          {figure(g,'scango-development',1800,1273,B('早期方案 · 三维渲染与配色探索','Early concepts · 3D renders and colour studies'))}
          <div class="case-pair">{figure(g,'scango-front',1800,1275,B('正面视角 · 地面模式','Front view · Ground mode'))}{figure(g,'scango-profile',1800,632,B('侧面视角 · 轮组与主体','Side view · Wheels and body'))}</div>
        </section>'''
    other = CASES[1] if slug == 'honghu-mark1' else CASES[0]
    end = f'''<section class="case-end wrap"><a class="link" href="{g.pre()}/studio/{other['slug']}/">{'下一个案例' if g.zh() else 'Next case'} · {g.e(other['name'])} ↗</a><button class="btn btn-solid" data-consult="studio" data-from="industrial-case">{'聊聊你的产品' if g.zh() else 'Discuss your product'} ↗</button></section>'''
    return assets(head + g.header(path,'studio') + hero + content + end + g.footer())
