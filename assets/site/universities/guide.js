(() => {
 const root=document.querySelector('.uni-guide');if(!root)return;
 const list=root.querySelector('#uni-list'), count=root.querySelector('#uni-count'), search=root.querySelector('#uni-search');
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const rank=v=>v&&/^=?\d+$/.test(String(v))?Number(String(v).replace('=','')):Infinity;
 const statuses={confirmed:'已公布',recurring:'常规日程',pending:'待公布',closed:'已结束',historical:'往届参考',process:'申请流程'};
 let data,year='2026',page=1;const pageSize=20,degrees=new Map(),expanded=new Set();
 const pagination=root.querySelector('#uni-pagination');
 function render(){
  list.querySelectorAll('.uni-row').forEach(el=>{el.open?expanded.add(el.dataset.id):expanded.delete(el.dataset.id)});
  const selected=data.schools.filter(s=>rank(s.ranks[year])<=50).sort((a,b)=>rank(a.ranks[year])-rank(b.ranks[year])||a.name.localeCompare(b.name));
  const q=search.value.trim().toLowerCase(),items=selected.filter(s=>[s.name,s.nameZh,s.country,s.countryZh,s.id].join(' ').toLowerCase().includes(q));
  count.textContent=`${year} · ${items.length} 所院校`;
  root.querySelectorAll('[data-year]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.year===year)));
  root.querySelector('#uni-source').href=data.sources[year].page;
  const pageCount=Math.max(1,Math.ceil(items.length/pageSize));page=Math.min(page,pageCount);
  const start=(page-1)*pageSize;
  list.innerHTML=items.slice(start,start+pageSize).map(s=>{
   const degree=degrees.get(s.id)||'ug';
   const a=s.admissions[degree];
   const history=['2026','2025','2024'].map(y=>`<span class="${y===year?'is-current':''}"><small>${y}</small>${esc(s.ranks[y]??'—')}</span>`).join('');
   return `<details class="uni-row" data-id="${esc(s.id)}" ${expanded.has(s.id)?'open':''}><summary><span class="uni-rank">${esc(s.ranks[year])}</span><span class="uni-school"><span class="uni-logo"><img src="${esc(s.logo)}" alt="${esc(s.name)} Logo" width="64" height="64" loading="lazy"></span><span class="uni-name"><strong>${esc(s.nameZh)}</strong><span>${esc(s.name)}</span><small>${esc(s.countryZh)}</small></span></span><span class="uni-history">${history}</span><span class="uni-toggle" aria-hidden="true">＋</span></summary><div class="uni-detail"><div class="uni-levels" role="group" aria-label="${esc(s.nameZh)}申请层次"><button type="button" data-degree="ug" aria-pressed="${degree==='ug'}">本科申请</button><button type="button" data-degree="pg" aria-pressed="${degree==='pg'}">硕士申请</button></div><p class="uni-program">${degree==='ug'?'本科':'硕士'} / ${esc(a.program)}</p><div class="uni-detail-grid"><div><h3>申请时间</h3><ol class="uni-timeline">${a.timeline.map(x=>`<li><div><time>${esc(x.date)}</time><small>${esc(statuses[x.status]||x.status)}</small></div><p>${esc(x.label)}</p></li>`).join('')}</ol></div><div><h3>录取要求</h3><ul class="uni-requirements">${a.requirements.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><div class="uni-links">${a.sources.map(x=>`<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)} ↗</a>`).join('')}</div></div></div></div></details>`;
  }).join('')||'<p class="uni-empty">暂无匹配院校</p>';
  pagination.hidden=items.length<=pageSize;
  pagination.innerHTML=`<span class="uni-page-count">${items.length?start+1:0}–${Math.min(start+pageSize,items.length)} / ${items.length}</span><div><button type="button" data-page="${page-1}" ${page===1?'disabled':''} aria-label="上一页">←</button>${Array.from({length:pageCount},(_,i)=>`<button type="button" data-page="${i+1}" ${page===i+1?'aria-current="page"':''} aria-label="第 ${i+1} 页">${i+1}</button>`).join('')}<button type="button" data-page="${page+1}" ${page===pageCount?'disabled':''} aria-label="下一页">→</button></div>`;
 }
 root.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||!data)return;
  if(b.dataset.year){year=b.dataset.year;page=1;render()}
  if(b.dataset.degree){const id=b.closest('.uni-row').dataset.id;degrees.set(id,b.dataset.degree);render();list.querySelector(`[data-id="${id}"] [data-degree="${b.dataset.degree}"]`).focus({preventScroll:true})}
  if(b.dataset.page&&!b.disabled){page=Number(b.dataset.page);render();root.querySelector('.uni-controls').scrollIntoView({block:'start'});list.querySelector('summary')?.focus({preventScroll:true})}
 });
 search.addEventListener('input',()=>{if(data){page=1;render()}});
 fetch('/assets/site/universities/data.json?v=20261123c').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{data=d;render()}).catch(()=>{count.textContent='加载失败，请刷新重试'});
})();
