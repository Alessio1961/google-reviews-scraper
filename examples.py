#!/usr/bin/env python3
"""
Esempio di utilizzo programmatico del Google Reviews Scraper
"""

import sys
from pathlib import Path

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scraper import GoogleReviewsScraper
from exporters import ReviewExporter


def esempio_base():
    """Esempio base: scarica tutte le recensioni"""
    print("=== ESEMPIO BASE ===")
    
    url = "https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
    
    # Crea scraper
    scraper = GoogleReviewsScraper(url)
    
    # Esegui scraping
    reviews = scraper.scrape()
    
    # Esporta
    exporter = ReviewExporter(scraper.get_reviews_as_dicts())
    exporter.export('output_base', 'both')
    
    print(f"Scaricate {len(reviews)} recensioni")


def esempio_filtro_stelle():
    """Esempio con filtro stelle"""
    print("\n=== ESEMPIO CON FILTRO STELLE ===")
    
    url = "https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
    
    # Scarica solo recensioni a 5 stelle
    scraper = GoogleReviewsScraper(url, stars_filter=5)
    reviews = scraper.scrape()
    
    # Esporta solo CSV
    exporter = ReviewExporter(scraper.get_reviews_as_dicts())
    exporter.export('recensioni_5stelle', 'csv')
    
    print(f"Scaricate {len(reviews)} recensioni a 5 stelle")


def esempio_analisi_dati():
    """Esempio: analisi dati dopo lo scraping"""
    print("\n=== ESEMPIO ANALISI DATI ===")
    
    url = "https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
    
    scraper = GoogleReviewsScraper(url)
    reviews = scraper.scrape()
    
    # Analizza i dati
    if reviews:
        # Conta recensioni per stelle
        stelle_count = {}
        for review in reviews:
            stars = review.stars
            stelle_count[stars] = stelle_count.get(stars, 0) + 1
        
        # Calcola media
        media = sum(r.stars for r in reviews) / len(reviews)
        
        # Conta risposte proprietario
        con_risposta = sum(1 for r in reviews if r.owner_response)
        
        print(f"Totale recensioni: {len(reviews)}")
        print(f"Media stelle: {media:.2f}")
        print(f"Distribuzione stelle:")
        for stelle in sorted(stelle_count.keys(), reverse=True):
            print(f"  {stelle} stelle: {stelle_count[stelle]}")
        print(f"Recensioni con risposta: {con_risposta} ({con_risposta/len(reviews)*100:.1f}%)")


def esempio_usa_dati_in_python():
    """Esempio: usa i dati direttamente in Python"""
    print("\n=== ESEMPIO USO DATI IN PYTHON ===")
    
    url = "https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
    
    scraper = GoogleReviewsScraper(url, stars_filter=1)
    reviews = scraper.scrape()
    
    print(f"Recensioni negative (1 stella): {len(reviews)}")
    
    # Estrai parole chiave comuni nelle recensioni negative
    if reviews:
        parole_comuni = {}
        for review in reviews:
            parole = review.text.lower().split()
            for parola in parole:
                if len(parola) > 4:  # Solo parole lunghe
                    parole_comuni[parola] = parole_comuni.get(parola, 0) + 1
        
        # Top 5 parole più comuni
        print("Parole più comuni nelle recensioni negative:")
        for parola, count in sorted(parole_comuni.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {parola}: {count}")


if __name__ == '__main__':
    # ATTENZIONE: Questi esempi eseguono scraping reale
    # Commenta gli esempi che non vuoi eseguire
    
    print("Esempi Google Reviews Scraper")
    print("=" * 60)
    
    # esempio_base()
    # esempio_filtro_stelle()
    # esempio_analisi_dati()
    # esempio_usa_dati_in_python()
    
    print("\n⚠️  Gli esempi sono commentati per evitare scraping accidentale")
    print("Decommenta gli esempi nel codice per eseguirli")
