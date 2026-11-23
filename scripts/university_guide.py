"""QS Art & Design ranking explorer. Current admissions are independent of ranking year."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent

def block():
 return '''<!-- university-guide:start -->
<link rel="stylesheet" href="/assets/site/universities/guide.css?v=20261123c">
<section class="sec sec-t uni-guide" id="universities"><div class="wrap">
<div class="uni-heading"><div><p>QS ART & DESIGN</p><h2>全球院校榜单</h2></div><span>TOP 50</span></div>
<div class="uni-controls"><div class="uni-years" role="group" aria-label="榜单年份"><button type="button" data-year="2026" aria-pressed="true">2026</button><button type="button" data-year="2025" aria-pressed="false">2025</button><button type="button" data-year="2024" aria-pressed="false">2024</button></div><label class="uni-search"><span class="uni-sr">搜索院校</span><input id="uni-search" type="search" placeholder="搜索院校" autocomplete="off"></label></div>
<div class="uni-meta"><span id="uni-count" role="status" aria-live="polite">加载中</span></div>
<div class="uni-column-head" aria-hidden="true"><span>排名</span><span>院校</span><div><span>2026</span><span>2025</span><span>2024</span></div><span>申请</span></div>
<div id="uni-list"></div><nav class="uni-pagination" id="uni-pagination" aria-label="院校榜单分页"></nav>
<div class="uni-foot"><a id="uni-source" href="https://www.topuniversities.com/university-subject-rankings/art-design" target="_blank" rel="noopener">QS 官方榜单 ↗</a></div>
<noscript><p>请启用 JavaScript 查看院校与申请信息</p></noscript>
</div></section><script src="/assets/site/universities/guide.js?v=20261123c" defer></script>
<!-- university-guide:end -->'''

def inject(markup,en=False):
 if en:return markup
 if '<!-- university-guide:start -->' in markup:
  markup=re.sub(r'<!-- university-guide:start -->[\s\S]*?<!-- university-guide:end -->',lambda _:block(),markup)
 else:
  markup=markup.replace('<!-- admission-library:start -->',block()+'\n<!-- admission-library:start -->')
 if 'href="#universities"' not in markup:
  markup=re.sub(r'(<a class="btn btn-line" href="#admissions">.*?</a>)',lambda m:m.group(1)+'<a class="btn btn-line" href="#universities">全球院校榜单 <span class="arr">↓</span></a>',markup,count=1)
 markup=re.sub(r'(href="#universities">).*?(<span class="arr">)',lambda m:m.group(1)+'全球院校榜单 '+m.group(2),markup)
 markup=markup.replace('<div class="acts" data-reveal>','<div class="acts academy-acts" data-reveal>',1)
 return markup

if __name__=='__main__':
 p=ROOT/'academy/index.html';p.write_text(inject(p.read_text()))
