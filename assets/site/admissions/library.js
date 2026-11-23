(() => {
 const root=document.querySelector('.ad-library');if(!root)return;
 const en=root.dataset.lang==='en',t=(a,b)=>en?b:a,$=id=>root.querySelector('#ad-'+id);
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const rail=root.querySelector('.ad-schools'),railNav=root.querySelector('.ad-school-nav');
 let data,schools,school='',limit=12;
 const aliases={design:'设计 交互 游戏 沉浸 虚拟现实',media:'数字媒体 传媒 传播 新闻 电影 摄影 广告',fashion:'时尚 服装 纺织',culture:'文化 创意 音乐 美术 艺术管理',urban:'建筑 景观 城市 空间 规划',other:'商科 法律 工程 其他'};
 function railState(){
  const max=rail.scrollWidth-rail.clientWidth;
  railNav.hidden=max<2;$('schools-prev').disabled=rail.scrollLeft<2;$('schools-next').disabled=rail.scrollLeft>=max-2;
 }
 function render(){
  const q=$('search').value.trim().toLowerCase(),cat=$('category').value,result=$('result').value,year=$('year').value;
  if(school&&year!=='all'&&!schools.get(school).countsByYear[year])school='';
  const records=data.cases.filter(c=>(year==='all'||c.year===year)&&(!school||c.school===school)&&(cat==='all'||(cat==='focused'?c.category!=='other':c.category===cat))&&(result==='all'||c.result===result)&&(!q||[c.origin,c.major,c.program,c.grade,c.year,schools.get(c.school).zh,schools.get(c.school).en,aliases[c.category],...Object.entries({'games':'游戏','user experience':'用户体验 交互','human computer interaction':'人机交互','immersive':'沉浸 虚拟现实','digital media':'数字媒体','animation':'动画','fashion':'时尚 服装','music':'音乐','architecture':'建筑','fine art':'纯艺 美术'}).filter(([word])=>[c.program,c.major].join(' ').toLowerCase().includes(word)).map(([,label])=>label)].join(' ').toLowerCase().includes(q)));
  $('count').textContent=t(`${records.length.toLocaleString()} 个案例`,`${records.length.toLocaleString()} offers`);
  $('years').textContent=year==='all'?'2026–2027':year;
  $('grid').innerHTML=records.slice(0,limit).map(c=>{
   const s=schools.get(c.school);
   return `<article class="ad-card" data-case-id="${esc(c.id)}" data-year="${esc(c.year)}"><div class="ad-row"><div class="ad-program"><p class="ad-university"><span class="ad-case-year">${esc(c.year)}</span>${esc(en?s.en:s.zh)}</p><h3>${esc(c.program)}</h3></div><dl class="ad-background"><dt>${t('申请背景','Background')}</dt><dd>${esc(c.origin)}</dd><dd>${esc(c.major)}</dd></dl><dl class="ad-score"><dt>${t('申请成绩','Grade')}</dt><dd>${esc(c.grade)}</dd></dl></div><details><summary><span>${c.result==='CO'?t('有条件录取','Conditional offer'):t('无条件录取','Unconditional offer')}</span><span>${t('录取条件','Offer conditions')} <span class="ad-open" aria-hidden="true">＋</span></span></summary><p class="ad-condition">${esc(c.condition)}</p></details></article>`;
  }).join('')||`<p class="ad-empty">${t('暂无匹配案例','No matching offers')}</p>`;
  $('more').hidden=limit>=records.length;
  root.querySelectorAll('[data-school]').forEach(b=>{
   const s=schools.get(b.dataset.school),count=year==='all'?s.count:s.countsByYear[year];
   b.hidden=!count;b.querySelector('.ad-school-count').textContent=count;b.setAttribute('aria-pressed',String(school===s.id));
  });
  requestAnimationFrame(railState);
 }
 fetch('/assets/site/admissions/cases.json?v=20261123d').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{
  data=d;schools=new Map(d.schools.map(s=>[s.id,s]));render();
  for(const id of ['search','year','category','result'])$(id).addEventListener(id==='search'?'input':'change',()=>{limit=12;if(id==='year')rail.scrollLeft=0;render()});
  root.querySelectorAll('[data-school]').forEach(b=>b.addEventListener('click',()=>{school=school===b.dataset.school?'':b.dataset.school;limit=12;render()}));
  $('reset').addEventListener('click',()=>{school='';limit=12;$('search').value='';$('year').value='all';$('category').value='focused';$('result').value='all';rail.scrollLeft=0;render()});
  $('more').addEventListener('click',()=>{limit+=12;render()});
  for(const [id,direction] of [['schools-prev',-1],['schools-next',1]])$(id).addEventListener('click',()=>rail.scrollBy({left:direction*rail.clientWidth,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));
  rail.addEventListener('scroll',railState,{passive:true});window.addEventListener('resize',railState);
 }).catch(()=>{$('count').textContent=t('案例暂时加载失败，请刷新页面重试。','Records could not load. Please refresh to try again.')});
})();
