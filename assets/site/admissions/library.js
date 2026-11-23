(() => {
 const root=document.querySelector('.ad-library');if(!root)return;
 const en=root.dataset.lang==='en', t=(a,b)=>en?b:a, $=id=>root.querySelector('#ad-'+id);
 const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let data,school='',limit=12;
 const aliases={design:'设计',media:'数字媒体 传媒 传播 新闻',fashion:'时尚 服装 纺织',culture:'文化 创意 音乐 艺术管理',urban:'城市 空间 规划',other:'商科 法律 工程 其他'};
 function render(){
  const q=$('search').value.trim().toLowerCase(),cat=$('category').value,result=$('result').value;
  const records=data.cases.filter(c=>(!school||c.school===school)&&(cat==='all'||(cat==='focused'?c.category!=='other':c.category===cat))&&(result==='all'||c.result===result)&&(!q||[c.origin,c.major,c.program,c.grade,data.schools.find(s=>s.id===c.school).zh,data.schools.find(s=>s.id===c.school).en,aliases[c.category],...Object.entries({'games':'游戏','user experience':'用户体验 交互','immersive':'沉浸 虚拟现实','digital media':'数字媒体','animation':'动画','fashion':'时尚 服装','music':'音乐'}).filter(([word])=>[c.program,c.major].join(' ').toLowerCase().includes(word)).map(([,label])=>label)].join(' ').toLowerCase().includes(q)));
  $('count').textContent=t(`找到 ${records.length} 条记录 · 已展示 ${Math.min(limit,records.length)} 条`,`Found ${records.length} records · Showing ${Math.min(limit,records.length)}`);
  $('grid').innerHTML=records.slice(0,limit).map(c=>{
   const s=data.schools.find(s=>s.id===c.school),field=(a,b,value,cls='')=>`<div><dt>${t(a,b)}</dt><dd class="${cls}">${esc(value)}</dd></div>`;
   return `<article class="ad-card"><div class="ad-card-top"><span>${esc(c.year)} / ${esc(c.id.toUpperCase())}</span><span>${c.result==='CO'?t('CO · 有条件录取','CO · Conditional'):t('UO · 无条件录取','UO · Unconditional')}</span></div><h3>${esc(c.program)}</h3><p class="ad-university">${esc(en?s.en:s.zh)}</p><dl>${field('本科 / 原就读院校','Previous institution',c.origin)}${field('原专业','Previous subject',c.major)}${field('申请时成绩','Grade at application',c.grade,'ad-grade')}</dl><details><summary>${t('查看 Offer 条件与来源','Offer conditions & source')} ↗</summary><p>${esc(c.condition)}</p><p class="ad-ref">${t('原表','Source')}: ${esc(c.sourceSheet)} · ${t('第','row ')} ${c.sourceRow} ${t('行','')}<br>2026.11.10 · ${t('学员录取案例','Academy student offer')}</p></details></article>`;
  }).join('')||`<p class="ad-empty">${t('没有匹配的案例。试试其他关键词，或重置筛选。','No matching records. Try another keyword or reset the filters.')}</p>`;
  $('more').hidden=limit>=records.length;
  root.querySelectorAll('[data-school]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.school===school)));
 }
 fetch('/assets/site/admissions/2027.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{
  data=d;render();
  for(const id of ['search','category','result'])$(id).addEventListener(id==='search'?'input':'change',()=>{limit=12;render()});
  root.querySelectorAll('[data-school]').forEach(b=>b.addEventListener('click',()=>{school=school===b.dataset.school?'':b.dataset.school;limit=12;render()}));
  $('reset').addEventListener('click',()=>{school='';limit=12;$('search').value='';$('category').value='focused';$('result').value='all';render()});
  $('more').addEventListener('click',()=>{limit+=12;render()});
 }).catch(()=>{$('count').textContent=t('案例暂时加载失败，请刷新页面重试。','Records could not load. Please refresh to try again.')});
})();
