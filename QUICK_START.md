# 🚀 Quick Start Guide

Guida rapida per iniziare subito a usare Google Reviews Scraper.

## ⚡ Utilizzo Super Rapido

### 1. Scarica l'Applicazione

Vai alle [Releases](../../releases/latest) e scarica `scraper.exe`.

### 2. Usa l'Applicazione

Apri il **Prompt dei comandi** (CMD) nella cartella dove hai salvato `scraper.exe` e digita:

```cmd
scraper.exe --url="https://maps.app.goo.gl/TUO_LINK_QUI"
```

Sostituisci `TUO_LINK_QUI` con l'URL della pagina Google Maps che vuoi analizzare.

### 3. Trova i File

L'applicazione creerà automaticamente due file nella stessa cartella:
- `recensioni.csv` - File CSV per Excel
- `recensioni.dbf` - File DBF per Visual FoxPro

## 📍 Come Ottenere l'URL di Google Maps

1. Apri [Google Maps](https://www.google.com/maps)
2. Cerca l'attività/luogo che ti interessa
3. Clicca su "Condividi"
4. Copia il link breve (es: `https://maps.app.goo.gl/...`)
5. Usa questo link con il parametro `--url`

## 🎯 Esempi Pratici

### Tutte le recensioni
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
```

### Solo 5 stelle ⭐⭐⭐⭐⭐
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --stars=5
```

### Solo CSV
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --format=csv
```

### Nome file personalizzato
```cmd
scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --output="mio_ristorante"
```
Creerà: `mio_ristorante.csv` e `mio_ristorante.dbf`

## 🦊 Per Utenti Visual FoxPro

### Metodo 1: Usa da VFP

```foxpro
* Scarica recensioni
RUN scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6"

* Apri il file
USE recensioni.dbf
BROWSE
```

### Metodo 2: Scarica prima, poi apri

1. Esegui da CMD:
   ```cmd
   scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --format=dbf
   ```

2. In Visual FoxPro:
   ```foxpro
   USE recensioni.dbf
   BROWSE
   ```

## 📊 Cosa Contengono i File

### CSV (per Excel)
Puoi aprirlo direttamente con Excel. Contiene:
- Nome recensore
- Stelle (1-5)
- Testo recensione
- Data recensione
- Risposta proprietario (se presente)
- Data risposta (se presente)

### DBF (per VFP)
Stesso contenuto del CSV, ma in formato Visual FoxPro con campi:
- `nome` - Nome recensore
- `stelle` - Numero stelle
- `testo` - Testo recensione (Memo)
- `data` - Data recensione
- `risposta` - Risposta proprietario (Memo)
- `data_risp` - Data risposta

## ❓ Domande Comuni

### L'antivirus blocca il file?
È normale. Il file è sicuro. Aggiungi un'eccezione nell'antivirus oppure esegui come amministratore.

### Non funziona?
- Verifica che l'URL sia completo e corretto
- Assicurati di avere connessione internet
- Prova ad eseguire come amministratore

### Quanto tempo ci vuole?
Dipende dal numero di recensioni:
- 100 recensioni: ~1-2 minuti
- 500 recensioni: ~5-10 minuti
- 1000+ recensioni: ~15+ minuti

### Posso scaricare più luoghi contemporaneamente?
Sì! Apri più finestre CMD ed esegui il comando per ogni luogo.

## 📚 Documentazione Completa

- [README completo](README.md) - Tutte le funzionalità
- [Guida sviluppatori](DEVELOPER_GUIDE.md) - Per modificare il codice
- [Esempi Python](examples.py) - Uso programmatico

## 🆘 Hai Bisogno di Aiuto?

Apri una [Issue](../../issues) su GitHub descrivendo il problema.

---

**Buon lavoro! 🎉**
