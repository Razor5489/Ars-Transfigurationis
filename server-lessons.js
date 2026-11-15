// Integrazione richiesta il 15 novembre 2026. Le schermate del server
// prevalgono sulla suddivisione per anno proposta nel PDF di riferimento.
const FIRST_YEAR = [
 {title:'La disciplina della forma',subtitle:'Fondamenti, concentrazione e cinque parametri',
 theory:[
 'La Trasfigurazione modifica la forma e le proprietà della materia attraverso un progetto preciso. Prima di impugnare la bacchetta, il trasfiguratore osserva lo stato iniziale, definisce il risultato e decide come verificarlo. Una somiglianza approssimativa non basta: il risultato deve corrispondere all’intenzione.',
 'Cinque parametri guidano la visualizzazione. Lo spazio descrive le dimensioni; la struttura comprende forma e consistenza; il colore identifica la tinta; la tonalità ne definisce sfumature e luminosità. L’essenza, nel modello del manuale, rimane quella del soggetto originario. La concentrazione governa questi parametri, senza costituirne un sesto.',
 'Il primo anno introduce Colovaria, Aguamenti e Avis, secondo l’assegnazione delle lezioni della scuola. Il percorso procede dall’osservazione alla variazione cromatica, quindi all’acqua e alle forme aviarie. Non si aggiungono costi, tempi o vantaggi magici che non siano descritti dall’insegnamento effettivo.'
 ],materials:'Un oggetto semplice, una pergamena e una scheda dei cinque parametri.',
 steps:['Descrivi dimensioni, forma, consistenza e tinta del bersaglio senza modificarlo.','Compila cinque righe, una per parametro; distingui ciò che cambia da ciò che deve restare invariato.','Progetta una modifica del solo colore e confrontala con una modifica della struttura.'],
 check:'Lo studente distingue i cinque parametri e presenta un risultato atteso che il docente possa verificare.',
 question:'Una scatola diventa blu senza cambiare forma: quale parametro è stato modificato?',
 answer:'Il colore. Dimensioni e struttura devono rimanere quelle previste; la tonalità va confrontata con la finitura richiesta.',source:'2–3, fondamenti. Ordinamento delle formule: lezioni della scuola, primo anno.'},
 {title:'Colovaria',subtitle:'Il governo del colore',
 theory:[
 'Colovaria è la formula dedicata al mutamento cromatico. L’esercizio comincia scegliendo una tinta riconoscibile su un oggetto semplice: una sola modifica permette di osservare il risultato senza confonderlo con cambiamenti di forma o dimensione.',
 'Colore e tonalità devono essere distinti. Il colore è la tinta generale; la tonalità riguarda gradazioni, luminosità e sfumature. Un oggetto può assumere il colore desiderato e conservare tuttavia zone irregolari, che richiedono una nuova osservazione prima di ripetere il tentativo.',
 'La formula è collocata al primo anno nelle lezioni della scuola. La pratica conserva il bersaglio iniziale e modifica soltanto quanto stabilito con il docente. Non si deducono dalla variazione cromatica cambiamenti di materiale, poteri aggiuntivi o durata illimitata. Gesto e pronuncia vengono appresi nella dimostrazione.'
 ],materials:'Un oggetto neutro predisposto dal docente e un riferimento cromatico.',
 steps:['Annota il colore iniziale e scegli una tinta finale precisa.','Visualizza la colorazione, mantenendo invariati spazio e struttura; esegui Colovaria secondo la dimostrazione.','Confronta le diverse superfici del risultato e descrivi eventuali zone rimaste del colore iniziale.'],
 check:'La tinta corrisponde al progetto, la superficie è coerente e il bersaglio conserva forma e dimensioni.',
 question:'Un oggetto cambia colore ma diventa anche più grande: il progetto cromatico è stato rispettato?',
 answer:'No. Un cambiamento di spazio non previsto costituisce una deviazione, anche quando la tinta è corretta.',source:'2–3, parametri. Formula e anno: lezioni della scuola, voce Colovaria.'},
 {title:'Aguamenti',subtitle:'Acqua, direzione e controllo',
 theory:[
 'Aguamenti viene studiato nel primo anno di Trasfigurazione, come stabilito dalle lezioni della scuola. La formula è associata alla produzione di acqua: il suo uso didattico mette al centro la direzione dell’effetto e la capacità di mantenere il controllo sul risultato.',
 'Il lavoro si prepara con un recipiente e una zona sgombra. La destinazione dell’acqua deve essere individuata prima dell’esecuzione; la supervisione del docente accompagna avvio, controllo e conclusione dell’effetto. Non occorre aumentare la quantità per dimostrare una migliore padronanza.',
 'Questo incontro collega l’osservazione ai limiti della magia. La presenza di acqua non consente di attribuire alla formula proprietà curative o potenziamenti non descritti. Pronuncia, gesto e controllo dell’intensità si apprendono nella dimostrazione del docente: il progetto deve restare commisurato al compito assegnato.'
 ],materials:'Recipiente predisposto dal docente e spazio di lavoro libero.',
 steps:['Definisci il punto d’arrivo dell’acqua e controlla che non vi siano persone o materiali sul percorso.','Segui la dimostrazione di Aguamenti; svolgi un tentativo guidato concentrandoti sulla direzione.','Descrivi dove è arrivato l’effetto e se il bersaglio concordato è stato rispettato.'],
 check:'L’allievo controlla il punto d’arrivo e riferisce il risultato senza inventare proprietà o effetti aggiuntivi.',
 question:'Produrre più acqua del necessario dimostra automaticamente una maggiore efficacia?',
 answer:'No. L’efficacia dipende dalla corrispondenza con il compito assegnato e dal controllo, non dalla quantità esibita.',source:'Lezioni della scuola, primo anno, voce Aguamenti. Attività guidata proposta per questa edizione.'},
 {title:'Avis',subtitle:'La forma evocata e i suoi limiti',
 theory:[
 'Avis fa apparire un piccolo stormo di uccelli dalla bacchetta. Le lezioni della scuola lo assegnano al primo anno di Trasfigurazione. Si studia come effetto evocativo: non si parte da un oggetto che viene trasformato davanti all’osservatore.',
 'La visualizzazione considera proporzioni, ali, becco e piumaggio. Colore e tonalità contribuiscono alla definizione dell’aspetto, mentre la concentrazione sostiene la coerenza dell’insieme. Il confronto con Avifors verrà approfondito nel terzo anno: Avifors modifica un bersaglio già presente, Avis produce un’apparizione.',
 'Il manuale descrive le forme evocate come temporanee e non come creazione di vita naturale. Nel quadro didattico adottato, i limiti di Gamp ricordano che somiglianza non significa autenticità: denaro, cibo, vita, informazioni e amore non si ottengono semplicemente imitandone l’apparenza. L’ultimo incontro conclude le due settimane del primo anno.'
 ],materials:'Area libera per la dimostrazione e scheda di osservazione delle forme aviarie.',
 steps:['Descrivi una forma aviaria semplice e individua le parti che devono essere riconoscibili.','Osserva Avis e annota origine, forma e presenza temporanea dell’effetto, senza usarlo contro i compagni.','Confronta Colovaria, Aguamenti e Avis: per ciascuno indica il risultato atteso e il controllo esercitato.'],
 check:'Lo studente distingue cambiamento cromatico, acqua e apparizione di volatili e riconosce i limiti del risultato.',
 question:'La comparsa di uccelli dimostra che è stata trasformata una materia già presente?',
 answer:'No. Bisogna conoscere l’origine dell’effetto: Avis viene descritto come apparizione, mentre Avifors trasforma un bersaglio.',source:'9, Avis; 4–5, Gamp. Collocazione al primo anno: lezioni della scuola.'}
];
FIRST_YEAR.forEach((lesson,i)=>Object.assign(LESSONS[i],lesson));
// La comparazione al terzo anno è un approfondimento di Avis, già introdotto al primo.
LESSONS[10].theory[0]='Avis, già studiato nel primo anno, fa apparire uccelli dalla bacchetta. Avifors trasforma invece un bersaglio in una forma di volatile. La differenza non sta soltanto nell’aspetto finale: nel primo caso si osserva un’apparizione temporanea, nel secondo si segue la trasformazione di materia presente.';
