const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const N=(n,o)=>new Intl.NumberFormat('it-IT',o).format(isFinite(n)?n:0);
const fmt=(n,d=0)=>N(n,{maximumFractionDigits:d});
const eur=(n,d=0)=>N(n,{style:'currency',currency:'EUR',maximumFractionDigits:d,minimumFractionDigits:d});
const pmt=(P,r,n)=>r?P*r/(1-Math.pow(1+r,-n)):P/n;
const loan=(P,m,n)=>({k:'Rata mensile',m:eur(m,2),r:[['Interessi totali',eur(m*n-P)],['Totale da restituire',eur(m*n)]],d:[P,m*n-P,'Capitale','Interessi']});
const C={
mutuo:v=>loan(v.p,pmt(v.p,v.t/1200,v.y*12),v.y*12),
prestito:v=>loan(v.p,pmt(v.p,v.t/1200,v.n),v.n),
interessi:v=>{const n=v.y*12,r=v.t/1200,g=Math.pow(1+r,n),F=r?v.c*g+v.v*(g-1)/r:v.c+v.v*n,T=v.c+v.v*n;
 return{k:'Capitale finale',m:eur(F),r:[['Totale versato',eur(T)],['Interessi maturati',eur(F-T)]],d:[T,F-T,'Versato','Interessi']}},
obiettivo:v=>{const n=v.y*12,r=v.t/1200,g=Math.pow(1+r,n),m=Math.max(0,r?(v.g-v.c*g)*r/(g-1):(v.g-v.c)/n),T=m*n+v.c,I=Math.max(0,v.g-T);
 return{k:'Versamento mensile',m:eur(m,2),r:[['Totale versato',eur(T)],['Interessi guadagnati',eur(I)]],d:[T,I,'Versato','Interessi']}},
iva:v=>{const k=v.al/100,s=v.m=='s',n=s?v.a/(1+k):v.a,i=n*k;
 return{k:s?'Imponibile':'Totale con IVA',m:eur(s?n:n+i,2),r:[['IVA al '+v.al+'%',eur(i,2)],[s?'Totale con IVA':'Imponibile',eur(s?v.a:n,2)]],d:[n,i,'Imponibile','IVA']}},
percentuale:v=>{const a=v.x/100*v.y,b=v.y?v.x/v.y*100:0,c=v.x?(v.y-v.x)/v.x*100:0;
 return v.m=='a'?{k:v.x+'% di '+v.y,m:fmt(a,2),r:[[v.y+' meno il '+v.x+'%',fmt(v.y-a,2)],[v.y+' più il '+v.x+'%',fmt(+v.y+a,2)]]}
 :v.m=='b'?{k:v.x+' su '+v.y,m:fmt(b,2)+'%'}:{k:'Variazione da '+v.x+' a '+v.y,m:(c>0?'+':'')+fmt(c,2)+'%'}}
};
function donut(d){if(!d)return'';const t=d[0]+d[1],p=t>0?Math.max(0,Math.min(100,d[0]/t*100)):0,q=Math.round(p);
return`<svg class=dn viewBox="0 0 36 36" role=img aria-label="${d[2]} ${q}%, ${d[3]} ${100-q}%"><circle cx=18 cy=18 r=15.915 fill=none stroke="#ffd23f" stroke-width=4.5 /><circle cx=18 cy=18 r=15.915 fill=none stroke="#19b5c8" stroke-width=4.5 stroke-dasharray="${p} ${100-p}" transform="rotate(-90 18 18)"/></svg><ul class=lg><li><i style=background:#19b5c8></i>${d[2]} ${q}%</li><li><i style=background:#ffd23f></i>${d[3]} ${100-q}%</li></ul>`}
function show(o){$('#out').innerHTML=`<div><small>${o.k}</small><b>${o.m}</b><dl>${(o.r||[]).map(r=>`<div><dt>${r[0]}</dt><dd>${r[1]}</dd></div>`).join('')}</dl></div>${donut(o.d)}`}
const id=document.body.dataset.c;
if(id){const F=$$('form [id]'),q=new URLSearchParams(location.search);
 const run=()=>{const v={};F.forEach(e=>v[e.id]=e.tagName=='SELECT'?(isNaN(e.value)?e.value:+e.value):parseFloat(e.value)||0);
  show(C[id](v));try{history.replaceState(null,'','?'+new URLSearchParams(v))}catch(x){}};
 F.forEach(e=>{if(q.has(e.id))e.value=q.get(e.id);const s=$('[data-for='+e.id+']');if(s)s.value=e.value});
 $('form').oninput=e=>{const t=e.target;if(t.dataset.for)$('#'+t.dataset.for).value=t.value;else{const s=$('[data-for='+t.id+']');if(s)s.value=t.value}run()};
 $('#sh').onclick=async()=>{try{navigator.share?await navigator.share({title:document.title,url:location.href}):(await navigator.clipboard.writeText(location.href),$('#sh').textContent='Link copiato ✓')}catch(x){}};
 run()}
const S=window.SITE||{},A=S.ads||{};
if(A.client&&$('.ad')){const s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+A.client;document.head.append(s);
 $$('.ad').forEach(e=>{const sl=(A.slots||{})[e.dataset.s];if(!sl)return;e.innerHTML=`<small>Pubblicità</small><ins class="adsbygoogle" style="display:block" data-ad-client="${A.client}" data-ad-slot="${sl}" data-ad-format="auto" data-full-width-responsive="true"></ins>`;e.classList.add('on');try{(window.adsbygoogle=window.adsbygoogle||[]).push({})}catch(x){}})}
$$('.aff').forEach(e=>{const a=(S.aff||{})[e.dataset.s]||(S.aff||{}).all;if(a)e.innerHTML=`<a href="${a.u}" target="_blank" rel="sponsored nofollow noopener">${a.t}</a><small>Link sponsorizzato</small>`});
