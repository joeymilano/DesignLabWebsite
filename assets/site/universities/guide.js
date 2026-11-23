(() => {
 const root=document.querySelector('.uni-guide');if(!root)return;
 const list=root.querySelector('#uni-list'), count=root.querySelector('#uni-count'), search=root.querySelector('#uni-search');
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const rank=v=>Number(String(v).replace('=',''));
 const statuses={confirmed:'已公布',recurring:'常规日程',pending:'待公布',closed:'已结束',historical:'往届参考',process:'申请流程'};
 let data,year='2026',degree='ug';let expanded=new Set();
 function render(){
  const selected=data.schools.filter(s=>rank(s.ranks[year])<=20).sort((a,b)=>rank(a.ranks[year])-rank(b.ranks[year])||a.name.localeCompare(b.name));
  const q=search.value.trim().toLowerCase(),items=selected.filter(s=>[s.name,s.nameZh,s.country,s.countryZh,s.id].join(' ').toLowerCase().includes(q));
  count.textContent=`${year} · ${items.length} 所院校`;
  root.querySelectorAll('[data-year]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.year===year)));
  root.querySelectorAll('[data-degree]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.degree===degree)));
  root.querySelector('#uni-source').href=data.sources[year].page;
  list.innerHTML=items.map(s=>{
   const a=s.admissions[degree];
   const history=['2026','2025','2024'].map(y=>`<span class="${y===year?'is-current':''}"><small>${y}</small>${esc(s.ranks[y])}</span>`).join('');
   return `<details class="uni-row" data-id="${esc(s.id)}" ${expanded.has(s.id)?'open':''}><summary><span class="uni-rank">${esc(s.ranks[year])}</span><span class="uni-school"><span class="uni-logo"><img src="${esc(s.logo)}" alt="${esc(s.name)} Logo" width="64" height="64" loading="lazy"></span><span class="uni-name"><strong>${esc(s.nameZh)}</strong><span>${esc(s.name)}</span><small>${esc(s.countryZh)}</small></span></span><span class="uni-history">${history}</span><span class="uni-toggle" aria-hidden="true">＋</span></summary><div class="uni-detail"><p class="uni-program">${degree==='ug'?'本科':'硕士'} / ${esc(a.program)}</p><div class="uni-detail-grid"><div><h3>申请时间</h3><ol class="uni-timeline">${a.timeline.map(x=>`<li><div><time>${esc(x.date)}</time><small>${esc(statuses[x.status]||x.status)}</small></div><p>${esc(x.label)}</p></li>`).join('')}</ol></div><div><h3>录取要求</h3><ul class="uni-requirements">${a.requirements.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><div class="uni-links">${a.sources.map(x=>`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)} ↗</a>`).join('')}</div></div></div></div></details>`;
  }).join('')||'<p class="uni-empty">暂无匹配院校</p>';
  list.querySelectorAll('.uni-row').forEach(el=>el.addEventListener('toggle',()=>{el.open?expanded.add(el.dataset.id):expanded.delete(el.dataset.id)}));
 }
 fetch('/assets/site/universities/data.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{data=d;render();root.querySelectorAll('[data-year]').forEach(b=>b.addEventListener('click',()=>{year=b.dataset.year;render()}));root.querySelectorAll('[data-degree]').forEach(b=>b.addEventListener('click',()=>{degree=b.dataset.degree;render()}));search.addEventListener('input',render)}).catch(()=>{count.textContent='加载失败，请刷新重试'});
})();
