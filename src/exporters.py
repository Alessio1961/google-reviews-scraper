"""
Modulo per l'esportazione delle recensioni in formati CSV e DBF
"""

import csv
from typing import List, Dict
from pathlib import Path
import dbf


class ReviewExporter:
    """Classe per esportare recensioni in vari formati"""
    
    def __init__(self, reviews: List[Dict]):
        self.reviews = reviews
    
    def export_to_csv(self, output_path: str) -> None:
        """
        Esporta recensioni in formato CSV con encoding UTF-8 BOM
        per compatibilità con Excel e Visual FoxPro
        """
        if not self.reviews:
            print("⚠️  Nessuna recensione da esportare")
            return
        
        csv_file = f"{output_path}.csv"
        
        try:
            # UTF-8 con BOM per compatibilità Excel/VFP
            with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
                fieldnames = ['reviewer_name', 'stars', 'text', 'date', 
                             'owner_response', 'response_date']
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',', 
                                       quotechar='"', quoting=csv.QUOTE_ALL)
                
                writer.writeheader()
                writer.writerows(self.reviews)
            
            print(f"✅ File CSV creato: {csv_file} ({len(self.reviews)} recensioni)")
        
        except Exception as e:
            print(f"❌ Errore durante la creazione del CSV: {e}")
            raise
    
    def export_to_dbf(self, output_path: str) -> None:
        """
        Esporta recensioni in formato DBF compatibile con Visual FoxPro
        """
        if not self.reviews:
            print("⚠️  Nessuna recensione da esportare")
            return
        
        dbf_file = f"{output_path}.dbf"
        
        try:
            # Definizione struttura DBF
            # Visual FoxPro ha limite di 254 caratteri per campo Character
            # Usiamo Memo (M) per testi lunghi
            table = dbf.Table(
                dbf_file,
                'reviewer_name C(100); stars N(1,0); text M; date C(50); '
                'owner_response M; response_date C(50)',
                codepage='cp1252'  # Windows-1252 per compatibilità VFP
            )
            
            table.open(mode=dbf.READ_WRITE)
            
            for review in self.reviews:
                # Tronca i campi per evitare overflow
                reviewer_name = review.get('reviewer_name', '')[:100]
                stars = int(review.get('stars', 0))
                text = review.get('text', '')
                date = review.get('date', '')[:50]
                owner_response = review.get('owner_response', '')
                response_date = review.get('response_date', '')[:50]
                
                # Aggiungi record
                table.append({
                    'reviewer_name': reviewer_name,
                    'stars': stars,
                    'text': text,
                    'date': date,
                    'owner_response': owner_response,
                    'response_date': response_date
                })
            
            table.close()
            
            print(f"✅ File DBF creato: {dbf_file} ({len(self.reviews)} recensioni)")
        
        except Exception as e:
            print(f"❌ Errore durante la creazione del DBF: {e}")
            raise
    
    def export(self, output_path: str, format_type: str = 'both') -> None:
        """
        Esporta recensioni nel formato specificato
        
        Args:
            output_path: Percorso base del file (senza estensione)
            format_type: 'csv', 'dbf' o 'both'
        """
        if format_type in ['csv', 'both']:
            self.export_to_csv(output_path)
        
        if format_type in ['dbf', 'both']:
            self.export_to_dbf(output_path)
