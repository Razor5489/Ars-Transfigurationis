"""Build the illustrated A4 leaves and reader data from the editable lessons."""
import json, re, math, subprocess
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT=Path(__file__).parent
DATA=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),vm=require('vm');let c={};vm.createContext(c);vm.runInContext(fs.readFileSync('content.js','utf8')+'\\n'+fs.readFileSync('server-lessons.js','utf8')+'\\nthis.out={years:YEARS,lessons:LESSONS}',c);process.stdout.write(JSON.stringify(c.out));"],cwd=ROOT))
OUT=ROOT/'pages';OUT.mkdir(exist_ok=True)
ROMAN=['I','II','III','IV','V','VI','VII'];PAGES=[];CHAPTERS=[];SECTIONS=[]
NOTES=json.loads((ROOT/'spell-notes.json').read_text())
SHEET_POSITIONS={};INDEX_ROWS=[];ANNUAL_ROWS=[];LESSON_POSITIONS={}
BOOK_TITLE='ARS TRANSFIGURATIONIS'
INK='#283b32';GOLD='#ac9258';MUTED='#8e8a76';PAPER='#f8f4e8';GREEN='#153f33'

def text(x,y,s,size=12,fill=INK,weight='',anchor='',italic=False):
    return f'<text x="{x}" y="{y}" font-family="Georgia, Times New Roman, serif" font-size="{size}" fill="{fill}"'+(f' font-weight="{weight}"' if weight else '')+(f' text-anchor="{anchor}"' if anchor else '')+(' font-style="italic"' if italic else '')+'>'+escape(str(s))+'</text>'

def lines(s,size=12,width=479,bold=False):
    words=s.split();result=[];current=''
    for w in words:
        t=(current+' '+w).strip()
        # Slightly conservative for Georgia on browsers without the same font.
        if stringWidth(t,'Times-Bold' if bold else 'Times-Roman',size)*1.08>width and current:
            result.append(current);current=w
        else:current=t
    if current:result.append(current)
    return result

class Leaf:
    def __init__(self,section,title,subtitle='',kind='theory'):
        self.section=section;self.title=title;self.subtitle=subtitle;self.kind=kind;self.parts=[];self.plain=[section,title,subtitle];self.y=109
        self.parts.append('<rect width="595" height="842" fill="'+PAPER+'"/><rect width="595" height="842" fill="url(#paper)" opacity=".17"/>')
        self.parts += [text(52,38,'ARS TRANSFIGURATIONIS',7,MUTED),text(543,38,section.upper(),7,MUTED,anchor='end'),'<path d="M52 48H543" stroke="'+GOLD+'" stroke-width=".7"/>']
        for line in lines(title,26,480,True):self.parts.append(text(52,self.y,line,26,GREEN,'bold'));self.y+=31
        self.y+=1
        if subtitle:self.paragraph(subtitle,11,MUTED,True,16);self.y+=8
    def paragraph(self,s,size=12,fill=INK,italic=False,leading=18):
        self.plain.append(s)
        for line in lines(s,size):
            self.parts.append(text(52,self.y,line,size,fill,italic=italic));self.y+=leading
        self.y+=12
    def heading(self,s):
        self.plain.append(s);self.y+=7
        for line in lines(s,15,480,True):self.parts.append(text(52,self.y,line,15,GREEN,'bold'));self.y+=20
        self.y+=4
    def box(self,label,s):
        ls=lines(s,11,449);height=39+len(ls)*16
        self.parts.append(f'<rect x="52" y="{self.y-12}" width="491" height="{height}" fill="#eee9d8"/><path d="M52 {self.y-12}v{height}" stroke="{GOLD}" stroke-width="1.5"/>')
        self.parts.append(text(66,self.y+3,label.upper(),8,GREEN,'bold'));self.y+=24
        for line in ls:self.parts.append(text(66,self.y,line,11));self.y+=16
        self.y+=22;self.plain.extend([label,s])
    def row(self,left,right):
        self.parts.append('<!--ROW:'+str(len(self.plain))+'-->')
        for line in lines(left,11,417):self.parts.append(text(60,self.y,line,11));self.y+=16
        self.parts.append(text(536,self.y-16,right,10,MUTED,anchor='end'))
        self.parts.append(f'<path d="M60 {self.y-8}H536" stroke="#c3b89b" stroke-dasharray="1 3" stroke-width=".4"/>');self.y+=12
        self.plain.append(left+' '+str(right))
    def finish(self,folio):
        if self.y>758:raise ValueError(f'Overflow {self.title}: {self.y}')
        return svg(''.join(self.parts)+f'<path d="M52 789H543" stroke="#c3b89b" stroke-width=".45"/>'+text(52,804,'MANUALE DIDATTICO DI TRASFIGURAZIONE',6.5,MUTED)+text(543,804,folio,8,MUTED,anchor='end'))

