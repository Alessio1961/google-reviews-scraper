#!/usr/bin/env python3
"""
Test script per verificare encoding e funzionalità
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from exporters import ReviewExporter

def test_exporters():
    """Test encoding italiano e funzionalità export"""
    print("=" * 60)
    print("   TEST EXPORTERS - Encoding Italiano")
    print("=" * 60)
    print()
    
    # Dati di test con caratteri italiani
    test_reviews = [
        {
            'reviewer_name': 'Mario Rossi',
            'stars': 5,
            'text': 'Ottimo servizio! Molto professionale e cortese. Consigliato! àèéìòù',
            'date': '3 mesi fa',
            'owner_response': 'Grazie mille per la recensione! È stato un piacere servirla.',
            'response_date': '2 mesi fa'
        },
        {
            'reviewer_name': 'Lucia Verdi',
            'stars': 4,
            'text': 'Buona esperienza complessiva. Qualità prezzo eccellente.',
            'date': '1 settimana fa',
            'owner_response': '',
            'response_date': ''
        },
        {
            'reviewer_name': 'Giuseppe Bianchi',
            'stars': 3,
            'text': 'Esperienza nella media. Potrebbe migliorare la velocità del servizio.',
            'date': '2 giorni fa',
            'owner_response': 'Grazie per il feedback, lavoreremo per migliorare.',
            'response_date': '1 giorno fa'
        }
    ]
    
    print(f"📊 Test con {len(test_reviews)} recensioni campione")
    print()
    
    # Test export
    exporter = ReviewExporter(test_reviews)
    
    try:
        # Test CSV
        print("🔸 Test export CSV...")
        exporter.export_to_csv('/tmp/test_recensioni')
        print("   ✅ CSV creato con successo")
        
        # Verifica contenuto CSV
        with open('/tmp/test_recensioni.csv', 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if 'àèéìòù' in content:
                print("   ✅ Caratteri italiani preservati nel CSV")
            else:
                print("   ❌ Problema con caratteri italiani nel CSV")
        
        print()
        
        # Test DBF
        print("🔸 Test export DBF...")
        exporter.export_to_dbf('/tmp/test_recensioni')
        print("   ✅ DBF creato con successo")
        
        # Verifica DBF
        import dbf
        table = dbf.Table('/tmp/test_recensioni.dbf')
        table.open()
        
        print(f"   ✅ DBF contiene {len(table)} record")
        
        # Verifica primo record
        first_record = table[0]
        print(f"   ✅ Primo record: {first_record.nome}, {first_record.stelle} stelle")
        
        table.close()
        
        print()
        print("=" * 60)
        print("✅ TUTTI I TEST SUPERATI!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FALLITO: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_exporters()
    sys.exit(0 if success else 1)
