# 🌟 Google Reviews Scraper

Applicazione console Windows per scaricare recensioni da Google Maps e salvarle in formato **CSV** e **DBF** compatibile con **Visual FoxPro**.

---

📖 **[Quick Start Guide](QUICK_START.md)** | 👨‍💻 **[Developer Guide](DEVELOPER_GUIDE.md)** | 💡 **[Examples](examples.py)**

---

## 📥 Download

**[➡️ Scarica l'ultima versione (scraper.exe)](../../releases/latest)**

Vai alla sezione [Releases](../../releases) e scarica il file `scraper.exe`.

## ✨ Caratteristiche

- ✅ **Scraping automatico** da Google Maps
- ✅ **Scroll automatico** per caricare tutte le recensioni
- ✅ **Estrazione dati completi**: nome, stelle, testo, data, risposta proprietario
- ✅ **Filtro per stelle** (1-5)
- ✅ **Export CSV** con encoding UTF-8 BOM (compatibile Excel e VFP)
- ✅ **Export DBF** formato dBase (compatibile Visual FoxPro)
- ✅ **Nessuna installazione** richiesta - file EXE standalone
- ✅ **Supporto caratteri italiani** (à, è, é, ì, ò, ù)

## 🚀 Utilizzo Base

### Da Prompt dei Comandi (CMD)

Apri il **Prompt dei comandi** nella cartella dove hai scaricato `scraper.exe`:

```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
```

Questo comando scaricherà tutte le recensioni e creerà due file:
- `recensioni.csv`
- `recensioni.dbf`

## 📋 Parametri Disponibili

| Parametro | Obbligatorio | Descrizione | Esempio |
|-----------|--------------|-------------|---------|
| `--url` | ✅ Sì | URL della pagina Google Maps | `--url="https://maps.app.goo.gl/..."` |
| `--output` | No | Nome file output (senza estensione) | `--output="mie_recensioni"` |
| `--stars` | No | Filtro per stelle (1-5) | `--stars=5` |
| `--format` | No | Formato: `csv`, `dbf` o `both` | `--format=csv` |

## 💡 Esempi di Utilizzo

### Scarica tutte le recensioni
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
```

### Scarica solo recensioni a 5 stelle
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --stars=5 --output="5stelle"
```

### Scarica recensioni negative (1-2 stelle)
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --stars=1 --output="negative"
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --stars=2 --output="negative2"
```

### Esporta solo in formato CSV
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --format=csv
```

### Esporta solo in formato DBF
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --format=dbf
```

## 🦊 Utilizzo da Visual FoxPro

### Esegui lo scraper da VFP

```foxpro
* Scarica tutte le recensioni
RUN scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --output="tutte_recensioni"

* Scarica solo recensioni 5 stelle
RUN scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --output="5stelle" --stars=5 --format=dbf

* Attendi il completamento
WAIT WINDOW "Recensioni scaricate!" TIMEOUT 2
```

### Leggi i dati scaricati in VFP

```foxpro
* Apri il file DBF
USE tutte_recensioni.dbf
BROWSE

* Filtra recensioni 5 stelle
SELECT * FROM tutte_recensioni WHERE stelle = 5

* Conta recensioni per stelle
SELECT stelle, COUNT(*) as totale FROM tutte_recensioni GROUP BY stelle

* Cerca parola chiave nel testo
SELECT * FROM tutte_recensioni WHERE "ottimo" $ LOWER(testo)

* Esporta in report
REPORT FORM mio_report TO PRINTER
```

### Esempio completo: Analisi recensioni

```foxpro
LOCAL lcURL, lcOutput

* Imposta parametri
lcURL = "https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
lcOutput = "recensioni_" + DTOC(DATE(), 1)

* Scarica recensioni
RUN scraper.exe --url="&lcURL" --output="&lcOutput"

* Apri e analizza
USE &lcOutput
BROWSE TITLE "Recensioni Google Maps"

* Statistiche
? "Totale recensioni:", RECCOUNT()
? "Media stelle:", AVERAGE(stelle)
? "Recensioni con risposta:", ;
  RECCOUNT("risposta <> ''")

USE
```

### Import CSV in VFP (alternativo)

Se preferisci usare il CSV invece del DBF:

```foxpro
* Import da CSV
APPEND FROM recensioni.csv TYPE DELIMITED WITH CHARACTER "

* Oppure usa IMPORT
IMPORT FROM recensioni.csv TYPE CSV
```

## 📊 Struttura Dati

I file generati contengono i seguenti campi:

### File CSV
| Campo | Descrizione |
|-------|-------------|
| `reviewer_name` | Nome del recensore |
| `stars` | Numero di stelle (1-5) |
| `text` | Testo completo della recensione |
| `date` | Data della recensione |
| `owner_response` | Risposta del proprietario (se presente) |
| `response_date` | Data della risposta (se presente) |

### File DBF
| Campo | Tipo | Dimensione | Descrizione |
|-------|------|------------|-------------|
| `nome` | Character | 100 | Nome del recensore |
| `stelle` | Numeric | 1 | Numero di stelle (1-5) |
| `testo` | Memo | - | Testo completo della recensione |
| `data` | Character | 50 | Data della recensione |
| `risposta` | Memo | - | Risposta del proprietario (se presente) |
| `data_risp` | Character | 50 | Data della risposta (se presente) |

**Nota**: I nomi dei campi nel DBF sono abbreviati per rispettare il limite di 10 caratteri del formato dBase. I campi `testo` e `risposta` sono di tipo **Memo (M)** per supportare testi lunghi.

## 🛠️ Troubleshooting

### L'applicazione non si avvia
- Verifica di avere **Windows 10 o superiore**
- Disabilita temporaneamente l'antivirus (potrebbe bloccare l'EXE)
- Esegui come amministratore (tasto destro → "Esegui come amministratore")

### Nessuna recensione trovata
- Verifica che l'URL sia corretto e completo
- Controlla che la pagina abbia recensioni visibili
- Prova ad aprire l'URL in un browser per verificare

### Errore "URL non valido"
- Assicurati di includere le virgolette: `--url="..."`
- Usa l'URL completo di Google Maps (incluso `https://`)

### Il file DBF non si apre in VFP
- Assicurati di usare Visual FoxPro 6.0 o superiore
- Verifica che il file non sia corrotto
- Prova a ricompilare con il parametro `--format=dbf`

### Caratteri strani nel testo
- Per CSV: apri con Excel e assicurati che usi encoding UTF-8
- Per DBF: dovrebbe funzionare direttamente in VFP con caratteri italiani

### Lo scraping è lento
- È normale! Google Maps carica le recensioni gradualmente
- Il tempo dipende dal numero di recensioni (può richiedere diversi minuti)
- Non interrompere il processo durante lo scroll

## 🔧 Compilazione Locale (per sviluppatori)

Se vuoi modificare il codice e compilare l'EXE da solo:

### Prerequisiti
- Python 3.10 o superiore
- Windows 10/11

### Passi

1. **Clona il repository**
   ```cmd
   git clone https://github.com/Alessio1961/google-reviews-scraper.git
   cd google-reviews-scraper
   ```

2. **Installa dipendenze**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Installa browser Playwright**
   ```cmd
   python -m playwright install chromium
   ```

4. **Compila con build.bat**
   ```cmd
   build.bat
   ```

Il file `scraper.exe` sarà nella cartella `dist/`.

### Struttura Progetto

```
google-reviews-scraper/
├── src/
│   ├── scraper.py          # Logica scraping Google Maps
│   ├── exporters.py        # Export CSV e DBF
│   └── main.py             # Entry point CLI
├── .github/
│   └── workflows/
│       └── build.yml       # GitHub Actions build automatico
├── requirements.txt        # Dipendenze Python
├── build.bat              # Script build locale Windows
└── README.md              # Questa documentazione
```

## 📝 Note Tecniche

- **Engine**: Playwright per scraping affidabile
- **Export CSV**: UTF-8 con BOM per compatibilità Excel/VFP
- **Export DBF**: Formato dBase III con codepage Windows-1252
- **Compatibilità**: Testato con Visual FoxPro 6.0, 7.0, 8.0, 9.0
- **Browser**: Chromium headless (incluso nell'EXE)

## 🤝 Contributi

Contributi, segnalazioni bug e richieste di funzionalità sono benvenuti!

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/nuova-funzione`)
3. Commit le modifiche (`git commit -m 'Aggiunge nuova funzione'`)
4. Push al branch (`git push origin feature/nuova-funzione`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## ⚠️ Disclaimer

Questo strumento è fornito "così com'è" per scopi educativi e di ricerca. L'uso dello scraping deve rispettare i Termini di Servizio di Google Maps. L'autore non è responsabile per un uso improprio dello strumento.

## 📧 Supporto

Per domande, problemi o suggerimenti, apri una [Issue](../../issues) su GitHub.

---

**Sviluppato con ❤️ per la comunità Visual FoxPro italiana**