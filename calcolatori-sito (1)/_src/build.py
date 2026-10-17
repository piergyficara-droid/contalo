#!/usr/bin/env python3
# Rigenera tutte le pagine HTML del sito:  python3 _src/build.py
# Per aggiungere un calcolatore: nuova riga in K + una funzione in app.js (oggetto C).
import json,os
NAME='Contalo'
BASE=''  # dopo aver comprato il dominio: 'https://tuodominio.it' (senza / finale) -> attiva canonical, sitemap e robots
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230b3c5d'/%3E%3Ccircle cx='16' cy='16' r='7' fill='none' stroke='%23ffd23f' stroke-width='4'/%3E%3C/svg%3E"
LOGO='<svg width=30 height=30 viewBox="0 0 32 32" aria-hidden=true><rect width=32 height=32 rx=8 fill=#0b3c5d /><circle cx=16 cy=16 r=7 fill=none stroke=#ffd23f stroke-width=4 /></svg>'
RING='<svg viewBox="0 0 36 36" aria-hidden=true><circle cx=18 cy=18 r=15.915 fill=none stroke=#ffd23f stroke-width=4.5 /><circle cx=18 cy=18 r=15.915 fill=none stroke=#19b5c8 stroke-width=4.5 stroke-dasharray="68 32" transform="rotate(-90 18 18)"/></svg>'
# (id, slug, nome breve, h1, icona, descrizione card, meta description, campi, spiegazione, FAQ)
# campo numerico: (id, etichetta, min, max-slider|None, step, default, unità) - select: (id, etichetta, [(valore, testo)])
K=[
('mutuo','calcolo-rata-mutuo','Mutuo','Calcolo rata mutuo','⌂','Rata mensile, interessi e costo totale del tuo mutuo.','Calcola la rata mensile del mutuo, gli interessi totali e quanto restituirai alla banca. Gratis, senza registrazione.',
 [('p','Importo del mutuo',20000,600000,1000,150000,'€'),('y','Durata',5,40,1,25,'anni'),('t','Tasso TAN',0,10,0.1,3.5,'%')],
 'La rata si calcola con l’ammortamento alla francese: resta costante per tutta la durata, ma all’inizio paghi più interessi e meno capitale. Il calcolo usa il tasso TAN diviso 12 e il numero totale di mesi.',
 [('Che differenza c’è tra TAN e TAEG?','Il TAN è il tasso d’interesse puro. Il TAEG include anche spese e costi accessori, quindi dice meglio quanto costa davvero il mutuo.'),('Il calcolo vale per tasso fisso e variabile?','È pensato per il tasso fisso. Con il variabile la rata cambia nel tempo: il risultato è una stima basata sul tasso di oggi.')]),
('prestito','calcolo-rata-prestito','Prestito','Calcolo rata prestito personale','€','Rata e costo totale di un finanziamento.','Calcola la rata mensile del tuo prestito personale e il costo totale degli interessi. Gratis e immediato.',
 [('p','Importo richiesto',1000,60000,500,10000,'€'),('n','Durata',6,120,6,48,'mesi'),('t','Tasso TAN',0,20,0.1,8,'%')],
 'La rata è fissa e comprende capitale e interessi: più la durata è lunga, più la rata scende ma più interessi paghi in totale. Confronta sempre il TAEG, che include anche le spese di istruttoria.',
 [('Meglio una rata bassa o una durata breve?','Una durata breve costa meno in interessi, ma la rata è più alta. Scegli la rata più alta che puoi sostenere senza stress.'),('Il calcolo comprende le spese?','No: usa solo il TAN. Spese di istruttoria e assicurazioni aumentano il costo reale, quindi guarda il TAEG.')]),
('interessi','calcolatore-interessi-composti','Interessi composti','Calcolatore interessi composti','↗','Quanto cresce un capitale nel tempo, con versamenti mensili.','Calcola quanto crescerà il tuo capitale con gli interessi composti e i versamenti mensili. Gratis e immediato.',
 [('c','Capitale iniziale',0,200000,500,5000,'€'),('v','Versamento mensile',0,2000,10,200,'€'),('t','Rendimento annuo',0,12,0.1,4,'%'),('y','Durata',1,40,1,20,'anni')],
 'Gli interessi composti si calcolano anche sugli interessi già maturati: ogni mese il capitale cresce e il mese dopo rende di più. Più anni passano, più l’effetto si nota. Qui la capitalizzazione è mensile.',
 [('Il rendimento è garantito?','No. Il rendimento è un’ipotesi che inserisci tu: nella realtà cambia da prodotto a prodotto e nel tempo.'),('Il risultato è al netto delle tasse?','No. Il calcolo è al lordo di tasse, costi e inflazione, quindi il valore reale sarà più basso.')]),
('obiettivo','calcolo-risparmio-obiettivo','Obiettivo di risparmio','Risparmio mensile per un obiettivo','◎','Quanto mettere da parte ogni mese per arrivare a una cifra.','Scopri quanto risparmiare ogni mese per raggiungere il tuo obiettivo in un certo numero di anni. Gratis e immediato.',
 [('g','Obiettivo da raggiungere',1000,500000,1000,30000,'€'),('y','Tempo a disposizione',1,40,1,8,'anni'),('t','Rendimento annuo',0,10,0.1,3,'%'),('c','Capitale già disponibile',0,200000,500,0,'€')],
 'Il calcolo trova il versamento mensile costante che, con il rendimento indicato, ti porta all’obiettivo nel tempo scelto. Più anni hai a disposizione, meno devi versare ogni mese.',
 [('Posso contare su un rendimento garantito?','No: è un’ipotesi. Con rendimento 0% il calcolo divide semplicemente l’obiettivo per il numero di mesi.'),('Il risultato tiene conto dell’inflazione?','No. Con l’inflazione l’obiettivo di oggi varrà meno tra qualche anno: per sicurezza punta un po’ più in alto.')]),
('iva','scorporo-iva','Scorporo IVA','Scorporo e calcolo IVA','%','Dal prezzo lordo all’imponibile, e viceversa.','Scorpora l’IVA da un importo o aggiungila al netto. Aliquote italiane 22%, 10%, 5% e 4%. Gratis e immediato.',
 [('a','Importo',0,None,10,1000,'€'),('al','Aliquota IVA',[('22','22% (ordinaria)'),('10','10%'),('5','5%'),('4','4%')]),('m','Cosa vuoi fare',[('s','Scorporo: l’importo comprende l’IVA'),('a','Aggiungi IVA: l’importo è al netto')])],
 'Per scorporare l’IVA si divide il prezzo per 1 più l’aliquota (1,22 per il 22%): il risultato è l’imponibile. L’IVA è la differenza tra prezzo e imponibile.',
 [('Quali sono le aliquote IVA in Italia?','L’aliquota ordinaria è il 22%. Quelle ridotte sono il 10%, il 5% e il 4%, e valgono solo per specifici beni e servizi.'),('Che differenza c’è tra imponibile e totale?','L’imponibile è l’importo senza IVA. Il totale è l’imponibile più l’IVA.')]),
('percentuale','calcolo-percentuale','Percentuali','Calcolo percentuale','÷','Percentuali, sconti e variazioni in un attimo.','Calcola percentuali, sconti e variazioni percentuali online: quanto fa il X% di Y, X su Y, aumento o calo. Gratis.',
 [('m','Cosa vuoi calcolare',[('a','Quanto fa il X% di Y'),('b','X è quanto % di Y'),('c','Variazione % da X a Y')]),('x','Valore X',0,None,0.01,20,''),('y','Valore Y',0,None,0.01,150,'')],
 'Per trovare il X% di Y si moltiplica Y per X e si divide per 100. Per sapere quanto è X rispetto a Y si divide X per Y e si moltiplica per 100. La variazione è la differenza tra Y e X divisa per X.',
 [('Come si calcola uno sconto?','Scegli «Quanto fa il X% di Y»: Y è il prezzo, X lo sconto. Il valore «meno il X%» è il prezzo scontato.'),('Come si calcola un aumento percentuale?','Scegli «Variazione % da X a Y»: X è il valore iniziale e Y quello finale.')]),
]
def field(f):
    i,l=f[0],f[1]
    if isinstance(f[2],list):
        o=''.join(f'<option value={a}>{b}</option>' for a,b in f[2])
        return f'<div class=f><label for={i}>{l}</label><select id={i}>{o}</select></div>'
    lo,hi,st,d,u=f[2:]
    s=f'<input type=range aria-label="{l}" data-for={i} min={lo} max={hi} step={st} value={d}>' if hi else ''
    return f'<div class=f><label for={i}>{l}<span>{u}</span></label><div class=in><input id={i} type=number inputmode=decimal min={lo} step={st} value={d}>{s}</div></div>'
