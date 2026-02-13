# Guida per Sviluppatori

Questa guida spiega come modificare e compilare il progetto.

## Prerequisiti

- Python 3.10 o superiore
- Windows 10/11 (per compilare l'EXE)
- Git

## Setup Ambiente di Sviluppo

1. **Clona il repository**
   ```bash
   git clone https://github.com/Alessio1961/google-reviews-scraper.git
   cd google-reviews-scraper
   ```

2. **Crea ambiente virtuale (opzionale ma consigliato)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installa dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Installa browser Playwright**
   ```bash
   python -m playwright install chromium
   ```

## Test durante lo Sviluppo

### Test locale senza compilare

```bash
python src/main.py --url="URL_GOOGLE_MAPS" --output="test"
```

### Test encoding italiano

```bash
python test_encoding.py
```

Questo test verifica:
- Creazione corretta dei file CSV e DBF
- Encoding UTF-8 con BOM per CSV
- Compatibilità caratteri italiani (à, è, é, ì, ò, ù)
- Struttura campi DBF corretta

## Struttura Codice

### src/scraper.py

Contiene la classe `GoogleReviewsScraper` che:
- Utilizza Playwright per navigare su Google Maps
- Scrolla automaticamente per caricare tutte le recensioni
- Espande i testi completi delle recensioni
- Estrae tutti i dati richiesti
- Applica filtri opzionali (stelle)

**Selettori CSS principali:**
- `.m6QErb`: Contenitore scrollabile delle recensioni
- `[data-review-id]`: Singola recensione
- `.d4r55`: Nome recensore
- `[role="img"]`: Elemento stelle
- `.wiI7pd, .MyEned`: Testo recensione
- `.rsqaWe`: Data
- `.CDe7pd`: Risposta proprietario

**Nota:** I selettori CSS possono cambiare. Se Google Maps cambia la struttura HTML, sarà necessario aggiornarli.

### src/exporters.py

Contiene la classe `ReviewExporter` che gestisce:
- Export CSV con UTF-8 BOM
- Export DBF con codepage Windows-1252
- Gestione caratteri speciali
- Limiti campo DBF (nome max 10 caratteri, Character max 254)

**Campi DBF:**
- Nome campo max 10 caratteri (limitazione dBase)
- Character (C): max 254 caratteri
- Memo (M): lunghezza illimitata per testi lunghi
- Numeric (N): formato `N(lunghezza, decimali)`

### src/main.py

Entry point dell'applicazione:
- Parser argomenti CLI con `argparse`
- Gestione errori e feedback utente
- Coordinamento scraper ed exporter

## Compilazione EXE

### Manuale (Windows)

Usa lo script batch:
```bash
build.bat
```

L'EXE sarà in `dist/scraper.exe`.

### Con PyInstaller direttamente

```bash
pip install pyinstaller

pyinstaller --onefile --name scraper ^
    --hidden-import playwright ^
    --hidden-import dbf ^
    --collect-all playwright ^
    src/main.py
```

**Parametri PyInstaller:**
- `--onefile`: Crea singolo EXE
- `--name scraper`: Nome output
- `--hidden-import`: Importa moduli non rilevati automaticamente
- `--collect-all playwright`: Include tutti i file Playwright necessari

### Automatico (GitHub Actions)

Il workflow `.github/workflows/build.yml` compila automaticamente l'EXE quando:
- Si fa push su branch main/master
- Si crea un tag `v*` (es: v1.0.0)
- Si attiva manualmente (workflow_dispatch)

L'EXE viene:
- Caricato come artifact (disponibile per 30 giorni)
- Pubblicato nelle Releases (se si usa un tag)

## Debugging

### Errori di scraping

Se le recensioni non vengono estratte:

1. **Verifica selettori CSS**
   - Apri Google Maps in un browser
   - Usa DevTools (F12) per ispezionare gli elementi
   - Controlla se i selettori sono cambiati

2. **Aumenta timeout**
   ```python
   page.wait_for_selector('...', timeout=30000)  # 30 secondi
   ```

3. **Esegui con browser visibile**
   ```python
   browser = p.chromium.launch(headless=False)  # Vedi cosa succede
   ```

4. **Screenshot per debug**
   ```python
   page.screenshot(path='debug.png')
   ```

### Errori di encoding

Se i caratteri italiani non vengono salvati correttamente:

**CSV:**
- Verifica encoding UTF-8 con BOM: `encoding='utf-8-sig'`

**DBF:**
- Verifica codepage: `codepage='cp1252'`
- Windows-1252 è lo standard per VFP

## Modificare i Selettori CSS

Se Google Maps cambia la sua struttura HTML, aggiorna i selettori in `src/scraper.py`:

```python
# Esempio: cambiare selettore nome recensore
name_element = review_element.query_selector('.NUOVO_SELETTORE')
```

**Come trovare i nuovi selettori:**
1. Apri la pagina Google Maps
2. Premi F12 per DevTools
3. Usa il selettore elemento (icona freccia)
4. Clicca sull'elemento desiderato
5. Nel pannello Elements, vedi le classi CSS
6. Testa il selettore nella Console:
   ```javascript
   document.querySelector('.classe-css')
   ```

## Aggiungere Nuovi Formati Export

Per aggiungere un nuovo formato (es: JSON, Excel):

1. Aggiungi metodo in `src/exporters.py`:
   ```python
   def export_to_json(self, output_path: str) -> None:
       import json
       with open(f"{output_path}.json", 'w', encoding='utf-8') as f:
           json.dump(self.reviews, f, ensure_ascii=False, indent=2)
   ```

2. Modifica `export()` per includere il nuovo formato
3. Aggiungi opzione in `src/main.py`:
   ```python
   parser.add_argument('--format', choices=['csv', 'dbf', 'json', 'both'])
   ```

## Performance

### Ottimizzare lo scraping

- **Ridurre sleep times**: Attenzione a non andare troppo veloce (rischio ban)
- **Parallel processing**: Non consigliato per web scraping (può causare rate limiting)
- **Caching**: Se scrapi la stessa pagina più volte, salva risultati intermedi

### Gestire grandi quantità di recensioni

Se una pagina ha migliaia di recensioni:
- Lo scroll può richiedere diversi minuti
- Considera un timeout massimo
- Mostra progresso all'utente

## Licenza

Questo progetto è sotto licenza MIT - vedi LICENSE per dettagli.

## Contribuire

1. Fork il progetto
2. Crea un branch (`git checkout -b feature/nuova-feature`)
3. Commit le modifiche (`git commit -m 'Aggiungi feature'`)
4. Push al branch (`git push origin feature/nuova-feature`)
5. Apri una Pull Request

## Supporto

Per domande o problemi:
- Apri una [Issue](https://github.com/Alessio1961/google-reviews-scraper/issues)
- Descrivi il problema in dettaglio
- Includi versione Python e sistema operativo
- Allega screenshot se possibile
