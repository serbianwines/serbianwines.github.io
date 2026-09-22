'use strict';
(() => {
const KEY='serbian-wines-photo-route-20260922-v1';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=s=>String(s??'').toLowerCase().replace(/đ/g,'dj').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const safeURL=s=>{try{const u=new URL(s);return u.protocol==='https:'?esc(u.href):'';}catch{return '';}};
let data=null,cards=[],state={marks:{},visits:{}},persistent=true;
function storageMessage(){ $('#storage').textContent=persistent?'Отметки автоматически сохраняются в этом браузере. Синхронизации с другими устройствами нет.':'Сохранение в браузере недоступно. Экспортируй заметки до закрытия страницы.'; }
function load(){state={marks:{},visits:{}};persistent=true;try{const x=JSON.parse(localStorage.getItem(KEY)||'null');if(x&&x.marks&&typeof x.marks==='object'&&!Array.isArray(x.marks)&&x.visits&&typeof x.visits==='object')state=x;localStorage.setItem(KEY+'-probe','1');localStorage.removeItem(KEY+'-probe');}catch{persistent=false;}storageMessage();}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));persistent=true;}catch{persistent=false;}storageMessage();}
function mark(key){const m=state.marks[key];return m&&typeof m==='object'?m:{};}
function makeCard(i,o,style){
 const key=o.shop+'-'+i.id,ask=o.status==='ask',url=safeURL(o.source?.url),search=norm([i.name,i.aliases,i.source_year,i.question,i.shelf_note,o.catalog_vintage,o.note].join(' '));
 const badge=(v,c='')=>`<span class="badge ${c}">${v}</span>`;
 const price=o.price_rsd!=null?'≈ '+Number(o.price_rsd).toLocaleString('ru-RU')+' RSD'+(o.volume_l?' / '+String(o.volume_l).replace('.',',')+' л':''):'Цена не подтверждена';
 return `<article class="card" data-key="${key}" data-item="${esc(i.id)}" data-shop="${o.shop}" data-style="${style}" data-ask="${ask}" data-priority="${i.priority}" data-gem="${!!i.gem}" data-new="${i.origin!=='original_46'}" data-budget="${!!i.budget}" data-search="${esc(search)}"><div class="id">${esc(i.id)}</div><h3>${esc(i.name)}</h3><div class="badges">${i.priority===1?badge('Приоритет','priority'):''}${i.gem?badge('Гем','gem'):''}${i.sweet?badge('Сладкое / десертное','sweet'):''}${i.origin!=='original_46'?badge('Добавлено'):''}${badge(ask?'Сначала спросить':o.status==='delivery'?'Доставка другого филиала':'Найдено в онлайн-каталоге')}</div><p class="price">${price}</p><p>${esc(i.question)}</p>${i.shelf_note?`<p class="shelf">${esc(i.shelf_note)}</p>`:''}<p class="small"><b>В каталоге:</b> ${esc(o.catalog_vintage??'год не указан / не подтверждён')}<br><b>Цель исследования:</b> ${esc(i.source_year)}</p>${o.note?`<p class="small">${esc(o.note)}</p>`:''}<div class="actions row"><label><input type="checkbox" class="donecheck" data-key="${key}" aria-label="Снято: ${esc(i.name)}">Снято</label><label><input type="checkbox" class="absentcheck" data-key="${key}" aria-label="Не встретилось: ${esc(i.name)}">Не встретилось</label></div><details><summary>Год, цена, партия и источник</summary><textarea class="itemnote" data-key="${key}" rows="2" maxlength="4000" aria-label="Наблюдение: ${esc(i.name)}" placeholder="2025; 0,75 л; 1599 RSD; lot…"></textarea>${url?`<p class="source"><a href="${url}" target="_blank" rel="noopener noreferrer">${esc(o.source.label||'Источник')}</a> · ${esc(o.checked_date||'2026-09-22')}</p>`:''}<p class="small">${esc(i.evidence_note)}</p></details></article>`;
}
function render(){
 $('#summary').textContent=data.items.length+' групп поиска · 3 магазина · белое, розовое, красное, игристое и оранжевое';
 $('#serbian').textContent=data.metadata.serbian_photo_request;
 $('#navigation').innerHTML=data.shops.map(s=>`<a href="#${s.id}" data-shop="${s.id}">${esc(s.name)}</a>`).join('');
 $('#shopfilter').innerHTML='<option value="">Все магазины</option>'+data.shops.map(s=>`<option value="${s.id}">${esc(s.name)}</option>`).join('');
 $('#stylefilter').innerHTML='<option value="">Все полки</option>'+Object.entries(data.metadata.styles).map(([k,v])=>`<option value="${k}">${esc(v)}</option>`).join('');
 $('#shops').innerHTML=data.shops.map(s=>{
  const sections=Object.entries(data.metadata.styles).map(([style,title])=>{
   const found=[]; data.items.filter(i=>i.styles.includes(style)).sort((a,b)=>a.name.localeCompare(b.name,'sr')).forEach(i=>i.offers.filter(o=>o.shop===s.id).forEach(o=>found.push({i,o})));
   if(!found.length)return '';
   const normal=found.filter(x=>x.o.status!=='ask').map(x=>makeCard(x.i,x.o,style)).join('');
   const rare=found.filter(x=>x.o.status==='ask').map(x=>makeCard(x.i,x.o,style)).join('');
   return `<section class="style-section" data-style="${style}"><h2 class="style ${style}">${esc(title)}</h2>${normal}${rare?`<details class="rare"><summary>Сначала спросить · ${found.filter(x=>x.o.status==='ask').length}</summary><p class="small">Наличие в выбранном магазине не подтверждено.</p>${rare}</details>`:''}</section>`;
  }).join('');
  return `<section class="shop" id="${s.id}"><h2>${esc(s.name)}</h2><address>${esc(s.address)}</address><p class="shoplinks"><a href="https://www.google.com/maps/search/?api=1&amp;query=${encodeURIComponent(s.map_query)}" target="_blank" rel="noopener noreferrer">Открыть карту</a>${s.phone?` · <a href="tel:${esc(s.phone)}">${esc(s.phone)}</a>`:''}</p><p class="small">${esc(s.note)}</p>${s.hours?`<p class="small">${esc(s.hours)}</p>`:''}<details class="visit"><summary>Записать посещение</summary><textarea class="visitnote" data-shop="${s.id}" rows="2" maxlength="2000" aria-label="Посещение ${esc(s.name)}" placeholder="Дата, точный филиал, условия скидки"></textarea></details>${sections}</section>`;
 }).join('');
 cards=$$('.card');reflect();filter();
}
function reflect(){cards.forEach(c=>{const m=mark(c.dataset.key);c.querySelector('.donecheck').checked=!!m.done;c.querySelector('.absentcheck').checked=!!m.absent;c.querySelector('.itemnote').value=typeof m.note==='string'?m.note:'';c.classList.toggle('is-done',!!m.done);c.classList.toggle('is-absent',!!m.absent);});$$('.visitnote').forEach(x=>x.value=state.visits[x.dataset.shop]||'');}
function filter(){if(!data)return;const shop=$('#shopfilter').value,style=$('#stylefilter').value,scope=$('#scopefilter').value,q=norm($('#search').value).trim().split(/\s+/);cards.forEach(c=>{const d=c.dataset,m=mark(d.key);c.hidden=!!((shop&&d.shop!==shop)||(style&&d.style!==style)||($('#hideDone').checked&&m.done)||(scope==='priority'&&d.priority!=='1')||(scope==='gem'&&d.gem!=='true')||(scope==='new'&&d.new!=='true')||(scope==='budget'&&d.budget!=='true')||(scope==='ask'&&d.ask!=='true')||(scope==='catalog'&&d.ask==='true')||!q.every(t=>d.search.includes(t)));});$$('.rare').forEach(r=>{r.hidden=!r.querySelector('.card:not([hidden])');if($('#search').value.trim()||scope==='ask'||scope==='gem')r.open=true;});$$('.style-section,.shop').forEach(s=>s.hidden=!s.querySelector('.card:not([hidden])'));const visible=cards.filter(c=>!c.hidden);$('#counter').textContent='Групп: '+new Set(visible.map(c=>c.dataset.item)).size+' / '+data.items.length+' · снято: '+new Set(cards.filter(c=>mark(c.dataset.key).done).map(c=>c.dataset.key)).size;$('#empty').hidden=visible.length>0;}
function clearFilters(){ $('#search').value='';['shopfilter','stylefilter','scopefilter'].forEach(id=>$('#'+id).value='');$('#hideDone').checked=false;filter(); }
$('#shops').addEventListener('change',e=>{const x=e.target;if(!x.matches('.donecheck,.absentcheck'))return;const m=mark(x.dataset.key);state.marks[x.dataset.key]=m;const prop=x.matches('.donecheck')?'done':'absent';m[prop]=x.checked;if(x.checked)m[prop==='done'?'absent':'done']=false;m.updated=new Date().toISOString();save();reflect();filter();});
$('#shops').addEventListener('input',e=>{const x=e.target;if(x.matches('.itemnote')){const m=mark(x.dataset.key);state.marks[x.dataset.key]=m;m.note=x.value;m.updated=new Date().toISOString();$$('.itemnote').filter(y=>y!==x&&y.dataset.key===x.dataset.key).forEach(y=>y.value=x.value);save();}else if(x.matches('.visitnote')){state.visits[x.dataset.shop]=x.value;save();}});
['search','shopfilter','stylefilter','scopefilter','hideDone'].forEach(id=>$('#'+id).addEventListener(id==='search'?'input':'change',filter));
$('#clearFilters').addEventListener('click',clearFilters);
$('#navigation').addEventListener('click',e=>{const a=e.target.closest('a[data-shop]');if(a){clearFilters();$('#shopfilter').value=a.dataset.shop;filter();}});
function exportNotes(){const lines=['ФОТОНАБЛЮДЕНИЯ · Терруары Сербии',new Date().toLocaleString(),'Личные отметки; не приёмка доказательств.',''];data.shops.forEach(s=>{lines.push(s.name,state.visits[s.id]||'Дата и филиал не записаны.');data.items.forEach(i=>{const m=mark(s.id+'-'+i.id);if(m.done||m.absent||m.note)lines.push((m.done?'[СНЯТО]':m.absent?'[НЕ ВСТРЕТИЛОСЬ]':'[ЗАМЕТКА]')+' '+i.name,m.note||'Без подробностей.');});lines.push('');});return lines.join('\n');}
$('#export').addEventListener('click',()=>{const text=exportNotes();$('#exportText').value=text;$('#exportBox').hidden=false;$('#copyStatus').textContent='';const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='WINE-PHOTO-NOTES.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);$('#exportBox').scrollIntoView({block:'center'});});
$('#copyNotes').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#exportText').value);$('#copyStatus').textContent='Скопировано';}catch{$('#exportText').select();$('#copyStatus').textContent='Текст выделен. Выбери «Копировать» в меню.';}});
$('#closeExport').addEventListener('click',()=>$('#exportBox').hidden=true);
$('#reset').addEventListener('click',()=>{if(confirm('Удалить только отметки этой страницы? Сначала экспортируй нужное.')){state={marks:{},visits:{}};save();reflect();filter();}});
$('#lock').addEventListener('click',()=>{$('#shops').replaceChildren();cards=[];data=null;state={marks:{},visits:{}};$('#app').hidden=true;$('#gate').hidden=false;$('#exportBox').hidden=true;$('#exportText').value='';$('#password').value='';$('#password').focus();window.scrollTo(0,0);});
const bytes=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
$('#unlockForm').addEventListener('submit',async e=>{
 e.preventDefault();const button=$('#unlockButton'),error=$('#loginError');error.textContent='';button.disabled=true;button.textContent='Открываю…';
 try{
  if(!crypto.subtle||!window.DecompressionStream)throw new Error('Нужен современный браузер и адрес HTTPS.');
  let payload;try{const r=await fetch('list.enc.json',{cache:'no-cache',credentials:'omit'});if(!r.ok)throw new Error();payload=await r.json();}catch{throw new Error('Не удалось загрузить список. Проверь интернет и попробуй снова.');}
  const material=await crypto.subtle.importKey('raw',new TextEncoder().encode($('#password').value),'PBKDF2',false,['deriveKey']);
  const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:bytes(payload.salt),iterations:payload.iterations,hash:'SHA-256'},material,{name:'AES-GCM',length:256},false,['decrypt']);
  let compressed;try{compressed=await crypto.subtle.decrypt({name:'AES-GCM',iv:bytes(payload.iv)},key,bytes(payload.ciphertext));}catch{throw new Error('Неверный пароль. Попробуй ещё раз.');}
  const text=await new Response(new Blob([compressed]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
  data=JSON.parse(text);if(!Array.isArray(data.items)||!Array.isArray(data.shops))throw new Error('Не удалось прочитать список.');
  load();render();$('#password').value='';$('#gate').hidden=true;$('#app').hidden=false;$('#search').focus({preventScroll:true});
 }catch(err){error.textContent=err.message||'Не удалось открыть список.';}
 finally{button.disabled=false;button.textContent='Открыть список';}
});
// Refresh an existing book worker: it must not cache this page as index.html.
if('serviceWorker'in navigator)navigator.serviceWorker.getRegistration('/').then(r=>r&&r.update()).catch(()=>{});
})();