def tile(k): return f'<a class=tile href={k[1]}.html><span class=ic>{k[4]}</span><span><b>{k[2]}</b><small>{k[5]}</small></span></a>'
def page(f,t,d,body,c='',ld='',cur=''):
    nav=''.join(f'<a href={k[1]}.html{" aria-current=page" if k[0]==cur else ""}>{k[2]}</a>' for k in K)
    can=f'<link rel=canonical href="{BASE}/{f}">' if BASE else ''
    ldt=f'<script type="application/ld+json">{ld}</script>' if ld else ''
    dc=f' data-c={c}' if c else ''
    h=f'''<!doctype html><html lang=it><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=theme-color content="#eef4f6" media="(prefers-color-scheme:light)"><meta name=theme-color content="#09161d" media="(prefers-color-scheme:dark)">
<title>{t}</title><meta name=description content="{d}">{can}
<meta property=og:title content="{t}"><meta property=og:description content="{d}"><meta property=og:type content=website>
<link rel=icon href="{FAV}"><link rel=stylesheet href=style.css>{ldt}
<script src=config.js></script><script src=app.js defer></script></head>
<body{dc}>
<div class=top><a class=logo href=index.html>{LOGO}{NAME}</a></div>
<nav class=chips aria-label="Calcolatori">{nav}</nav>
<main>{body}</main>
<footer>I risultati sono indicativi e non costituiscono consulenza finanziaria, fiscale o legale. <a href=privacy.html>Privacy e cookie</a> · © {NAME}</footer></body></html>'''
    open(os.path.join(R,f),'w',encoding='utf-8').write(h)
