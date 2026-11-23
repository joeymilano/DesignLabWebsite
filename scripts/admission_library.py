# -*- coding: utf-8 -*-
"""2027 Academy offers. Ownership confirmed by user on 2026-11-23."""
from pathlib import Path
import json
import re
ROOT=Path(__file__).resolve().parent.parent

def block(en=False):
 d=json.loads((ROOT/'assets/site/admissions/2027.json').read_text())
 def t(zh,eng):return eng if en else zh
 tiles=''.join(f'<button type="button" class="ad-school" data-school="{s["id"]}" aria-pressed="false"><span class="ad-logo ad-logo-{s["id"]}"><img src="/assets/site/admissions/{s["id"]}.svg" alt="{s["en"]}" loading="lazy" width="190" height="62"></span><span class="ad-school-name">{s["en"] if en else s["zh"]}<span>100</span></span></button>' for s in d['schools'])
 cats=[('focused',t('设计与创意','Design & creative')),('all',t('全部专业','All subjects')),('design',t('设计 / 游戏','Design / Games')),('media',t('媒体与传播','Media & communication')),('fashion',t('时尚与纺织','Fashion & textiles')),('culture',t('文化与音乐','Culture & music')),('urban',t('城市与空间','Urban studies')),('other',t('其他专业','Other subjects'))]
 return f'''<!-- admission-library:start -->
<link rel="stylesheet" href="/assets/site/admissions/library.css?v=20261123b">
<section class="sec sec-t ad-library" id="admissions" data-lang="{'en' if en else 'zh'}"><div class="wrap">
<div class="ad-heading"><h2>{t('案例库','Student offers')}</h2><span class="ad-edition">2027<span>500 {t('份录取','offers')}</span></span></div>
<div class="ad-schools" role="group" aria-label="{t('院校','Universities')}">{tiles}</div>
<div class="ad-tools"><label class="ad-search-label"><span class="ad-sr">{t('搜索','Search')}</span><input id="ad-search" type="search" placeholder="{t('搜索院校、专业','Search universities, subjects')}" autocomplete="off"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg></label><label><span class="ad-sr">{t('专业','Subject')}</span><select id="ad-category">{''.join(f'<option value="{v}">{label}</option>' for v,label in cats)}</select></label><label><span class="ad-sr">{t('录取类型','Offer type')}</span><select id="ad-result"><option value="all">{t('全部录取类型','All offer types')}</option><option value="CO">{t('有条件录取','Conditional')}</option><option value="UO">{t('无条件录取','Unconditional')}</option></select></label><button type="button" id="ad-reset">{t('重置','Reset')}</button></div>
<div class="ad-results-bar"><p id="ad-count" role="status" aria-live="polite">{t('加载中','Loading')}</p><span>{t('入学年份 / 2027','Entry / 2027')}</span></div>
<div class="ad-grid" id="ad-grid"></div><div class="ad-more"><button type="button" id="ad-more" hidden>{t('更多案例','More offers')} <span aria-hidden="true">↓</span></button></div>
<noscript><p>{t('请启用 JavaScript 查看案例','Enable JavaScript to view offers')}</p></noscript>
</div></section><script src="/assets/site/admissions/library.js?v=20261123b" defer></script>
<!-- admission-library:end -->'''

def inject(markup,en=False):
 label='Student offers' if en else '案例库'
 if 'href="#admissions"' not in markup:
  markup=re.sub(r'(<a class="btn btn-line" href="#gallery">.*?</a>)',lambda m:m.group(1)+f'<a class="btn btn-line" href="#admissions">{label} <span class="arr">↓</span></a>',markup,count=1)
 else:
  markup=re.sub(r'(<a class="btn btn-line" href="#admissions">).*?(<span class="arr">)',lambda m:m.group(1)+label+' '+m.group(2),markup)
 if not en:
  markup=re.sub(r'(<h[1-6]\b[^>]*>)([\s\S]*?)(</h[1-6]>)',lambda m:m.group(1)+m.group(2).replace('。','')+m.group(3),markup)
 if '<!-- admission-library:start -->' in markup:
  return re.sub(r'<!-- admission-library:start -->[\s\S]*?<!-- admission-library:end -->',lambda _:block(en),markup)
 return markup.replace('<section class="sec sec-t" id="stories">',block(en)+'\n<section class="sec sec-t" id="stories">')

if __name__=='__main__':
 for rel,en in [('academy/index.html',False),('en/academy/index.html',True)]:
  p=ROOT/rel;p.write_text(inject(p.read_text(),en))
