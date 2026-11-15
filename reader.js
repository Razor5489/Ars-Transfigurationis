const $=id=>document.getElementById(id);
const roman=['I','II','III','IV','V','VI','VII'];
const pages=[],yearPages=[],lessonPages=[];
const readStore=(key,fallback=null)=>{try{return localStorage.getItem('ars-transfigurationis-'+key)??fallback}catch{return fallback}};
const writeStore=(key,val)=>{try{localStorage.setItem('ars-transfigurationis-'+key,String(val));return true}catch{return false}};
const seal=`<svg viewBox="0 0 100 100" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1"><circle cx="50" cy="50" r="43"/><path d="M50 9 85 70H15ZM50 91 15 30h70ZM50 20v60M20 50h60"/><circle cx="50" cy="50" r="14"/></g><path d="m50 34 4 12 12 4-12 4-4 12-4-12-12-4 12-4z" fill="currentColor"/></svg>`;
const cover=`<section class="cover"><div class="edition">HOGWARTS · MDCCCXC</div><div><p>Il mutamento della materia</p><h1>Ars<span>Transfigurationis</span></h1><div class="seal">${seal}</div><p>Trattato scolastico di Trasfigurazione<br>Dai fondamenti all’identità della forma</p></div><div><div class="author">Edmund Valemont</div><div class="edition">Sette anni · Ventotto lezioni</div><button id="openBook">Apri il volume →</button><div class="imprint">NIGHTFALL · EDIZIONE PERSONALE</div></div></section>`;
pages.push({html:cover,title:'Copertina'});
function leaf(body,title,year=null){return {title,year,html:`<article class="page"><div class="running"><span>ARS TRANSFIGURATIONIS</span><span>${year?roman[year-1]+' ANNO':'EDMUND VALEMONT'}</span></div>${body}<div class="folio"><span>Hogwarts · 1890</span><span>__FOLIO__</span></div></article>`}}
pages.push(leaf(`<div class="kicker">AL LETTORE</div><h2>La forma cambia.<br>Lo studio rimane.</h2><p class="subtitle">Prefazione al volume personale</p><p class="initial">La Trasfigurazione comincia prima del gesto: comincia quando sappiamo osservare. Un buon trasfiguratore non impone alla materia un desiderio confuso; prepara un’immagine precisa e ne riconosce i limiti.</p><p>Questo volume accompagna sette annualità. Ogni anno si svolge in due settimane, con due lezioni per settimana: quattro incontri prima di procedere all’anno successivo.</p><p>La pagina di sinistra presenta i principi. Quella di destra li traduce in osservazione, progetto e attività guidata. Le risposte di ripasso sono consultabili dopo aver provato a ragionare da soli.</p><div class="callout"><strong>Il metodo di Valemont</strong>Osservare. Visualizzare. Eseguire con controllo. Confrontare il risultato. Correggere.</div><p class="source">Rielaborazione didattica del libro «Trasfigurazione» fornito per il progetto. Le attività sono proposte originali. Terminologia e modelli del riferimento sono adattati al contesto di Nightfall; riferimenti a eventi o personaggi posteriori al 1890 sono omessi. Gli argomenti avanzati non conferiscono automaticamente abilità al personaggio.</p><p class="subtitle">Edmund Valemont</p>`,'Prefazione'));
pages.push(leaf(`<div class="kicker">ORDINAMENTO DEL CORSO</div><h2>Due settimane.<br>Un anno di studio.</h2><p class="subtitle">Il medesimo ritmo per tutte le sette annualità</p><div class="plan-grid"><div class="plan-cell"><strong>Settimana I</strong>Lezione 1 · principi e osservazione<br>Lezione 2 · sviluppo e confronto</div><div class="plan-cell"><strong>Settimana II</strong>Lezione 3 · applicazione guidata<br>Lezione 4 · sintesi e ripasso</div></div><p>Con la quarta lezione si conclude il ciclo dell’annualità. Il percorso prosegue poi con la prima lezione dell’anno seguente.</p><h3>Un incontro di quindici minuti</h3><p>2 minuti per obiettivo e preparazione; 3 per la lettura guidata; 7 per esercizio, dimostrazione o caso; 3 per confronto e ripasso.</p><div class="callout"><strong>Un obiettivo per incontro</strong>Quando compaiono più formule, una sola attività è centrale. Le altre servono a confrontare effetti e difficoltà.</div><p>Le lezioni mancanti possono essere recuperate leggendo teoria e scheda operativa. Il ripasso è uno strumento di studio e non costituisce un esame finale.</p><p class="source">Indice per anno, ricerca, pagina singola e segnalibro sono disponibili nella barra superiore. La posizione si conserva solo sul dispositivo e nel browser in uso.</p>`,'Piano delle lezioni'));
YEARS.forEach((y,yi)=>{
 const year=yi+1;yearPages.push(pages.length);
 const annual=LESSONS.filter(l=>l.year===year);
 pages.push(leaf(`<div class="year-page"><div class="kicker">LIBER ${roman[yi]}</div><div class="year-number">${roman[yi]}</div><h2>${y.name}</h2><p class="subtitle">${y.goal}</p><div class="ornament">✧</div><div class="annual-plan">${annual.map(l=>`<button data-lesson="${l.id}"><small>SETTIMANA ${roman[l.week-1]} · LEZIONE ${l.meeting}</small>${l.title}</button>`).join('')}</div><p class="source">Due settimane · Due lezioni settimanali<br>Quattro incontri, poi l’anno successivo</p></div>`,`${roman[yi]} anno · ${y.name}`,year));
 annual.forEach(l=>{
  lessonPages[l.id]=pages.length;
  pages.push(leaf(`<div class="kicker">SETTIMANA ${roman[l.week-1]} · LEZIONE ${l.meeting} / 4</div><h2>${l.title}</h2><p class="subtitle">${l.subtitle}</p>${l.theory.map((p,i)=>`<p${i===0?' class="initial"':''}>${p}</p>`).join('')}<p class="source">Riferimento nel volume di partenza: p. ${l.source}.</p>`,`${roman[yi]} anno · Lezione ${l.meeting} · Teoria`,year));
  pages.push(leaf(`<div class="kicker">OFFICINA DELLA FORMA · ${String(l.id).padStart(2,'0')}</div><h2>Osservare.<br>Mettere alla prova.</h2><p class="subtitle">${l.title} · Attività guidata</p><div class="callout"><strong>Preparazione</strong>${l.materials}</div><ol>${l.steps.map(s=>`<li>${s}</li>`).join('')}</ol><div class="callout"><strong>Che cosa verificare</strong>${l.check}</div><h3>Una domanda di ripasso</h3><p>${l.question}</p><details><summary>Consulta il ragionamento</summary><p>${l.answer}</p></details><p class="source">${l.meeting===4?(year<7?'Concluso il ciclo delle due settimane, si prosegue con il '+roman[year]+' anno.':'Con questa lezione si conclude il percorso dei sette anni.'):'Prosegui con la lezione successiva della stessa annualità.'}</p>`,`${roman[yi]} anno · Lezione ${l.meeting} · Attività`,year));
 });
});
pages.push(leaf(`<div class="kicker">EX LIBRIS</div><h2>La materia attende<br>una mente precisa.</h2><div class="ornament">✧</div><p>Sette annualità. Quattordici settimane. Ventotto incontri per imparare a distinguere ciò che cambia da ciò che rimane.</p><p>Questo volume è dedicato allo studio e al gioco di ruolo nella Scuola di Magia e Stregoneria di Hogwarts di Nightfall.</p><p class="subtitle">Edmund Valemont</p><div class="callout"><strong>Colophon</strong>Testi rielaborati dal volume «Trasfigurazione». Piano delle lezioni, attività e veste editoriale preparati per questa edizione personale.</div><p class="source">Creato per NightFall da Razor.<br>Progetto amatoriale di roleplay, non ufficiale.</p>`,'Colophon'));
let explicitSingle=readStore('mode','auto')==='single';
let textLevel=Math.min(2,Math.max(0,Number(readStore('font','0'))||0));
let page=0;let lastFocus=null;let touchX=null;
function isSingle(){return explicitSingle||window.innerWidth<=850}
function clamp(n){return Math.max(0,Math.min(pages.length-1,Number(n)||0))}
function hashPage(){const m=location.hash.match(/^#p=(\d+)$/);return m?clamp(m[1]):null}
function spreadStart(n){if(n===2)return 1;for(const start of lessonPages){if(start!==undefined&&(n===start||n===start+1))return start}return n}
function displayCount(){return page===0||yearPages.includes(page)||page===pages.length-1||isSingle()?1:Math.min(2,pages.length-page)}
page=hashPage()??clamp(readStore('page','0'));
function alertNote(text){$('notice').textContent=text;$('notice').classList.add('show');clearTimeout(alertNote.timer);alertNote.timer=setTimeout(()=>$('notice').classList.remove('show'),2600)}
function render(animate=false){
 const single=isSingle();if(!single)page=spreadStart(page);const count=displayCount();
 $('book').className='book'+(single||count===1?' single':'')+(page===0?' cover-open':'')+(animate?' turn':'');
 $('book').innerHTML=pages.slice(page,page+count).map((p,i)=>p.html.replace('__FOLIO__',String(page+i))).join('');
 $('prev').disabled=page===0;$('next').disabled=page+count>=pages.length;
 $('position').textContent=page===0?'Copertina':`Pagina ${page}${count===2?'–'+(page+1):''} / ${pages.length-1}`;
 $('context').textContent=pages[page].title;
 $('mode').textContent=explicitSingle?'Doppia pagina':'Pagina singola';$('mode').setAttribute('aria-pressed',String(explicitSingle));
 $('mode').disabled=window.innerWidth<=850;$('mode').title=window.innerWidth<=850?'Su questo schermo la lettura è a pagina singola':'';
 document.documentElement.style.setProperty('--reading',(17+textLevel*2)+'px');
 $('font').textContent=textLevel===2?'A−':'A+';
 document.querySelectorAll('[data-year]').forEach(el=>el.setAttribute('aria-current',String(Number(el.dataset.year)===pages[page].year)));
 if($('openBook'))$('openBook').onclick=()=>go(1);
 document.querySelectorAll('[data-lesson]').forEach(el=>el.onclick=()=>{go(lessonPages[Number(el.dataset.lesson)]);closeIndex()});
 writeStore('page',page);history.replaceState(null,'','#p='+page);
}
function go(n){page=clamp(n);render(true);window.scrollTo({top:0,behavior:'instant'})}
function next(){if(!$('next').disabled)go(page+displayCount())}
function prev(){if(page)go(isSingle()?page-1:spreadStart(page-1))}
function closeIndex(){if($('drawer').hidden)return;$('drawer').hidden=true;$('shade').hidden=true;$('indexButton').setAttribute('aria-expanded','false');document.body.style.overflow='';if(lastFocus)lastFocus.focus()}
function openIndex(){lastFocus=document.activeElement;$('drawer').hidden=false;$('shade').hidden=false;$('indexButton').setAttribute('aria-expanded','true');document.body.style.overflow='hidden';$('search').focus()}
function indexContent(){const q=$('search').value.trim().toLocaleLowerCase('it');let matches=0;$('indexList').innerHTML=YEARS.map((y,yi)=>{const ls=LESSONS.filter(l=>l.year===yi+1&&[l.title,l.subtitle,...l.theory].join(' ').toLocaleLowerCase('it').includes(q));matches+=ls.length;return ls.length?`<h3>${roman[yi]} anno · ${y.name}</h3>${ls.map(l=>`<button data-lesson="${l.id}"><small>SETTIMANA ${roman[l.week-1]} · LEZIONE ${l.meeting}</small>${l.title}<small>${l.subtitle}</small></button>`).join('')}`:''}).join('');if(!matches)$('indexList').textContent='Nessuna lezione trovata. Prova con un’altra parola.';document.querySelectorAll('#indexList [data-lesson]').forEach(el=>el.onclick=()=>{go(lessonPages[Number(el.dataset.lesson)]);closeIndex()})}
$('prev').onclick=prev;$('next').onclick=next;$('indexButton').onclick=openIndex;$('closeIndex').onclick=closeIndex;$('shade').onclick=closeIndex;$('search').oninput=indexContent;
$('mode').onclick=()=>{explicitSingle=!explicitSingle;writeStore('mode',explicitSingle?'single':'double');render()};
$('font').onclick=()=>{textLevel=(textLevel+1)%3;writeStore('font',textLevel);render()};
$('bookmark').onclick=()=>alertNote(writeStore('bookmark',page)?'Segnalibro salvato a questa pagina.':'Il browser non consente di salvare il segnalibro.');
$('savedLink').onclick=()=>{const saved=readStore('bookmark');if(saved===null)alertNote('Non hai ancora salvato un segnalibro.');else{go(saved);closeIndex()}};
$('coverLink').onclick=()=>{go(0);closeIndex()};$('planLink').onclick=()=>{go(2);closeIndex()};
document.querySelector('.year-tabs').innerHTML=roman.map((r,i)=>`<button data-year="${i+1}" aria-label="Vai al ${r} anno">${r}</button>`).join('');
document.querySelectorAll('[data-year]').forEach(el=>el.onclick=()=>go(yearPages[Number(el.dataset.year)-1]));
document.querySelector('.brand').onclick=e=>{e.preventDefault();go(0)};
document.addEventListener('keydown',e=>{if(!$('drawer').hidden){if(e.key==='Escape')closeIndex();if(e.key==='Tab'){const els=[...$('drawer').querySelectorAll('button,input')].filter(el=>!el.disabled);const first=els[0],last=els[els.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}return}if(/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();next()}if(e.key==='ArrowLeft'){e.preventDefault();prev()}if(e.key==='Home'){e.preventDefault();go(0)}});
$('book').addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX},{passive:true});
$('book').addEventListener('touchend',e=>{if(touchX===null)return;const delta=e.changedTouches[0].clientX-touchX;touchX=null;if(Math.abs(delta)>85){delta<0?next():prev()}},{passive:true});
let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>render(),120)});
window.addEventListener('hashchange',()=>{const target=hashPage();if(target!==null&&target!==page){page=target;render()}});
indexContent();render();