for k in K:
    i,s,sh,h1,g,card,meta,fl,ex,fq=k
    ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in fq]},ensure_ascii=False)
    rel=''.join(tile(x) for x in K if x[0]!=i)
    faq=''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in fq)
    body=f'''<h1>{h1}</h1><p class=lead>{card}</p>
<div class=app><section class=hero aria-live=polite><div id=out></div><button type=button id=sh>Condividi risultato</button></section>
<form class=card onsubmit="return false">{''.join(field(x) for x in fl)}</form></div>
<div class=aff data-s={i}></div><div class=ad data-s=top></div>
<article><h2>Come funziona</h2><p>{ex}</p><h2>Domande frequenti</h2>{faq}</article>
<div class=ad data-s=mid></div>
<h2>Altri calcolatori</h2><div class=grid>{rel}</div><div class=ad data-s=end></div>'''
    page(s+'.html',f'{h1} online gratis | {NAME}',meta,body,i,ld,i)
page('index.html',f'{NAME}: calcolatori online gratuiti (mutuo, prestito, IVA)','Calcolatori online gratuiti e senza registrazione: rata del mutuo, prestito personale, interessi composti, scorporo IVA e percentuali.',
 f'<section class="hero home"><div><h1>Fai i conti in 10 secondi</h1><p class=lead>Mutuo, prestito, risparmio e IVA: calcolatori gratuiti, senza registrazione, pensati per funzionare benissimo anche da telefono.</p></div>{RING}</section><div class=grid>{"".join(tile(k) for k in K)}</div><div class=ad data-s=mid></div>')
page('privacy.html',f'Privacy e cookie | {NAME}','Informativa su privacy, cookie, pubblicità e link di affiliazione.',
 '<h1>Privacy e cookie</h1><article><p>Questo sito non richiede registrazione e non raccoglie dati personali: i calcoli avvengono nel tuo browser e non vengono inviati a nessun server.</p><h2>Pubblicità</h2><p>Il sito può mostrare annunci di Google AdSense. Google e i suoi partner possono usare cookie e identificatori per mostrare annunci personalizzati e misurarne i risultati, secondo la <a href="https://policies.google.com/technologies/ads">loro informativa</a>. Puoi scegliere o revocare il consenso dal messaggio cookie del sito e dalle impostazioni annunci di Google.</p><h2>Link di affiliazione</h2><p>Alcuni link sono sponsorizzati: se acquisti un servizio o richiedi un preventivo, il sito può ricevere una commissione, senza costi extra per te.</p><h2>Titolare</h2><p>[Inserisci qui nome e email di contatto]</p></article>')
if BASE:
    u=['index.html']+[k[1]+'.html' for k in K]+['privacy.html']
    open(os.path.join(R,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}/{x}</loc></url>' for x in u)+'</urlset>')
    open(os.path.join(R,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
