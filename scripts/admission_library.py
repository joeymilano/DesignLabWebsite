# -*- coding: utf-8 -*-
"""2027 Academy offer records; ownership confirmed by user on 2026-11-23."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent

def block(en=False):
 d=json.loads((ROOT/'assets/site/admissions/2027.json').read_text())
 def t(zh,eng):return eng if en else zh
 tiles=''.join(f'<button type="button" class="ad-school" data-school="{s["id"]}" aria-pressed="false"><span class="ad-logo ad-logo-{s["id"]}"><img src="/assets/site/admissions/{s["id"]}.svg" alt="{s["en"]}" loading="lazy" width="190" height="62"></span><strong>{s["en"] if en else s["zh"]}</strong><span>100 {t("条申请记录","records")} <b>↗</b></span></button>' for s in d['schools'])
 cats=[('focused',t('设计与创意相关 · 97','Design & creative · 97')),('all',t('全部方向 · 500','All subjects · 500')),('design',t('设计 / 游戏 / 沉浸艺术','Design / Games / Immersive arts')),('media',t('媒体与传播','Media & communication')),('fashion',t('时尚与纺织','Fashion & textiles')),('culture',t('文化创意与音乐','Culture & music')),('urban',t('城市与空间','Urban studies')),('other',t('其他方向','Other subjects'))]
 return f'''<!-- admission-library:start -->
<link rel="stylesheet" href="/assets/site/admissions/library.css?v=20261123">
<section class="sec sec-t ad-library" id="admissions" data-lang="{'en' if en else 'zh'}"><div class="wrap">
<div class="ad-heading"><div><p class="label mono">2027 / STUDENT OFFERS</p><h2>{t('从背景，到下一站。','From here, to what’s next.')}</h2><p>{t('五所英国大学，500 条申请记录。先找到与你相近的起点，再看清每一份 Offer 的条件。','500 application records across five UK universities. Explore backgrounds, programmes and the conditions attached to each offer.')}</p></div><div class="ad-edition"><b>2027</b><span>{t('秋季入学 · 学员录取案例','Autumn entry · Student offers')}</span></div></div>
<div class="ad-schools">{tiles}</div>
<div class="ad-tools"><label>{t('搜索背景与专业','Search backgrounds & programmes')}<input id="ad-search" type="search" placeholder="{t('试试 Animation、游戏、数字媒体…','Try Animation, Games, Digital Media…')}"></label><label>{t('专业方向','Subject area')}<select id="ad-category">{''.join(f'<option value="{v}">{label}</option>' for v,label in cats)}</select></label><label>{t('录取类型','Offer type')}<select id="ad-result"><option value="all">{t('全部类型','All offers')}</option><option value="CO">{t('CO · 有条件录取','CO · Conditional')}</option><option value="UO">{t('UO · 无条件录取','UO · Unconditional')}</option></select></label></div>
<div class="ad-results-bar"><p id="ad-count" role="status" aria-live="polite">{t('正在加载案例…','Loading records…')}</p><button type="button" id="ad-reset">{t('重置筛选','Reset filters')} ↺</button></div>
<div class="ad-grid" id="ad-grid"></div><div class="ad-more"><button type="button" id="ad-more" class="btn btn-line" hidden>{t('查看更多案例','Load more records')} ↓</button></div>
<noscript><p>{t('请启用 JavaScript 以搜索和查看申请记录。','Enable JavaScript to browse and search the records.')}</p></noscript>
<details class="ad-source"><summary>{t('数据来源与阅读说明','Source & reading notes')}</summary><p>{t('来源：用户提供的《布大+华威+利兹+格大+谢大2027学年500个录取案例》，版本日期 2026.11.10。共 500 条记录（非去重人数），498 条 CO、2 条 UO。案例归属已由学院确认；本次依据汇总表整理，未逐份核验原始 Offer。','Source: supplied 500-case workbook for 2027 entry, dated 10 November 2026. 500 records, not unique applicants: 498 CO and 2 UO. The Academy confirmed these as its student cases. Compiled from the supplied summary; individual original offers have not been independently verified.')}</p><p>{t('成绩与条件保留表格原值，数值型比例统一显示为百分比；未提供的字段不作推断。CO 为有条件录取，UO 为无条件录取，均不代表已经入学。方向分类用于浏览，不代表该专业必须提交作品集。个案条件不等于统一录取门槛。院校标识仅用于识别学校，不表示合作或背书。','Grades and conditions follow the source; numeric fractions are displayed as percentages. Missing values are not inferred. CO means conditional and UO unconditional, neither confirms enrolment. Subject groups aid browsing and do not imply a portfolio requirement. Individual conditions are not universal entry requirements. University marks identify institutions, not partnerships or endorsements.')}</p><p>{' · '.join(f'<a href="{s["url"]}" target="_blank" rel="noopener">{s["en"] if en else s["zh"]} ↗</a>' for s in d['schools'])}</p></details>
</div></section><script src="/assets/site/admissions/library.js?v=20261123" defer></script>
<!-- admission-library:end -->'''

def inject(markup,en=False):
 if 'href="#admissions"' not in markup:
  import re
  label='Explore 500 student offers' if en else '查看 500 条录取案例'
  markup=re.sub(r'(<a class="btn btn-line" href="#gallery">.*?</a>)',lambda m:m.group(1)+f'<a class="btn btn-line" href="#admissions">{label} <span class="arr">↓</span></a>',markup,count=1)
 if '<!-- admission-library:start -->' in markup:
  import re
  return re.sub(r'<!-- admission-library:start -->[\s\S]*?<!-- admission-library:end -->',lambda _:block(en),markup)
 return markup.replace('<section class="sec sec-t" id="stories">',block(en)+'\n<section class="sec sec-t" id="stories">')

if __name__=='__main__':
 for rel,en in [('academy/index.html',False),('en/academy/index.html',True)]:
  p=ROOT/rel;p.write_text(inject(p.read_text(),en))
