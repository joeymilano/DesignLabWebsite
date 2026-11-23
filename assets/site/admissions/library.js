(() => {
 const root=document.querySelector('.ad-library');if(!root)return;
 const en=root.dataset.lang==='en', t=(a,b)=>en?b:a, $=id=>root.querySelector('#ad-'+id);
 const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let data,school='',limit=12;
 const aliases={design:'设计',media:'数字媒体 传媒 传播 新闻',fashion:'时尚 服装 纺织',culture:'文化 创意 音乐 艺术管理',urban:'城市 空间 规划',other:'商科 法律 工程 其他'};
 function render(){
  const q=$('search').value.trim().toLowerCase(),cat=$('category').value,result=$('result').value;
  const records=data.cases.filter(c=>(!school||c.school===school)&&(cat==='all'||(cat==='focused'?c.category!=='other':c.category===cat))&&(result==='all'||c.result===result)&&(!q||[c.origin,c.major,c.program,c.grade,data.schools.find(s=>s.id===c.school).zh,data.schools.find(s=>s.id===c.school).en,aliases[c.category],...Object.entries({'games':'游戏','user experience':'用户体验 交互','immersive':'沉浸 虚拟现实','digital media':'数字媒体','animation':'动画','fashion':'时尚 服装','music':'音乐'}).filter(([word])=>[c.program,c.major].join(' ').toLowerCase().includes(word)).map(([,label])=>label)].join(' ').toLowerCase().includes(q)));
  $('count').textContent=t(`${records.length} 个案例`,`${records.length} offers`);
  $('grid').innerHTML=records.slice(0,limit).map(c=>{
   const s=data.schools.find(s=>s.id===c.school);
   return `<article class="ad-card"><div class="ad-row"><div class="ad-program"><p class="ad-university">${esc(en?s.en:s.zh)}</p><h3>${esc(c.program)}</h3></div><dl class="ad-background"><dt>${t('申请背景','Background')}</dt><dd>${esc(c.origin)}</dd><dd>${esc(c.major)}</dd></dl><dl class="ad-score"><dt>${t('申请成绩','Grade')}</dt><dd>${esc(c.grade)}</dd></dl></div><details><summary><span>${c.result==='CO'?t('有条件录取','Conditional offer'):t('无条件录取','Unconditional offer')}</span><span>${t('录取条件','Offer conditions')} <span class="ad-open" aria-hidden="true">＋</span></span></summary><p class="ad-condition">${esc(c.condition)}</p></details></article>`;
  }).join('')||`<p class="ad-empty">${t('暂无匹配案例','No matching offers')}</p>`;
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