def svg(body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="595" height="842" viewBox="0 0 595 842"><defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><pattern id="paper" width="595" height="842" patternUnits="userSpaceOnUse"><rect width="595" height="842" filter="url(#grain)" opacity=".17"/></pattern><linearGradient id="leather"><stop stop-color="#072a22"/><stop offset=".12" stop-color="#19483b"/><stop offset=".6" stop-color="#103c30"/><stop offset="1" stop-color="#05261e"/></linearGradient></defs>'+body+'</svg>'

def add(leaf,chapter=None):
    idx=len(PAGES);folio=f'{idx+1:02}'
    if chapter:CHAPTERS.append({'title':chapter,'page':idx+1})
    artwork=leaf.finish(folio);name=f'page-{idx+1:02}.svg';(OUT/name).write_text(artwork)
    PAGES.append({'image':'pages/'+name,'text':'ARS TRANSFIGURATIONIS\n'+'\n'.join(leaf.plain),'title':leaf.title,'folio':folio,'kind':leaf.kind})
    return idx

def spell_sheet(item,section):
    p=Leaf(section,item['name'],'La formula · Effetto e nozioni per la lezione',kind='spell')
    p.paragraph(item['mode'],9,MUTED,True,13)
    for label,key in [('Che cosa fa','effect'),('Nozioni da spiegare','notions'),('Esempio da discutere in aula','example')]:
        p.heading(label);p.paragraph(item[key],12,leading=18)
    p.heading('Domanda alla classe');p.paragraph(item['question'],11.5,leading=17)
    p.box('Risposta ragionata',item['answer'])
    SHEET_POSITIONS[item['name']]=len(PAGES)+1
    add(p,item['name']+' · Effetto e nozioni')

def cover(back=False):
    body='<rect width="595" height="842" fill="url(#leather)"/><rect width="595" height="842" fill="url(#paper)" opacity=".22"/>'
    for inset in [21,28,35]:body+=f'<rect x="{inset}" y="{inset}" width="{595-2*inset}" height="{842-2*inset}" fill="none" stroke="#aa9256" stroke-width="{.8 if inset==21 else .4}"/>'
    for x in [35,560]:
        for y in [35,807]:body+=f'<circle cx="{x}" cy="{y}" r="2.5" fill="none" stroke="{GOLD}" stroke-width=".6"/>'
    body+=text(297.5,84,'HOGWARTS · TRASFIGURAZIONE',9,GOLD,anchor='middle')
    body+=text(297.5,175,'ARS',36,'#eee4c9','bold','middle')+text(297.5,219,'TRANSFIGURATIONIS',31,'#eee4c9','bold','middle')
    body+=text(297.5,255,'Tractatus de Arte Transfigurationis',15,'#d9cda8',anchor='middle',italic=True)+'<path d="M205 282H390" stroke="'+GOLD+'" stroke-width=".6"/>'
    body+='<g fill="none" stroke="'+GOLD+'" stroke-width=".8"><circle cx="297.5" cy="422" r="90"/><circle cx="297.5" cy="422" r="82"/><path d="M297 469V383M297 407C234 323 208 391 262 427C209 456 262 501 297 444M298 407C361 323 387 391 333 427C386 456 333 501 298 444M298 386l-14-19m14 19 14-19M228 525l140-192"/><path d="m363 338 4-18 4 12 13 4-14 3-4 13z"/></g>'
    if back:
        body+=text(297.5,605,'La forma muta. Il metodo rimane.',16,'#e1d6b9',anchor='middle',italic=True)+text(297.5,669,'EDMUND VALEMONT',14,'#e1d6b9',anchor='middle')
    else:
        body+=text(297.5,616,'AD USUM SCHOLASTICUM HOGVARTENSE',9,GOLD,anchor='middle')+text(297.5,683,'Professor Edmund Valemont',17,'#e1d6b9',anchor='middle')+text(297.5,753,'OSSERVAZIONE · PRECISIONE · CONTROLLO',9,GOLD,anchor='middle')
    body+=text(297.5,790,'MDCCCXC',11,GOLD,anchor='middle')
    name='page-'+f'{len(PAGES)+1:02}'+'.svg';(OUT/name).write_text(svg(body));PAGES.append({'image':'pages/'+name,'text':'ARS TRANSFIGURATIONIS\n'+('Quarta di copertina' if back else 'Tractatus de Arte Transfigurationis')+'\nEdmund Valemont\nHogwarts · 1890','title':'Quarta di copertina' if back else 'Copertina','folio':'Quarta di copertina' if back else 'Copertina','kind':'cover'})

cover();CHAPTERS.append({'title':'Copertina','page':1})
p=Leaf('Praefatio','L’arte della forma','Prefazione di Edmund Valemont')
p.paragraph('La Trasfigurazione comincia prima del gesto: comincia quando sappiamo osservare. Un buon trasfiguratore non impone alla materia un desiderio confuso; prepara un’immagine precisa e ne riconosce i limiti.')
p.paragraph('Questo volume accompagna sette annualità. Ogni anno si svolge in due settimane, con due lezioni per settimana: quattro incontri prima di procedere all’anno successivo.')
p.heading('Il metodo comune')
p.paragraph('Le pagine teoriche introducono principi e formule. La scheda successiva organizza preparazione, attività e controllo. Ogni incontro ha un obiettivo riconoscibile e termina con una domanda ragionata.')
p.box('La sequenza di lavoro','Osservare. Visualizzare. Eseguire con controllo. Confrontare. Correggere.')
p.paragraph('La teoria non conferisce automaticamente abilità speciali. Gli argomenti avanzati si affrontano secondo la preparazione degli allievi e le indicazioni della scuola.')
p.paragraph('Edmund Valemont',13,GREEN,True)
add(p,'Praefatio')

p=Leaf('Tabula Materiarum','Indice del volume','Sette anni, un solo metodo.')
add(p,'Indice del volume');SECTIONS.append(['Indice',2])
p=Leaf('Cursus Septem Annorum','Due settimane per anno','Il ritmo didattico del volume')
p.heading('Settimana I');p.paragraph('Lezione 1: principi e osservazione. Lezione 2: sviluppo e confronto. Ogni incontro presenta una pratica centrale o un caso da interpretare.')
p.heading('Settimana II');p.paragraph('Lezione 3: applicazione guidata. Lezione 4: sintesi e ripasso. Concluso il quarto incontro, si prosegue con la prima lezione dell’anno successivo.')
p.box('Quindici minuti','2 minuti per obiettivo e preparazione; 3 per la lettura guidata; 7 per attività o dimostrazione; 3 per confronto e ripasso.')
p.heading('Conoscenza e applicazione');p.paragraph('Il programma conserva nome, materia e anno delle formule documentate dalla scuola. Le attività del libro accompagnano l’insegnamento senza inventare meccaniche, durate o potenziamenti.')
p.paragraph('Le lezioni mancanti possono essere recuperate consultando teoria e scheda operativa. Non è previsto un esame finale.',11)
add(p,'Il percorso delle due settimane')
p=Leaf('Fondamenti','I cinque parametri','Visualizzare prima di trasformare')
for h,s in [('Spazio','Altezza, larghezza e profondità del risultato. Una dimensione prevista permette di distinguere il progetto da una crescita incontrollata.'),('Struttura','Forma, consistenza e organizzazione delle parti. Cambiare materiale è diverso da cambiare colore.'),('Colore e tonalità','La tinta generale va distinta da sfumature, luminosità e dettagli. Una superficie uniforme non equivale a un rivestimento ricco di particolari.'),('Essenza','Nel modello del riferimento rimane l’identità originaria del soggetto. Una forma animale apparente non dimostra la creazione di vita naturale.')]:p.heading(h);p.paragraph(s)
p.box('Concentrazione','Mantiene stabile il progetto mentale e sostiene l’esecuzione; non è un sesto parametro.')
add(p,'Fondamenti · I cinque parametri');SECTIONS.append(['Fondamenti',4])

for yi,y in enumerate(DATA['years']):
    year=yi+1;annual=[l for l in DATA['lessons'] if l['year']==year];idx=len(PAGES)
    p=Leaf('Anno '+ROMAN[yi],y['name'],'Annus '+['Primus','Secundus','Tertius','Quartus','Quintus','Sextus','Septimus'][yi],kind='divider')
    p.y+=36;p.parts.append(text(297.5,p.y,ROMAN[yi],100,GREEN,anchor='middle'));p.y+=60
    p.paragraph(y['goal'],16,GREEN,True,24)
    p.box('Il ciclo dell’annualità','Due settimane. Due lezioni ogni settimana. Quattro incontri. Le schede delle formule sono letture della stessa lezione, non incontri aggiuntivi.')
    if year==1:p.paragraph('Le formule del primo anno: Colovaria, Aguamenti, Avis.',13,GREEN)
    add(p,'Anno '+ROMAN[yi]+' · '+y['name']);SECTIONS.append([ROMAN[yi],idx])
    p=Leaf('Anno '+ROMAN[yi],'Il programma dell’anno','Due settimane · Quattro lezioni')
    for li,l in enumerate(annual):
        if li%2==0:p.heading('Settimana '+ROMAN[li//2])
        p.row(f"Lezione {l['meeting']} · {l['title']}",f'{idx+3+li*2:02}')
        p.paragraph(l['subtitle'],10,MUTED,True,15)
    p.box('Traguardo',y['goal']);p.paragraph('Leggere la teoria, preparare il compito e confrontare il risultato. La quarta lezione chiude il ciclo e raccoglie il ripasso dell’annualità.',11)
    ANNUAL_ROWS.append((len(PAGES),year))
    add(p)
    for l in annual:
        LESSON_POSITIONS[(year,l['meeting'])]=len(PAGES)+1
        p=Leaf(f"Anno {ROMAN[yi]} · Settimana {ROMAN[l['week']-1]}",l['title'],l['subtitle'])
        p.parts.insert(3,text(52,72,f"LECTIO {l['meeting']} · TEORIA",8,GOLD))
        for paragraph in l['theory']:p.paragraph(paragraph)
        p.box('Obiettivo',l['check']);p.paragraph('Riferimento: '+l['source'],8.5,MUTED,False,12)
        add(p,f"{ROMAN[yi]}.{l['meeting']} · {l['title']}")
        for note in NOTES:
            if note['lesson']==(year-1)*4+l['meeting']-1:
                spell_sheet(note,f"Anno {ROMAN[yi]} · Lectio {l['meeting']}")
        p=Leaf(f"Anno {ROMAN[yi]} · Lectio {l['meeting']}",'L’esercizio e il giudizio',l['title']+' · Scheda operativa')
        p.box('Preparazione',l['materials'])
        for i,s in enumerate(l['steps']):p.paragraph(f'{i+1}. '+s,11.5,leading=17)
        p.box('Controllo',l['check']);p.heading('Domanda di ripasso');p.paragraph(l['question'],11.5,leading=17)
        p.heading('Ragionamento');p.paragraph(l['answer'],11,leading=16)
        if l['meeting']==4:p.paragraph('Fine del ciclo di due settimane. '+('Si prosegue con il '+ROMAN[year]+' anno.' if year<7 else 'Il percorso dei sette anni è concluso.'),9,GOLD)
        add(p)
        PAGES[-1]['title']=l['title']+' · Esercizio e ripasso'

p=Leaf('Lexicon','Il lessico della forma','Parole da usare con precisione')
for h,s in [('Trasfigurazione','Modifica di un bersaglio presente secondo un risultato progettato.'),('Evocazione','Apparizione di un risultato temporaneo; non equivale alla creazione illimitata di vita o risorse.'),('Animazione','Movimento imposto a un manufatto, senza attribuirgli volontà autonoma.'),('Detrasfigurazione','Ripristino o correzione di un effetto trasfigurativo.'),('Potenza, durata, efficacia','Coesione della forma, tempo dell’effetto e corrispondenza al progetto sono criteri distinti.'),('Chartanimus','Esempio complementare del riferimento: una figura animale di carta conserva l’essenza cartacea. Non sostituisce le tre formule del primo anno assegnate dalla scuola.')]:p.heading(h);p.paragraph(s,11.5,leading=17)
add(p,'Lessico essenziale');SECTIONS.append(['Lessico',75])
p=Leaf('Appendice · Ordinamento','Le formule del primo anno','L’insegnamento della scuola e la struttura del volume')
p.heading('Lezioni di Trasfigurazione');p.paragraph('Colovaria, Aguamenti e Avis risultano assegnati al primo anno nelle lezioni della scuola. La prima settimana prepara il metodo e il mutamento cromatico; la seconda affronta Aguamenti e Avis, con il ripasso dei limiti.')
p.heading('Il ruolo del riferimento');p.paragraph('Il libro «Trasfigurazione» costituisce la base teorica. Le lezioni della scuola definiscono invece la collocazione delle formule nel programma. Avis viene anticipato al primo anno; il confronto con Avifors resta un approfondimento successivo.')
p.heading('Edizione e attribuzione');p.paragraph('Ars Transfigurationis è un volume personale di Edmund Valemont, preparato per l’esperienza roleplay di NightFall. Le attività sono proposte didattiche originali. I riferimenti a personaggi o avvenimenti posteriori al 1890 sono esclusi.')
p.paragraph('Creato per NightFall da Razor. Progetto amatoriale, non ufficiale.',10,MUTED)
add(p,'Lezioni della scuola');SECTIONS.append(['Appendice',76])
supplements=[n for n in NOTES if n['lesson'] is None]
if supplements:
    SECTIONS.append(['Formule',len(PAGES)])
    for note in supplements:spell_sheet(note,'Repertorio · '+note['mode'].split(' · ')[0])
p=Leaf('Finis','La forma muta.','Il metodo rimane.')
p.y=370;p.paragraph('Sette annualità. Quattordici settimane. Ventotto lezioni per distinguere ciò che cambia da ciò che rimane.',19,GREEN,True,29)
p.y+=55;p.paragraph('Edmund Valemont',15,GREEN);p.paragraph('Hogwarts · MDCCCXC',10,GOLD)
add(p,'Finis')
idx=len(PAGES);name=f'page-{idx+1:02}.svg';body='<rect width="595" height="842" fill="#0d3027"/>'
for i in range(38):
    yy=i*24;body+=f'<path d="M-40 {yy} Q130 {yy-80} 298 {yy+9}T650 {yy-5}" fill="none" stroke="{["#9a8659","#6c855d","#38584a"][i%3]}" stroke-width="{1+i%4}" opacity=".5"/>'
(OUT/name).write_text(svg(body));PAGES.append({'image':'pages/'+name,'text':'Controguardia posteriore marmorizzata.','title':'Controguardia posteriore','folio':'Controguardia','kind':'endpaper'})
cover(True)
assert len(DATA['lessons'])==28
assert len(SHEET_POSITIONS)==len(NOTES)
# Resolve printed tables after every inserted sheet has its final folio.
chapter_pages={c['title']:c['page'] for c in CHAPTERS}
original_sections={'Indice':'Indice del volume','Fondamenti':next(c['title'] for c in CHAPTERS if c['title'].startswith('Fondamenti ·')),'Lessico':'Lessico essenziale'}
for section in SECTIONS:
    label=section[0]
    if label in ROMAN:section[1]=chapter_pages['Anno '+label+' · '+DATA['years'][ROMAN.index(label)]['name']]-1
    elif label in original_sections:section[1]=chapter_pages[original_sections[label]]-1
    elif label=='Materie':section[1]=chapter_pages['Incantesimi · Tavola per anno']-1
    elif label=='Appendice':section[1]=chapter_pages['Lezioni della scuola']-1

def replace_leaf(index,leaf):
    old=PAGES[index];folio=f'{index+1:02}'
    (OUT/f'page-{index+1:02}.svg').write_text(leaf.finish(folio))
    old['text']=BOOK_TITLE+'\n'+'\n'.join(leaf.plain)
    old['title']=leaf.title

for index,year in ANNUAL_ROWS:
    y=DATA['years'][year-1];annual=[l for l in DATA['lessons'] if l['year']==year]
    p=Leaf('Anno '+ROMAN[year-1],'Il programma dell’anno','Due settimane · Quattro lezioni')
    for li,l in enumerate(annual):
        if li%2==0:p.heading('Settimana '+ROMAN[li//2])
        p.row(f"Lezione {l['meeting']} · {l['title']}",str(LESSON_POSITIONS[(year,l['meeting'])]))
        p.paragraph(l['subtitle'],10,MUTED,True,15)
    p.box('Traguardo',y['goal'])
    p.paragraph('Ogni incontro comprende teoria, spiegazione delle formule ed esercizio. Le schede aggiunte appartengono alla stessa lezione. Dopo il quarto incontro si passa all’anno successivo.',11)
    replace_leaf(index,p)

p=Leaf('Tabula Materiarum','Indice del volume','Sette anni · Ventotto lezioni')
for title in ['Praefatio','Il percorso delle due settimane',original_sections['Fondamenti']]+['Anno '+ROMAN[i]+' · '+y['name'] for i,y in enumerate(DATA['years'])]+['Lessico essenziale']:
    p.row('Prefazione' if title=='Praefatio' else title,str(chapter_pages[title]))
supplement_start=next((c['page'] for c in CHAPTERS if c['title'].endswith(' · Effetto e nozioni') and c['page']>chapter_pages['Lessico essenziale']),None)
if supplement_start:p.row('Repertorio delle formule · Schede distinte',str(supplement_start))
p.row('Finis',str(chapter_pages['Finis']))
p.paragraph('Le schede delle formule si trovano nelle rispettive lezioni. Il repertorio raccoglie le voci complementari. L’indice ricercabile permette di trovare ogni incantesimo per nome.',10,MUTED)
replace_leaf(2,p)
for item in PAGES:item['image']+='?v=20261118-nozioni1'
(ROOT/'book-data.json').write_text(json.dumps({'pages':PAGES,'chapters':CHAPTERS,'sections':SECTIONS},ensure_ascii=False,indent=2))
index=ROOT/'index.html'
if index.exists() and 'id="book-data"' in index.read_text():
    packed=json.dumps({'pages':PAGES,'chapters':CHAPTERS,'sections':SECTIONS},ensure_ascii=False).replace('</','<\\/')
    index.write_text(re.sub(r'(<script id="book-data" type="application/json">).*?(</script>)',lambda m:m[1]+packed+m[2],index.read_text(),flags=re.S))
print(f'{len(PAGES)} pagine A4, {len(DATA["lessons"])} lezioni. Nessun testo supera il margine inferiore.')
