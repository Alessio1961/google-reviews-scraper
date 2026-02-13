"""
Google Reviews Scraper - Entry point CLI
Applicazione per scaricare recensioni da Google Maps
"""

import sys
import argparse
from pathlib import Path

# Aggiungi la directory src al path per gli import
sys.path.insert(0, str(Path(__file__).parent))

from scraper import GoogleReviewsScraper
from exporters import ReviewExporter


def main():
    """Entry point principale dell'applicazione"""
    
    # Parser argomenti linea di comando
    parser = argparse.ArgumentParser(
        description='Google Reviews Scraper - Scarica recensioni da Google Maps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  
  Scarica tutte le recensioni:
    scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6"
  
  Scarica solo recensioni con 5 stelle:
    scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --stars=5
  
  Specifica nome file di output:
    scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --output="recensioni_negozio"
  
  Esporta solo in CSV:
    scraper.exe --url="https://maps.app.goo.gl/91jma2zHp9mWgG6M6" --format=csv
        """
    )
    
    parser.add_argument(
        '--url',
        required=True,
        help='URL della pagina Google Maps (obbligatorio)'
    )
    
    parser.add_argument(
        '--output',
        default='recensioni',
        help='Nome base file output senza estensione (default: recensioni)'
    )
    
    parser.add_argument(
        '--stars',
        type=int,
        choices=[1, 2, 3, 4, 5],
        help='Filtro per stelle (1-5). Se non specificato, scarica tutte le recensioni'
    )
    
    parser.add_argument(
        '--format',
        choices=['csv', 'dbf', 'both'],
        default='both',
        help='Formato di output: csv, dbf o both (default: both)'
    )
    
    # Parse argomenti
    args = parser.parse_args()
    
    # Banner
    print("=" * 60)
    print("   GOOGLE REVIEWS SCRAPER")
    print("   Scarica recensioni da Google Maps in CSV e DBF")
    print("=" * 60)
    print()
    
    try:
        # Inizializza scraper
        scraper = GoogleReviewsScraper(
            url=args.url,
            stars_filter=args.stars
        )
        
        # Esegui scraping
        reviews = scraper.scrape()
        
        if not reviews:
            print()
            print("⚠️  Nessuna recensione trovata o estratta.")
            print("   Verifica che l'URL sia corretto e che ci siano recensioni disponibili.")
            return 1
        
        # Esporta recensioni
        print()
        print("💾 Esportazione recensioni...")
        exporter = ReviewExporter(scraper.get_reviews_as_dicts())
        exporter.export(args.output, args.format)
        
        # Riepilogo finale
        print()
        print("=" * 60)
        print(f"✅ COMPLETATO CON SUCCESSO!")
        print(f"   Recensioni scaricate: {len(reviews)}")
        if args.stars:
            print(f"   Filtro stelle: {args.stars}")
        print(f"   File generati: {args.output}.*")
        print("=" * 60)
        
        return 0
    
    except KeyboardInterrupt:
        print()
        print("⚠️  Operazione annullata dall'utente")
        return 1
    
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERRORE: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
